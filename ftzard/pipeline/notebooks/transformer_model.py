# transformer_model.py
from transformers import AutoModelForSequenceClassification
from mlflow.pyfunc import PythonModel
class TransformerModel(PythonModel):
    def __init__(self, model):
        self.model = model

    def predict(self, inputs):
        return self.model(**inputs)
