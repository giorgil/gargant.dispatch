from gargant.dispatch.matching import (
    method_matching,
    path_matching,
    NotMetched,
)


def node(case_name, *matching):
    def _dispatch(environ):
        matched = map(lambda x: x(environ), matching)
        if all(matched):
            return case_name, matched
        else:
            return None, None
    return _dispatch


def dispatcher_factory(tree):
    def _dispatcher(environ):
        for node in tree:
            tree_or_leaf, matched = node(environ)
            if tree_or_leaf:
                if isinstance(tree_or_leaf, str):
                    return tree_or_leaf, matched
                else:
                    return _dispatcher(environ)
            else:
                continue
        else:
            raise NotMetched
    return _dispatcher
