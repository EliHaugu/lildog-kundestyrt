from collections import defaultdict, deque
from typing import Any


class FlowParser:

    def __init__(self, flow: Any):
        self.flow = flow
        self.nodes = list(flow.nodes.all())
        self.edges = list(flow.edges.all())

        self.outgoing_edges = defaultdict(list)
        self.incoming_edges_counter = {node.id: 0 for node in self.nodes}

        for edge in self.edges:
            self.outgoing_edges[edge.source.id].append(edge.target.id)
            self.incoming_edges_counter[edge.target.id] += 1

    def get_start_node(self) -> int:
        """
        Find potential starting nodes (those with no incoming edges)
        and return the one with the largest reachable subgraph.
        """
        start_candidates = [
            node.id
            for node in self.nodes
            if self.incoming_edges_counter[node.id] == 0
        ]
        max_connected_nodes = 0
        best_start_node = None

        for node_id in start_candidates:
            connected_nodes = self.bfs_connected_count(node_id)
            if connected_nodes > max_connected_nodes:
                max_connected_nodes = connected_nodes
                best_start_node = node_id
            elif connected_nodes == max_connected_nodes:
                # Tiebreaker is smallest ID
                best_start_node = min(best_start_node, node_id)

        if best_start_node is None:
            raise ValueError(
                "No start node found. Check for cycles and missing edges."
            )

        return best_start_node

    def bfs_connected_count(self, start_node_id: int) -> int:
        """
        Count the number of nodes reachable from start_node_id using BFS.
        """
        visited = set()
        queue = deque([start_node_id])

        while queue:
            node_id = queue.popleft()
            if node_id not in visited:
                visited.add(node_id)
                for neighbor in self.outgoing_edges[node_id]:
                    if neighbor not in visited:
                        queue.append(neighbor)

        return len(visited)

    def get_execution_order(self) -> list[list[Any]]:
        """
        Perform a topological sort with Kahn's algorith,
        grouping nodes by levels to show parallelism, with cycle detection.

        :return: List[List[Node]] - A list of lists,
        where each sublist contains nodes that can be executed in parallel.
        """
        start_node_id = self.get_start_node()
        if not start_node_id:
            return []

        queue = deque([start_node_id])
        visited = set()
        level_order = []
        nodes_visited_count = 0

        while queue:
            level_size = len(queue)
            current_level = []

            for _ in range(level_size):
                node_id = queue.popleft()
                if node_id in visited:
                    continue

                visited.add(node_id)
                current_level.append(node_id)
                nodes_visited_count += 1

                for neighbor in self.outgoing_edges[node_id]:
                    self.incoming_edges_counter[neighbor] -= 1
                    if (
                        self.incoming_edges_counter[neighbor] == 0
                        and neighbor not in visited
                    ):
                        queue.append(neighbor)

            if current_level:
                level_order.append(current_level)

        ordered_nodes = [
            [self.flow.nodes.get(id=node_id) for node_id in level]
            for level in level_order
        ]
        return ordered_nodes
