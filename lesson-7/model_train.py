import joblib
from sklearn.datasets import fetch_openml
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

mnist = fetch_openml("mnist_784", version=1, as_frame=False)
X, y   = mnist.data, mnist.target.astype("int")

X = X.astype("float32") / 255.0

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# clf = MLPClassifier(hidden_layer_sizes=(100,), max_iter=70, alpha=1e-4,
#                     solver='sgd', verbose=10, random_state=1, learning_rate_init=.1)

clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print("Accurency Score:", accuracy_score(y_pred, y_test))

joblib.dump(clf,   "digit_clf.joblib")
