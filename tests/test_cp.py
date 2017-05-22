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

import pytest

import mir.cp


def _count():
    x = 0

    def count_func(self):
        nonlocal x
        x += 1
        return x
    return count_func


@pytest.mark.parametrize('impl_class,args,kwargs', [
    (mir.cp.NonDataCachedProperty, (), dict(fget=_count(), name='foo')),
    (mir.cp.WeakRefCachedProperty, (), dict(fget=_count())),
])
def test_impl(impl_class, args, kwargs):
    """Test a cached property implementation for basic behavior."""
    impl = impl_class(*args, **kwargs)
    instance = _make_test_class(impl)()
    assert instance.foo == 1
    assert instance.foo == 1
    del instance.foo
    assert instance.foo == 2


@pytest.mark.parametrize('impl_class,args,kwargs', [
    (mir.cp.NonDataCachedProperty, (), dict(fget=_count(), name='foo')),
    (mir.cp.WeakRefCachedProperty, (), dict(fget=_count())),
])
def test_class_access(impl_class, args, kwargs):
    impl = impl_class(*args, **kwargs)
    cls = _make_test_class(impl)
    assert cls.foo is impl


def test_nondata_default_name():
    fget = _count()
    fget.__name__ = 'foo'
    impl = mir.cp.NonDataCachedProperty(fget)
    instance = _make_test_class(impl)()
    assert instance.foo == 1
    assert instance.foo == 1
    del instance.foo
    assert instance.foo == 2


def _make_test_class(descriptor):
    """Make an instance using the given cached property implementation."""
    return type('TestClass', (), {'foo': descriptor})
