from predict import Classifier


predictor = Classifier()


class Img:
    img_bytes: None
    predict: None


def generate_predict(img):
    return predictor.res(img)
