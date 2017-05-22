# Copyright (C) 2017 Allen Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Cached property implementations."""

__version__ = '0.1.0'


class NonDataCachedProperty:

    """Cached property implemented as a non-data descriptor.

    The value is cached on the instance property with the same name as
    the descriptor.

    `fget` is a function for getting the attribute value.  `name` is the
    attribute name to use for caching the value, defaulting to the name
    of the `fget` function.

    The arguments are also exposed as instance attributes with the same
    name as the parameters.
    """

    def __init__(self, fget, name=None):
        self.fget = fget
        if name is None:
            self.name = self.fget.__name__
        else:
            self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self.fget(instance)
        setattr(instance, self.name, value)
        return value
