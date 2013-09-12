import pytest


@pytest.fixture
def target():
    from gargant.dispatch import Node
    return Node


@pytest.fixture
def true_matching():
    return lambda x: True


@pytest.fixture
def false_matching():
    return lambda x: False


def test_create_tree(target, true_matching):
    child1 = target((true_matching,))
    child2 = target((true_matching,))
    parent = target(
        (true_matching,),
        children=(
            child1,
            child2,
        ))
    assert child1 in parent.children
    assert child2 in parent.children
    assert parent == child1.parent
    assert parent == child2.parent


def test_not_matched(target, false_matching):
    from gargant.dispatch import NotMatched
    with pytest.raises(NotMatched):
        target((false_matching,))({})


def test_matched(target, true_matching):
    node = target((true_matching,))
    actual = node({})
    assert actual == node
    assert actual.matched == [True]
    assert actual.adapter(True) is True


def test_matched_parent(target, true_matching, false_matching):
    child = target((false_matching,))
    parent = target(
        (true_matching,),
        children=(
            child,
        ))
    assert parent({}) == parent


def test_matched_child(target, true_matching):
    child = target((true_matching,))
    parent = target(
        (true_matching,),
        children=(
            child,
        ))
    actual = parent({})
    assert actual == child


def test_iter(target):
    node = target(tuple())
    assert iter(node) == node


def test_next(target):
    granchild = target(tuple())
    child = target(tuple(),
                   children=(
                       granchild,
                   ))
    parent = target(tuple(),
                    children=(
                        child,
                    ))
    assert granchild == next(granchild)
    assert child == next(granchild)
    assert parent == next(granchild)
    with pytest.raises(StopIteration):
        granchild.next()
