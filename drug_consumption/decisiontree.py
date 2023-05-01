import numpy as np
from node import Node


class DecisionTree:
    def __init__(self, max_depth=100, min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None

    def _is_finished(self, dt_depth):
        if (dt_depth >= self.max_depth or self.n_class_labels == 1 or self.n_samples < self.min_samples_split):
            return True
        return False
    
    def _entropy(self, y):
        proportions = np.bincount(y) / len(y)
        entropy = -np.sum([p * np.log2(p) for p in proportions if p > 0])
        return entropy

    def _create_split(self, X, threshold):
        left_indx = np.argwhere(X <= threshold).flatten()
        right_indx = np.argwhere(X > threshold).flatten()
        return left_indx, right_indx

    def _info_gain(self, X, y, threshold):
        parent_loss = self._entropy(y)
        left_indx, right_indx = self._create_split(X, threshold)
        n, no_left, no_right = len(y), len(left_indx), len(right_indx)

        if no_left == 0 or no_right == 0: 
            return 0
        
        child_loss = (no_left / n) * self._entropy(y[left_indx]) + (no_right / n) * self._entropy(y[right_indx])
        return parent_loss - child_loss

    def _best_split(self, X, y, features):
        split = {'score':- 1, 'feat': None, 'threshold': None}

        for feat in features:
            X_feat = X[:, feat]
            thresholds = np.unique(X_feat)
            for threshold in thresholds:
                score = self._info_gain(X_feat, y, threshold)

                if score > split['score']:
                    split['score'] = score
                    split['feat'] = feat
                    split['threshold'] = threshold

        return split['feat'], split['threshold']
    
    def _build_tree(self, X, y, dt_depth=0):
        self.n_samples, self.n_features = X.shape
        self.n_class_labels = len(np.unique(y))

    
        if self._is_finished(dt_depth):
            most_common_Label = np.argmax(np.bincount(y))
            return Node(value=most_common_Label)

        
        random_feats = np.random.choice(self.n_features, self.n_features, replace=False)
        best_feat, best_threshold = self._best_split(X, y, random_feats)

        
        left_indx, right_indx = self._create_split(X[:, best_feat], best_threshold)
        left_child = self._build_tree(X[left_indx, :], y[left_indx], dt_depth + 1)
        right_child = self._build_tree(X[right_indx, :], y[right_indx], dt_depth + 1)
        return Node(best_feat, best_threshold, left_child, right_child)
    
    def _traverse_tree(self, x, node):
        if node.is_leaf():
            return node.value
        
        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right)

    def fit(self, X, y):
        self.root = self._build_tree(X, y)

    def predict(self, X):
        predictions = [self._traverse_tree(x, self.root) for x in X]
        return np.array(predictions)