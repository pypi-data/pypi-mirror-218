"""

画像が挿入されると、猫・ライオン・チーターを学習したCNNモデルをロードして.

与えられた画像に対しての予測結果を出力する.

"""

import os

from tensorflow.keras.models import load_model  # type: ignore

classes = ["猫", "ライオン", "チーター"]


def predict(img):
    """
    モデルのロード
    """

    file_path = "ai/catai_cnn_new.h5"
    if not os.path.isfile(file_path):
        file_path = "catai_cnn_new.h5"
    model = load_model(file_path)
    result = model.predict([img])[0]
    predicted = result.argmax()
    return str(classes[predicted])
