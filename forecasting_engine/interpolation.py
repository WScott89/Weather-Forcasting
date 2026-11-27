class KDNode:
    """Used to store data points in a KD-Tree"""
    def __init__(self, point, index, axis, right=None, left=None):
        self.point = point
        self.index = index
        self.axis = axis
        self.right = right
        self.left = left

def build_kd_tree(points, indices, depth=0):
    """Recursively builds a KD-Tree for IDW interpolation. S

        :points: 2D-cordinates (x, y) of a point in a list.
        :indices: Index of each point, or node_id in the WeatherNode class.
        :depth: Current recursion depth.
    """
    # When we reach the base case (the end of a branch)
    if len(indices) == 0:
        return None

    # We only use 2 dimensions, longditude & latitude.
    # Find the current axis to split by (x or y) by depth MODULO 2
    dimensions = 2
    axis = depth % dimensions

    # Sort points by their axis
    indices.sort(key=lambda i: points[i][axis])

    # Find the median of the points
    median_pos = len(indices) // 2
    median_index = indices[median_pos]

    # Build right and left KD-tree branches via recursion
    left = build_kd_tree(points, indices[:median_pos], depth + 1)
    right = build_kd_tree(points, indices[median_pos+1:], depth + 1)

    return KDNode(
        point=points[median_index],
        index=median_index,
        axis=axis,
        right=right,
        left=left
    )