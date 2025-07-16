import os
import joblib

file_path = os.path.abspath(os.path.dirname(__file__))
clf = joblib.load(os.path.join(file_path, "digit_clf.joblib"))

def digit_pred(image):
    pred = int(clf.predict(image))
    conf = clf.predict_proba(image)[pred]
    print("prediction", pred)
    return pred, conf