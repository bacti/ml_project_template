"""
This file combine all model's predictor to make final predictor for project
"""
from model.ocr.predictor import OCRModule
import os

class ModelPredictor(object):
    def __init__(self, **kwargs):
        folder = os.path.dirname(os.path.abspath(__file__))
        weights_path = os.path.join(folder, 'weights/serving_model.pth')
        vocab_path = os.path.join(folder, 'weights/vocab.json')
        self.ocr_module = OCRModule(weights_path = weights_path, vocab_path = vocab_path)

    def predict(self, image):
        return self.ocr_module.process(image)
