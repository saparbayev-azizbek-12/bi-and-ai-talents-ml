import numpy as np


class DecisionTreeClassifierCustom:
    def __init__(self, max_depth=None, min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.tree = None
        self.n_classes_ = 3


    def _gini(self, y):
        # y: [0, 0, 0, 1, 1, 2, 1, 0]
        _, counts = np.unique(y, return_counts=True)
        probs = counts / counts.sum()
        return 1 - np.sum(probs**2)
    
    def _best_split(self, X, y):
        best_gain = -1
        split_idx = None
        split_threshold = None

        child_gini = 0
        parent_gini = self._gini(y)
        n_features = X.shape[1]

        for feature in range(n_features):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                left_mask = X[:, feature] <= threshold
                right_mask = ~left_mask

                if left_mask.sum() < self.min_samples_split  or right_mask.sum() < self.min_samples_split:
                    continue

                left_gini = self._gini(y[left_mask])
                right_gini = self._gini(y[right_mask])

                # Weighted average gini
                n = y.shape[0]
                child_gini = (left_mask.sum() / n) * left_gini + (right_mask.sum() / n) * right_gini

                gain = parent_gini - child_gini

                if gain > best_gain:
                    best_gain = gain
                    split_idx = feature
                    split_threshold = threshold

        return split_idx, split_threshold, best_gain, child_gini
    

    def _build_tree(self, X, y, depth=0):
        """
        This is recursive function to build tree.
        """
        num_samples = X.shape[0]
        num_classes = len(np.unique(y))
        values = np.bincount(y, minlength=self.n_classes_)

        # Find best split
        feature_idx, threshold, gain, gini = self._best_split(X, y)

        # Stop condition
        if (
            (self.max_depth and depth >= self.max_depth) or
            num_classes == 1 or
            num_samples < self.min_samples_split
        ):
            leaf_value = np.bincount(y).argmax()
            return {
                "leaf": True,
                "class": leaf_value,
                "gini": gini,
                "samples": num_samples,
                "values": values.tolist()
            }
        

        if gain <= 0:
            leaf_value = np.bincount(y).argmax()
            return {
                "leaf": True,
                "class": leaf_value,
                "gini": gini,
                "samples": num_samples,
                "values": values.tolist()
            }
        
        # Split
        left_mask = X[:, feature_idx] <= threshold
        right_mask = ~left_mask

        left_subtree = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right_subtree = self._build_tree(X[right_mask], y[right_mask], depth + 1)

        return {
            "leaf": False,
            "feature": feature_idx,
            "threshold": threshold,
            "left": left_subtree,
            "right": right_subtree,
            "gini": gini,
            "samples": num_samples,
            "values": values.tolist()
        }


    def fit(self, X, y):
        X = np.array(X)
        y = np.array(y)

        self.tree = self._build_tree(X, y)


    # This is also recursive function
    def _predict_one(self, x, tree):
        if tree["leaf"]:
            return tree["class"]
        if x[tree['feature']] <= tree['threshold']:
            return self._predict_one(x, tree['left'])
        else:
            return self._predict_one(x, tree['right'])

    def predict(self, X):
        return np.array([self._predict_one(x, self.tree) for x in np.array(X)])
