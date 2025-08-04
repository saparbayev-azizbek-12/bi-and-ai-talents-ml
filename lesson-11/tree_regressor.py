import numpy as np


class DecisionTreeRegressorCustom:
    def __init__(self, max_depth=None, min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.tree = None


    def _mse(self, y):
        # y: [0, 0, 0, 1, 1, 2, 1, 0]
        mean = np.mean(y)
        return np.mean((y - mean) ** 2)
    
    def _best_split(self, X, y):
        best_gain = -1
        split_idx = None
        split_threshold = None

        parent_mse = self._mse(y)
        n_features = X.shape[1]

        for feature in range(n_features):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                left_mask = X[:, feature] <= threshold
                right_mask = ~left_mask

                if left_mask.sum() < self.min_samples_split  or right_mask.sum() < self.min_samples_split:
                    continue

                left_mse = self._mse(y[left_mask])
                right_mse = self._mse(y[right_mask])

                # Weighted average mse
                n = y.shape[0]
                child_mse = (left_mask.sum() / n) * left_mse + (right_mask.sum() / n) * right_mse

                gain = parent_mse - child_mse

                if gain > best_gain:
                    best_gain = gain
                    split_idx = feature
                    split_threshold = threshold

        return split_idx, split_threshold, best_gain
    

    def _build_tree(self, X, y, depth=0):
        """
        This is recursive function to build tree.
        """
        num_samples = X.shape[0]
        num_classes = len(np.unique(y))

        # Stop condition
        if (
            (self.max_depth and depth >= self.max_depth) or
            num_classes == 1 or
            num_samples < self.min_samples_split
        ):
            leaf_value = np.mean(y)
            return {
                "leaf": True,
                "class": leaf_value
            }
        
        # Find best split
        feature_idx, threshold, gain = self._best_split(X, y)

        if gain <= 0:
            leaf_value = np.mean(y)
            return {
                "leaf": True,
                "class": leaf_value
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
            "right": right_subtree
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

# Predict
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeRegressor

iris = load_iris(as_frame=True)
X = iris.data[['petal length (cm)', 'petal width (cm)']] # type: ignore
y = iris.target # type: ignore


tree_clf = DecisionTreeRegressor(max_depth=3, random_state=42)
tree_clf.fit(X, y)

y.values
pred1 = tree_clf.predict(X)

tree_clf2 = DecisionTreeRegressorCustom(max_depth=3)
tree_clf2.fit(X, y)
pred2 = tree_clf2.predict(X)

# Calculate MSE
from sklearn.metrics import mean_squared_error

mse_sklearn = mean_squared_error(y, pred1)
mse_custom = mean_squared_error(y, pred2)

print("Sklearn Tree MSE:", mse_sklearn)
print("Custom Tree MSE:", mse_custom)

# tree = {
#     "leaf": False,
#     "left": {
#         "left": {
#             "leaf": True
#         },
#         "right": {
#             "leaf": False,

#         },
#     },
#     "right": {
#         "left": {},
#         "right": {}
#     }
# }