"""
t = lambda condition: True
f = lambda condition: False

tree = Node((t,),
            children=[
                Node((t,),
                     case='posts',
                     name='posts',
                     children=[
                         Node((f,),
                              case='post_detail',
                              name='post_detail',
                              ),
                         Node((t,),
                              case='post_create',
                              name='post_create'
                              ),
                     ]),
                Node((f,),
                     case='about',
                     name='about'),
            ])
"""
from gargant.dispatch.matching import (
    method_matching,
    path_matching,
)


class NotMatched(Exception):
    pass


class Node(object):
    def __init__(self, matchings, case=None, name='', children=[]):
        self.matchings = matchings
        self.case = case
        self.name = name
        self.children = children
        self.parent = None
        for child in self.children:
            child.parent = self

    def __call__(self, condition):
        self.matched = map(lambda x: x(condition), self.matchings)
        if all(self.matched):
            if self.children:
                for node in self.children:
                    try:
                        return node(condition)
                    except NotMatched:
                        continue
            return self
        raise NotMatched

    def __iter__(self):
        return self

    def next(self):
        if not hasattr(self, '_processing_node'):
            self._processing_node = self
        else:
            self._processing_node = self._processing_node.parent
        if self._processing_node:
            return self._processing_node
        else:
            raise StopIteration
