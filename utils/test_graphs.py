import dataclasses
import typing
import unittest

from utils.graphs.structures import DirectedGraph, DirectedAcyclicGraph, Tree, List, Set, Ordering


class TestStructures(unittest.TestCase):
    @dataclasses.dataclass
    class TestCase:
        label: str
        graph: dict[str, set[str]]
        groups: set[frozenset[str]]
        orders: dict[str, int]
        valid_structures: set[typing.Type[DirectedGraph]]
    
    TEST_CASES = [
        TestCase(
            label="disconnected nodes", graph={'A': set(), 'B': set()},
            groups={frozenset({'A'}), frozenset({'B'})},
            orders={'A': 0, 'B': 0},
            valid_structures={Set, List, Tree, DirectedAcyclicGraph, DirectedGraph},
        ),
        TestCase(
            label="linear chain",
            graph={'A': {'B'}, 'B': {'C'}, 'C': set()},
            groups={frozenset({'A'}), frozenset({'C'}), frozenset({'B'})},
            orders={'A': 2, 'B': 1, 'C': 0},
            valid_structures={List, Tree, DirectedAcyclicGraph, DirectedGraph},
        ),
        TestCase(
            label="tree",
            graph={'A': {'B', 'C'}, 'B': {}, 'C': {}},
            groups={frozenset({'A'}), frozenset({'B'}), frozenset({'C'})},
            orders={'A': 1, 'B': 0, 'C': 0},
            valid_structures={Tree, DirectedAcyclicGraph, DirectedGraph},
        ),
        TestCase(
            label="inverted tree",
            graph={'A': {'C'}, 'B': {'C'}, 'C': set()},
            groups={frozenset({'C'}), frozenset({'B'}), frozenset({'A'})},
            orders={'A': 1, 'B': 1, 'C': 0},
            valid_structures={DirectedAcyclicGraph, DirectedGraph},
        ),
        TestCase(
            label="diamond",
            graph={'A': {'B', 'C'}, 'B': {'D'}, 'C': {'D'}, 'D': set()},
            groups={frozenset({'B'}), frozenset({'A'}), frozenset({'C'}), frozenset({'D'})},
            orders={'A': 2, 'B': 1, 'C': 1, 'D': 0},
            valid_structures={DirectedAcyclicGraph, DirectedGraph},
        ),
        TestCase(
            label="self-loop",
            graph={'A': {'A'}},
            groups={frozenset({'A'})},
            orders={'A': 0},
            valid_structures={DirectedGraph},
        ),
        TestCase(
            label="2-node cycle",
            graph={'A': {'B'}, 'B': {'A'}},
            groups={frozenset({'B', 'A'})},
            orders={'A': 0, 'B': 0},
            valid_structures={DirectedGraph},
        ),
        TestCase(
            label="3-node cycle",
            graph={'A': {'B'}, 'B': {'C'}, 'C': {'A'}},
            groups={frozenset({'A', 'B', 'C'})},
            orders={'A': 0, 'B': 0, 'C': 0},
            valid_structures={DirectedGraph},
        ),
        TestCase(
            label="2-node & 3-node cycles",
            graph={'A': {'B'}, 'B': {'C'}, 'C': {'A'}, 'E': {'F'}, 'F': {'E'}},
            groups={frozenset({'E', 'F'}), frozenset({'A', 'B', 'C'})},
            orders={'A': 0, 'B': 0, 'C': 0, 'E': 0, 'F': 0},
            valid_structures={DirectedGraph},
        ),
        TestCase(
            label="complex",
            graph={'A': {'B'}, 'B': {'C'}, 'C': {'A'}, 'D': {'E'}, 'E': {'C'}},
            groups={frozenset({'D'}), frozenset({'A', 'B', 'C'}), frozenset({'E'})},
            orders={'A': 0, 'B': 0, 'C': 0, 'D': 2, 'E': 1},
            valid_structures={DirectedGraph},
        ),
    ]
    
    def test(self):
        for test_case in self.TEST_CASES:
            with self.subTest(msg=test_case.label):
                ordering = Ordering(test_case.graph)
                self.assertEqual(test_case.groups, ordering.clusters)
                for node in test_case.graph:
                    self.assertEqual(test_case.orders[node], ordering.get_node_order(node))
                
                DirectedGraph.from_dict(test_case.graph)

                for structure in [Set, List, Tree, DirectedAcyclicGraph, DirectedGraph]:
                    with self.subTest(msg=f"{test_case.label} with {structure.__name__}"):
                        if structure in test_case.valid_structures:
                            structure.from_dict(test_case.graph)
                        else:
                            self.assertRaises(Exception, structure.from_dict, test_case.graph)
                

if __name__ == '__main__':
    unittest.main()
