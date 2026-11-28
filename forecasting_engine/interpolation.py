import heapq

class KDNode:
    """Used to store data points in a KD-Tree"""
    def __init__(self, point: tuple, index: int, axis: int, right: KDNode=None, left: KDNode=None):
        self.point = point
        self.index = index
        self.axis = axis
        self.right = right
        self.left = left

def build_kdtree(points: list[tuple], indices: list[int], depth: int=0) -> KDNode:
    """Recursively builds a KD-Tree for IDW interpolation.

        :points: 2D-cordinates (x, y) of a point in a list.
        :indices: Index of each point, or node_id in the WeatherNode class.
        :depth: Current recursion depth.
    """
    # When we reach the base case (the end of a branch)
    if len(indices) == 0:
        return None

    # We only use 2 dimensions, longditude & latitude.
    # Find the current axis to split by (x or y) by depth MODULO 2 (Dimension)
    axis = depth % 2

    # Sort points by their axis
    indices.sort(key=lambda i: points[i][axis])

    # Find the median of the points
    median_pos = len(indices) // 2
    median_index = indices[median_pos]

    # Build right and left KD-tree branches via recursion
    left = build_kdtree(points, indices[:median_pos], depth + 1)
    right = build_kdtree(points, indices[median_pos+1:], depth + 1)

    return KDNode(
        point=points[median_index],
        index=median_index,
        axis=axis,
        right=right,
        left=left
    )

def calculate_square_distance(a: float, b: float)-> float:
    """Calculates the squared distance between two points a & b. We use squared distance
        to remove the need of math.sqrt() calls when only comparisons between the distances
        are needed.
    """
    distance_x = (b[0] - a[0]) ** 2
    distance_y = (b[1] - a[1]) ** 2
    return distance_x + distance_y

def query_nearest_points(tree: KDNode, target: tuple, k: int=1) -> list[tuple]:
    """Returns the k nearest points to a target from a KD-Tree.
    
        :tree: The KD-Tree being queried
        :target: The target point 
        :k: Amount of points needed

        :Returns: [(distance, index), ... ] for k points
    """
    heap = []

    def search_node(node: KDNode) -> None:
        # When we reach the root of a KD-Tree
        if node is None:
            return None

        # Calculates distance between the current node and target
        distance = calculate_square_distance(target, node.point)

        # Store the k closest candidates in a max-heap
        # We use the negation of the distance so the heap functions as intended
        entry = (-distance, -node.index)

        if len(heap) < k:
            heapq.heappush(heap, entry)
        elif entry > heap[0]:
            heapq.heapreplace(heap, entry)

        # Determine which side of the split target lies on
        axis = node.axis
        difference = target[axis] - node.point[axis]

        if difference <= 0:
            near_branch = node.left
            far_branch = node.right
        else:
            near_branch = node.right
            far_branch = node.left

    search_node(tree)

    # Convert heap back to positive distances and sort
    results = [
        (-distance, -index)
        for distance, index in heap
    ]

    results.sort(key=lambda x: x[0])

    return results