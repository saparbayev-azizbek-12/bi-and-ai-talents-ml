from pathlib import Path
import joblib, numpy as np
from PIL import Image, ImageOps


clf = joblib.load("source/digit_clf.joblib")

def to_array(img_path):
    img = Image.open(img_path).convert("L")
    if np.mean(img) > 127:
        img = ImageOps.invert(img)
    img = img.resize((28, 28))
    arr = np.asarray(img, dtype="float32") / 255.0
    return arr.reshape(1, -1)

def digit_pred(img_path):
    image_path = Path(img_path)
    X_img = to_array(image_path)
    pred = int(clf.predict(X_img)[0])
    conf = clf.predict_proba(X_img)[0][pred]
    return pred, conf

digit, conf = digit_pred("images/3_1.png")
print(f"Prediction: {digit}, (confidence {conf:.2%})")