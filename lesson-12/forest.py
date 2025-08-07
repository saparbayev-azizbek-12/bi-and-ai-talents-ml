import numpy as np
from collections import Counter
from sklearn.tree import DecisionTreeClassifier

class RandomForestClassifier:
    def __init__(self, n_eliminators, max_depth, min_samples_split: int|None=None):
        self.n_eliminators = n_eliminators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.trees = []

    def fit(self, X, y):
        n_samples = X.shape[0]
        indices = np.random.choice(n_samples, n_samples, replace=True)
        X_sample = X[indices]
        y_sample = y[indices]

        for _ in range(self.n_eliminators):
            tree = DecisionTreeClassifier(max_depth=self.max_depth)
            tree.fit(X_sample, y_sample)
            self.trees.append(tree)

    def predict(self, X, y):
        trees = np.array([tree.predict(X) for tree in self.trees])
        preds = []
        for i in trees.T:
            preds.append(Counter(i).most_common(1)[0][0])
        return preds
    
X = np.array([[0,0], [0,1], [1,0], [1, 1], [0.9, 0.7], [0.1, 0.2]])
y = np.array([0, 1, 1, 1, 1, 0])

clf = RandomForestClassifier(n_eliminators=3, max_depth=3)
clf.fit(X, y)
print(clf.predict(X, y))