from wsgiref.util import setup_testing_defaults
import pytest


@pytest.fixture
def target():
    from gargant.dispatch import make_wsgi_app
    return make_wsgi_app

@pytest.fixture
def environ():
    environ = {}
    setup_testing_defaults(environ)
    return environ


def tree_factory(portal):
    from gargant.dispatch import Node

    def wsgi_app(start_response, environ):
        return start_response, environ

    def matching(environ):
        portal['environ'] = environ
        return True

    return Node((matching,),
                case=wsgi_app)


def test_it(target, environ):
    from gargant.dispatch import ENVIRON_MATCHED_NODE_NAME
    portal = {}
    tree = tree_factory(portal)
    actual = target(tree)
    assert actual('start_response', environ) == ('start_response', environ)
    assert portal['environ'] == environ
    assert environ[ENVIRON_MATCHED_NODE_NAME] == tree
