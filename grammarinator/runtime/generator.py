# Copyright (c) 2017-2022 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import logging

from math import inf

from .default_model import DefaultModel

logger = logging.getLogger(__name__)


def depthcontrol(fn):
    def controlled_fn(obj, *args, **kwargs):
        obj._max_depth -= 1
        try:
            result = fn(obj, *args, **kwargs)
        finally:
            obj._max_depth += 1
        return result

    controlled_fn.__name__ = fn.__name__
    return controlled_fn


class Generator(object):

    def __init__(self, *, model=None, max_depth=inf):
        self._model = model or DefaultModel()
        self._max_depth = max_depth
        self._listeners = []

    def _enter_rule(self, node):
        for listener in self._listeners:
            listener.enter_rule(node)

    def _exit_rule(self, node):
        for listener in reversed(self._listeners):
            listener.exit_rule(node)

    def _filter_options(self, depths, weights):
        available_options = [w if depths[i] <= self._max_depth else 0 for i, w in enumerate(weights)]
        if sum(available_options) > 0:
            return available_options, self._max_depth
        max_depth = min(depths[i] if w > 0 else inf for i, w in enumerate(weights))
        logger.debug('max_depth must be temporarily set from %s to %s', self._max_depth, max_depth)
        return [w if depths[i] <= max_depth else 0 for i, w in enumerate(weights)], max_depth
