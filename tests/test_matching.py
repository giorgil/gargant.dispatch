import pytest
from wsgiref.util import setup_testing_defaults


def get_dummy_environ(base_environ={}):
    environ = base_environ
    setup_testing_defaults(environ)
    return environ


class TestMethodMatching(object):
    @pytest.fixture
    def target(self):
        from gargant.dispatch.matching import method_matching
        return method_matching

    def test_matched(self, target):
        environ = get_dummy_environ()
        assert target('get')(environ)

    def test_not_matched(self, target):
        environ = get_dummy_environ()
        assert not target('post')(environ)


def get_path_list(environ):
    from gargant.dispatch.matching import ENVIRON_PATH_MATCHING_LIST_NAME
    return environ.get(ENVIRON_PATH_MATCHING_LIST_NAME)


class TestPathMatching(object):
    @pytest.fixture
    def target(self):
        from gargant.dispatch.matching import path_matching
        return path_matching

    def test_matched(self, target):
        environ = get_dummy_environ()
        assert target(['', ''])(environ)
        assert get_path_list(environ) == []

    def test_matched_child(self, target):
        environ = get_dummy_environ({'PATH_INFO': '/members/ritsu'})
        assert target(['', 'members'])(environ)
        assert get_path_list(environ) == ['ritsu']

    def test_not_matched(self, target):
        environ = get_dummy_environ({'PATH_INFO': '/members'})
        assert not target(['', 'instruments'])(environ)

    def test_with_path_list(self, target):
        from gargant.dispatch.matching import ENVIRON_PATH_MATCHING_LIST_NAME
        environ = get_dummy_environ({ENVIRON_PATH_MATCHING_LIST_NAME: ['members', 'ritsu']})
        assert target(['members', 'ritsu'])(environ)

    def test_path_list_too_short(self, target):
        environ = get_dummy_environ({'PATH_INFO': '/members'})
        assert not target(['', 'members', 'ritsu'])(environ)

    def test_with_matching_pattern(self, target):
        environ = get_dummy_environ({'PATH_INFO': '/members/ritsu'})
        actual = target(['', 'members', '{member}'])(environ)
        assert actual == {'member': 'ritsu',
                          'matching_list': ['', 'members', '{member}']}
