import unittest

from balancer import NodesIterator, CallNode


class TestNodesIterator(unittest.TestCase):
    def test_iterator_over_each_node(self):
        nodes = [
            CallNode('a', 1, True),
            CallNode('b', 2, True),
            CallNode('c', 3, True),
        ]
        iterator = NodesIterator(nodes)
        self.assertEqual(iterator.next().name, 'a')
        self.assertEqual(iterator.next().name, 'b')
        self.assertEqual(iterator.next().name, 'c')

    def test_iterator_skips_unavailable_nodes(self):
        nodes = [
            CallNode('a', 1, False),
            CallNode('b', 2, True),
            CallNode('c', 3, False),
            CallNode('d', 4, True),
        ]
        iterator = NodesIterator(nodes)
        self.assertEqual(iterator.next().name, 'b')
        self.assertEqual(iterator.next().name, 'd')
