from transformers import AutoTokenizer, AutoModelForSequenceClassification
from flask import current_app
import torch

class MLService:
    def __init__(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(current_app.config['HUGGINGFACE_MODEL'])
            self.model = AutoModelForSequenceClassification.from_pretrained(
                current_app.config['HUGGINGFACE_MODEL']
            )
        except Exception as e:
            current_app.logger.error(f"Failed to initialize ML models: {str(e)}")
            self.tokenizer = None
            self.model = None

    def analyze_vulnerability(self, code_snippet):
        inputs = self.tokenizer(code_snippet, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        return self._process_predictions(predictions)

    def _process_predictions(self, predictions):
        vulnerability_types = ['sql_injection', 'xss', 'csrf', 'rce']
        scores = predictions[0].tolist()
        return {
            vuln_type: score 
            for vuln_type, score in zip(vulnerability_types, scores)
        }
