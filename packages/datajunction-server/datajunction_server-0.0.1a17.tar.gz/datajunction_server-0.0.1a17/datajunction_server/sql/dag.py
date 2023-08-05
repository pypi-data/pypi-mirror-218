"""
DAG related functions.
"""
import collections
import itertools
from typing import Deque, Dict, List, Set, Tuple, Union

from datajunction_server.models import Column
from datajunction_server.models.node import DimensionAttributeOutput, Node, NodeType
from datajunction_server.utils import get_settings

settings = get_settings()


def get_dimensions(
    node: Node,
    attributes: bool = True,
) -> List[Union[DimensionAttributeOutput, Node]]:
    """
    Return all available dimensions for a given node.
    * Setting `attributes` to True will return a list of dimension attributes,
    * Setting `attributes` to False will return a list of dimension nodes
    """
    dimensions = []

    # Start with the node itself or the node's immediate parent if it's a metric node
    StateTrackingType = Tuple[Node, List[Column]]
    node_starting_state: StateTrackingType = (node, [])
    immediate_parent_starting_state: List[StateTrackingType] = [
        (parent, [])
        for parent in (node.current.parents if node.type == NodeType.METRIC else [])
    ]
    to_process: Deque[StateTrackingType] = collections.deque(
        [node_starting_state, *immediate_parent_starting_state],
    )
    processed: Set[Node] = set()

    while to_process:
        current_node, join_path = to_process.popleft()

        # Don't include attributes from deactivated dimensions
        if current_node.deactivated_at:
            continue
        processed.add(current_node)

        for column in current_node.current.columns:
            # Include the dimension if it's a column belonging to a dimension node
            # or if it's tagged with the dimension column attribute
            if (
                current_node.type == NodeType.DIMENSION
                or any(
                    attr.attribute_type.name == "dimension"
                    for attr in column.attributes
                )
                or column.dimension
            ):
                join_path_str = [
                    (
                        (
                            link_column.node_revisions[0].name + "."
                            if link_column.node_revisions
                            else ""
                        )
                        + link_column.name
                    )
                    for link_column in join_path
                    if link_column is not None and link_column.dimension
                ]
                dimensions.append(
                    DimensionAttributeOutput(
                        name=f"{current_node.name}.{column.name}",
                        type=column.type,
                        path=join_path_str,
                    ),
                )
            if column.dimension and column.dimension not in processed:
                to_process.append((column.dimension, join_path + [column]))
    if attributes:
        return sorted(dimensions, key=lambda x: x.name)
    return sorted(list(processed), key=lambda x: x.name)


def check_convergence(path1: List[str], path2: List[str]) -> bool:
    """
    Determines whether two join paths converge before we reach the
    final element, the dimension attribute.
    """
    if path1 == path2:
        return True
    len1 = len(path1)
    len2 = len(path2)
    min_len = min(len1, len2)

    for i in range(min_len):
        partial1 = path1[len1 - i - 1 :]
        partial2 = path2[len2 - i - 1 :]
        if partial1 == partial2:
            return True

    return False


def group_dimensions_by_name(node: Node) -> Dict[str, List[DimensionAttributeOutput]]:
    """
    Group the dimensions for the node by the dimension attribute name
    """
    return {
        k: list(v)
        for k, v in itertools.groupby(
            get_dimensions(node),
            key=lambda dim: dim.name,
        )
    }


def get_shared_dimensions(
    metric_nodes: List[Node],
) -> List[DimensionAttributeOutput]:
    """
    Return a list of dimensions that are common between the nodes.
    """
    common = group_dimensions_by_name(metric_nodes[0])
    for node in set(metric_nodes[1:]):
        node_dimensions = group_dimensions_by_name(node)

        # Merge each set of dimensions based on the name and path
        to_delete = set()
        common_dim_keys = common.keys() & list(node_dimensions.keys())
        for common_dim in common_dim_keys:
            for existing_attr in common[common_dim]:
                for new_attr in node_dimensions[common_dim]:
                    converged = check_convergence(existing_attr.path, new_attr.path)
                    if not converged:
                        to_delete.add(common_dim)

        for dim_key in to_delete:
            del common[dim_key]

    return sorted(
        [y for x in common.values() for y in x],
        key=lambda x: (x.name, x.path),
    )
