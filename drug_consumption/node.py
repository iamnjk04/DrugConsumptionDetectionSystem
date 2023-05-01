class Node:
    def __init__(self, feature=None, threshold=None, left_node=None, right_node=None, *, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left_node = left_node
        self.right_node = right_node
        self.value = value
    def is_leaf(self):
        return self.value is not None