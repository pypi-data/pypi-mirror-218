"""

画像が挿入されると、猫・ライオン・チーターを学習したCNNモデルをロードして.

与えられた画像に対しての予測結果を出力する.

"""


from tensorflow.keras.models import load_model  # type: ignore

classes = ["猫", "ライオン", "チーター"]


def predict(img):
    """
    モデルのロード
    """

    model = load_model("ai/catai_cnn_new.h5")
    result = model.predict([img])[0]
    predicted = result.argmax()
    return str(classes[predicted])
