# GAEL SYSTEMS CONFIDENTIAL
# __________________
#
# 2023 GAEL SYSTEMS
# All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of GAEL SYSTEMS,
# if any.  The intellectual and technical concepts contained
# herein are proprietary to GAEL SYSTEMS
# and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from GAEL SYSTEMS.
import logging
import io
import os
import time

from drb.core import DrbNode

from pygssearch.destination.writer import FileWriter
from pygssearch.progress.process_manager import ManagedPoolExecutor
from pygssearch.progress.tdqm_progress_manager import \
    progress_chunk_handling, append_progress
from pygssearch.utility import slice_file

logger = logging.getLogger("pygssearch")


@progress_chunk_handling
def handler(node: DrbNode, start: int, stop: int, filename: str,
            writer: FileWriter, **kwargs):
    """
    Handler dedicated to downlaod chunks

    :param node:
    :param start:
    :param stop:
    :param filename:
    :param writer:
    :param checksum:
    :return:
    """
    buff = node.get_impl(io.BytesIO, start=start, end=stop - start).read()
    # open the file and write the content of the download
    writer.write(buff, start)

    return filename, start, stop, writer


class Download:
    """
    This class is used to handle the download of product after
    being initialized, you can submit each product to be
    downloaded to the pool.
    """
    def __init__(self, output_folder: str = '.',
                 threads: int = 2, chunk_size: int = 4194304,
                 verify=False, quiet=False, fail_fast=False):
        self._bars = {}
        self._output_folder = output_folder
        self._threads = threads
        self._chunk_size = chunk_size
        self._verify = verify
        self._quiet = quiet
        self._executor = ManagedPoolExecutor(
            max_workers=self._threads,
            fail_fast=fail_fast
        )

    def stop(self):
        if self._executor is not None:
            self._executor.shutdown(wait=True)
        self._executor = None

    def submit(self, node: DrbNode):
        file_size = node @ 'ContentLength'

        # prepare writer
        writer = FileWriter(
            out_path=os.path.join(self._output_folder, node.name),
            file_size=file_size
        )

        # prepare chunk list
        chunks = slice_file(file_size, self._chunk_size)

        # checksum
        if self._verify:
            checksum = node @ 'Checksum'
            content_checksum = checksum[0]['Value']
        else:
            content_checksum = None

        if not self._quiet:
            append_progress(node.name, file_size)

        for chunk in chunks:
            self._executor.submit(
                handler, node=node, start=chunk.start, stop=chunk.end,
                filename=node.name, writer=writer, checksum=content_checksum,
                size=file_size, quiet=self._quiet
            )

    def join(self):
        while not self._executor.done():
            time.sleep(1)

    def collect_exceptions(self):
        return self._executor.get_exceptions()
