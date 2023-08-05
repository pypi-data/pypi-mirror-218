from __future__ import annotations

import logging
import os
from itertools import islice
from pathlib import Path
from typing import TYPE_CHECKING

from joblib import Parallel, delayed
from rich import print as rprint
from sqlitedict import SqliteDict
from tqdm import tqdm

if TYPE_CHECKING:
    pass

import hydrusvideodeduplicator.hydrus_api as hydrus_api
import hydrusvideodeduplicator.hydrus_api.utils
from .vpdqpy.vpdqpy import Vpdq

from .config import DEDUP_DATABASE_DIR, DEDUP_DATABASE_FILE, DEDUP_DATABASE_NAME
from .dedup_util import database_accessible, find_tag_in_tags, get_file_names_hydrus


class HydrusVideoDeduplicator:
    hydlog = logging.getLogger("hydlog")
    threshold: float = 75.0
    _DEBUG = False

    def __init__(self, client: hydrus_api.Client, verify_connection: bool = True):
        self.client = client
        if verify_connection:
            self.verify_api_connection()
        self.hydlog.setLevel(logging.WARNING)

        # Commonly used things from the Hydrus database
        # If any of these are large they should probably be lazily loaded
        self.all_services = self.client.get_services()

    # Verify client connection and permissions
    # Will throw a hydrus_api.APIError if something is wrong
    def verify_api_connection(self):
        self.hydlog.info(
            f"Client API version: v{self.client.VERSION} | Endpoint API version: v{self.client.get_api_version()['version']}"
        )
        hydrus_api.utils.verify_permissions(self.client, hydrus_api.utils.Permission)

    # This is the master function of the class
    def deduplicate(self, overwrite: bool = False, custom_query: list | None = None, skip_hashing: bool | None = False):
        # Add perceptual hashes to video files
        # system:filetype tags are really inconsistent
        search_tags = ['system:filetype=video, gif, apng', 'system:has duration']

        query = False
        if custom_query is not None:
            custom_query = [x for x in custom_query if x.strip()]  # Remove whitespace and empty strings
            if len(custom_query) > 0:
                search_tags.extend(custom_query)
                rprint(f"[yellow] Custom Query: {custom_query}")
                query = True

        video_hashes = None
        if skip_hashing:
            rprint("[yellow] Skipping perceptual hashing")
            if query:
                video_hashes = set(self._retrieve_video_hashes(search_tags))
        else:
            all_video_hashes = self._retrieve_video_hashes(search_tags)
            self._add_perceptual_hashes_to_db(overwrite=overwrite, video_hashes=all_video_hashes)
        
        if query and not skip_hashing:
            video_hashes = set(self._retrieve_video_hashes(search_tags))

        if query:
            self._find_potential_duplicates(limited_video_hashes=video_hashes)
        else:
            self._find_potential_duplicates(limited_video_hashes=None)

        self.hydlog.info("Deduplication done.")

    @staticmethod
    def _calculate_perceptual_hash(video: str | bytes) -> str:
        perceptual_hash = Vpdq.vpdq_to_json(Vpdq.computeHash(video))
        assert perceptual_hash != "[]"
        return perceptual_hash

    def _retrieve_video_hashes(self, search_tags) -> list:
        all_video_hashes = self.client.search_files(
            search_tags,
            file_sort_type=hydrus_api.FileSortType.FILE_SIZE,
            return_hashes=True,
            file_sort_asc=True,
            return_file_ids=False,
        )["hashes"]
        return all_video_hashes

    def _add_perceptual_hashes_to_db(self, overwrite: bool, video_hashes=set | list) -> None:
        # Create database folder
        try:
            os.makedirs(DEDUP_DATABASE_DIR, exist_ok=False)
            # Exception before this log if directory already exists
            self.hydlog.info(f"Created DB dir {DEDUP_DATABASE_DIR}")
        except OSError:
            pass

        with SqliteDict(str(DEDUP_DATABASE_FILE), tablename="videos", flag="c") as hashdb:
            dblen = len(hashdb)
            dbsize = os.path.getsize(DEDUP_DATABASE_FILE)

            if dblen > 0:
                rprint(f"[blue] Database found with {dblen} videos already hashed.")
                self.hydlog.info(f"Database found of length {dblen}, size {dbsize} bytes")
            else:
                self.hydlog.info(f"Database not found. Creating one at {DEDUP_DATABASE_FILE}")

            try:
                with tqdm(total=len(video_hashes), dynamic_ncols=True, unit="video", colour="BLUE") as pbar:
                    count_since_last_commit = 0
                    COMMIT_INTERVAL = 16

                    for video_hash in video_hashes:
                        pbar.update(1)
                        # Only calculate new hash if it's missing or if overwrite is true
                        if not overwrite and video_hash in hashdb and "perceptual_hash" in hashdb[video_hash]:
                            continue

                        # Get video file from Hydrus
                        try:
                            video_response = self.client.get_file(hash_=video_hash)
                            # video_metadata = self.client.get_file_metadata(hashes=[video_hash], only_return_basic_information=False)
                            # print(video_metadata)
                        except hydrus_api.HydrusAPIException:
                            rprint("[red] Failed to get video from Hydrus.")
                            self.hydlog.error("Error getting video from Hydrus.")
                            continue

                        # Calculate perceptual_hash
                        try:
                            perceptual_hash = self._calculate_perceptual_hash(video_response.content)
                        except Exception as exc:
                            rprint("[red] Failed to calculate a perceptual hash.")
                            self.hydlog.exception(exc)
                            self.hydlog.error(f"Errored file hash: {video_hash}")
                        else:
                            # Write perceptual hash to DB
                            row = hashdb.get(video_hash, {})
                            row["perceptual_hash"] = perceptual_hash
                            hashdb[video_hash] = row

                            # Batch DB commits to avoid excessive writes
                            count_since_last_commit += 1
                            if count_since_last_commit >= COMMIT_INTERVAL:
                                hashdb.commit()
                                count_since_last_commit = 0
                                self.hydlog.debug("Committed perceptual hashes to database.")

                            self.hydlog.debug("Perceptual hash calculated.")

            except KeyboardInterrupt:
                interrupt_msg = "Perceptual hash processing was interrupted!"
                rprint(f"[yellow] {interrupt_msg}")
                self.hydlog.error(interrupt_msg)

            else:
                rprint("[green] Finished perceptual hash processing.")

            finally:
                hashdb.commit()
                self.hydlog.info("Finished perceptual hash processing.")

    def get_potential_duplicate_count_hydrus(self) -> int:
        return self.client.get_potentials_count(
            file_service_keys=[self.all_services["all_local_files"][0]["service_key"]]
        )["potential_duplicates_count"]

    def compare_videos(self, video1_hash: str, video2_hash: str, video1_phash: str, video2_phash: str):
        vpdq_hash1 = Vpdq.json_to_vpdq(video1_phash)
        vpdq_hash2 = Vpdq.json_to_vpdq(video2_phash)
        similar, similarity = Vpdq.is_similar(vpdq_hash1, vpdq_hash2, self.threshold)

        if similar:
            if self._DEBUG:
                # Getting the file names will be VERY slow because of the API call
                # file_names = get_file_names_hydrus(self.client, [video1_hash, video2_hash])
                # self.hydlog.info(f"Duplicates filenames: {file_names}")
                self.hydlog.info(f"\"Similar {similarity}%: {video1_hash}\" and \"{video2_hash}\"")

            new_relationship = {
                "hash_a": str(video1_hash),
                "hash_b": str(video2_hash),
                "relationship": int(hydrus_api.DuplicateStatus.POTENTIAL_DUPLICATES),
                "do_default_content_merge": True,
            }

            self.client.set_file_relationships([new_relationship])

    # Delete cache row in database
    @staticmethod
    def clear_search_cache():
        try:
            with SqliteDict(str(DEDUP_DATABASE_FILE), tablename="videos", flag="c") as hashdb:
                for key in hashdb:
                    row = hashdb[key]
                    if "farthest_search_index" in row:
                        del row["farthest_search_index"]
                    hashdb[key] = row
                hashdb.commit()
        except OSError:
            rprint(f"[red] Database does not exist. Cannot clear search cache.")

    # Sliding window duplicate comparisons
    # Alternatively, I could scan duplicates when added and never do it again which would be one of the best ways without a VP tree
    def _find_potential_duplicates(self, limited_video_hashes: list | set | None = None) -> None:
        if not database_accessible(DEDUP_DATABASE_FILE, tablename="videos", verbose=True):
            rprint(f"[red] Could not search for duplicates.")
            return

        # Number of potential duplicates before adding more. Just for user info.
        pre_dedupe_count = self.get_potential_duplicate_count_hydrus()

        # BUG: If this process is interrupted, the farthest_search_index will not save for ANY entries.
        #      I think it might be because every entry in the column needs an entry for SQlite but I'm not sure.
        video_counter = 0
        with SqliteDict(str(DEDUP_DATABASE_FILE), tablename="videos", flag="c") as hashdb:
            try:
                if limited_video_hashes is not None:
                    total = len(limited_video_hashes)
                else:
                    total = len(hashdb)

                with tqdm(
                    dynamic_ncols=True, total=total, desc="Finding duplicates", unit="video", colour="BLUE"
                ) as pbar:
                    # -1 is all cores, -2 is all cores but one
                    with Parallel(n_jobs=-2) as parallel:
                        if limited_video_hashes is not None:
                            # Avoid checking if in hashdb for each hash. Just do it now.
                            clean_all_retrieved_video_hashes = [
                                video_hash for video_hash in limited_video_hashes if video_hash in hashdb
                            ]

                            for i, video1_hash in enumerate(clean_all_retrieved_video_hashes):
                                video_counter += 1
                                pbar.update(1)
                                parallel(
                                    delayed(self.compare_videos)(
                                        video1_hash,
                                        clean_all_retrieved_video_hashes[j],
                                        hashdb[video1_hash]["perceptual_hash"],
                                        hashdb[clean_all_retrieved_video_hashes[j]]["perceptual_hash"],
                                    )
                                    for j in range(i + 1, len(clean_all_retrieved_video_hashes))
                                )

                        else:
                            count_since_last_commit = 0
                            commit_interval = 32

                            for i, video1_hash in enumerate(hashdb):
                                video_counter += 1
                                pbar.update(1)

                                row = hashdb[video1_hash]

                                # Store last furthest searched position in the database for each element
                                # This way you only have to start searching at that place instead of at i+1 if it exists
                                row.setdefault("farthest_search_index", i + 1)

                                # This is not necessary but may increase speed by avoiding any of the code below
                                if row["farthest_search_index"] >= len(hashdb) - 1:
                                    continue

                                parallel(
                                    delayed(self.compare_videos)(
                                        video1_hash,
                                        video2_hash,
                                        hashdb[video1_hash]["perceptual_hash"],
                                        hashdb[video2_hash]["perceptual_hash"],
                                    )
                                    for video2_hash in islice(hashdb, row["farthest_search_index"], None)
                                )

                                # Update furthest search position to the current length of the table
                                row["farthest_search_index"] = len(hashdb) - 1
                                hashdb[video1_hash] = row
                                count_since_last_commit += 1

                                if count_since_last_commit >= commit_interval:
                                    hashdb.commit()
                                    count_since_last_commit = 0

            except KeyboardInterrupt:
                pass
            finally:
                hashdb.commit()

        # Statistics for user
        post_dedupe_count = self.get_potential_duplicate_count_hydrus()
        new_dedupes_count = post_dedupe_count - pre_dedupe_count
        if new_dedupes_count > 0:
            rprint(f"[green] {new_dedupes_count} new potential duplicates marked for processing!")
        else:
            rprint("[green] No new potential duplicates found.")

    @staticmethod
    def batched(iterable, n):
        "Batch data into tuples of length n. The last batch may be shorter."
        # batched('ABCDEFG', 3) --> ABC DEF G
        if n < 1:
            raise ValueError('n must be at least one')
        it = iter(iterable)
        while batch := tuple(islice(it, n)):
            yield batch

    # Check if files are trashed
    # Returns a dictionary of hash : trashed_or_not
    def is_files_trashed_hydrus(self, file_hashes: list[str]) -> dict:
        videos_metadata = self.client.get_file_metadata(hashes=file_hashes, only_return_basic_information=False)[
            "metadata"
        ]

        result = {}
        for video_metadata in videos_metadata:
            video_hash = video_metadata['hash']
            is_trashed = video_metadata['is_trashed']
            is_deleted = video_metadata['is_deleted']
            result[video_hash] = is_trashed or is_deleted
        return result

    # Delete trashed and deleted files from Hydrus from the database
    def clear_trashed_files_from_db(self):
        if not database_accessible(DEDUP_DATABASE_FILE, tablename="videos"):
            return

        try:
            CHUNK_SIZE = 32
            delete_count = 0
            with SqliteDict(str(DEDUP_DATABASE_FILE), tablename="videos", flag="c") as hashdb:
                for batched_keys in self.batched(hashdb, CHUNK_SIZE):
                    is_trashed_result = self.is_files_trashed_hydrus(batched_keys)
                    for result in is_trashed_result.items():
                        if result[1] is True:
                            del hashdb[result[0]]
                            delete_count += 1
                    hashdb.commit()
            self.hydlog.info(f"Cleared {delete_count} trashed files from the database.")
        except OSError:
            rprint("[red] Error while clearing trashed files cache.")
