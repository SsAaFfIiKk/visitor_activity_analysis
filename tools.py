import random


class Img:
    img_bytes: None
    predict: None


def generate_predict():
    labels = ["laptop", "smartphone", "paper", "talking", "nothing"]
    index = random.randrange(0, len(labels))
    return labels[index]
