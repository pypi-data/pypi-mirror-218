#
# DATABRICKS CONFIDENTIAL & PROPRIETARY
# __________________
#
# Copyright 2020-present Databricks, Inc.
# All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains the property of Databricks, Inc.
# and its suppliers, if any.  The intellectual and technical concepts contained herein are
# proprietary to Databricks, Inc. and its suppliers and may be covered by U.S. and foreign Patents,
# patents in process, and are protected by trade secret and/or copyright law. Dissemination, use,
# or reproduction of this information is strictly forbidden unless prior written permission is
# obtained from Databricks, Inc.
#
# If you view or obtain a copy of this information and believe Databricks, Inc. may not have
# intended it to be made available, please promptly report it to Databricks Legal Department
# @ legal@databricks.com.
#


import functools


class HashableDict(dict):
    # Variation of dict which can be hashed
    # _hashable_dict must not be modified after it was hashed
    def __hash__(self):
        return hash(tuple((k, self[k]) for k in sorted(self.keys())))


def cached(map_args_to_cache_id):
    """
    Decorator to cache function results.

    Parameters
    ----------
    map_args_to_cache_id:
        function transforming arguments into cache id
        map_args_to_cache_id must return object suitable as a dict key
    """
    def _cached(func):
        cache = dict()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_id = map_args_to_cache_id(*args, **kwargs)
            if cache_id not in cache:
                cache[cache_id] = func(*args, **kwargs)
            return cache[cache_id]

        return wrapper

    return _cached
