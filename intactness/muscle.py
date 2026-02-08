#!/usr/bin/env python3
"""
multiple sequence alignment using muscle
"""

import logging
import os

from .utils import run_cmd


def muscle(configs):
    """Multiple sequence alignment using muscle
    """
    file_i = configs['file_seq']
    file_o = configs['file_aln']
    maxiters = configs['maxiters']
    logger = logging.getLogger(__name__)
    ...

    if os.path.exists(file_o):
        logger.info(f"Skipping MUSCLE: '{file_o}' already exists.")
        return

    logger.info(f"Running MUSCLE alignment: input={file_i}, output={file_o}")

    cmd = ['muscle', '-align', file_i, '-output', file_o]  #RD
    if maxiters:
        cmd.extend(['-maxiters', str(maxiters)])  #RD
    threads = configs.get('threads')  #RD
    if threads:
        cmd.extend(['-threads', str(threads)])  #RD
    run_cmd(cmd)
