from gargant.dispatch.matching import (
    method_matching,
    path_matching,
    NotMetched,
)


def node(case_name, *matching):
    def _dispatch(condition):
        matched = map(lambda x: x(condition), matching)
        if all(matched):
            return case_name, matched
        else:
            return None, None
    return _dispatch


def dispatcher_factory(tree):
    def _dispatcher(condition):
        for node in tree:
            tree_or_leaf, matched = node(condition)
            if tree_or_leaf:
                if isinstance(tree_or_leaf, str):
                    return tree_or_leaf, matched
                else:
                    return _dispatcher(condition)
            else:
                continue
        else:
            raise NotMetched
    return _dispatcher
