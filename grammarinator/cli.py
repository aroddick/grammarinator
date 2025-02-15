# Copyright (c) 2020-2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import logging
import os

logger = logging.getLogger('grammarinator')


def init_logging():
    logging.basicConfig(format='%(message)s')


def add_jobs_argument(parser):
    parser.add_argument('-j', '--jobs', metavar='NUM', type=int, default=os.cpu_count(),
                        help='parallelization level (default: number of cpu cores (%(default)d)).')


def add_disable_cleanup_argument(parser):
    parser.add_argument('--disable-cleanup', dest='cleanup', default=True, action='store_false',
                        help='disable the removal of intermediate files.')
