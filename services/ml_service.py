import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from flask import current_app

class MLService:
    """
    Service class for managing machine learning tasks, such as analyzing code snippets for vulnerabilities using a pre-trained model.
    """
    def __init__(self):
        """
        Initializes the tokenizer and model from Hugging Face.
        Logs any errors encountered during initialization.
        """
        try:
            model_name = current_app.config['HUGGINGFACE_MODEL']
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            current_app.logger.info(f"Successfully loaded model: {model_name}")
        except Exception as e:
            current_app.logger.error(f"Failed to initialize ML models: {str(e)}")
            self.tokenizer = None
            self.model = None

    def analyze_vulnerability(self, code_snippet):
        """
        Analyzes a code snippet for vulnerabilities using the loaded model.
        Tokenizes the input and performs inference.
        Returns the processed prediction results as a dictionary.

        Args:
            code_snippet (str): The code snippet to analyze.

        Returns:
            dict: The processed prediction results.
        """
        if not self.tokenizer or not self.model:
            current_app.logger.error("Model or tokenizer not initialized. Cannot analyze vulnerability.")
            return {"error": "Model or tokenizer not initialized."}

        try:
            # Tokenize the input code snippet
            inputs = self.tokenizer(code_snippet, return_tensors="pt", truncation=True, max_length=512)
            if not inputs.get('input_ids'):
                current_app.logger.warning("Tokenization failed: Empty input_ids.")
                return {"error": "Failed to tokenize input."}

            # Perform model inference
            outputs = self.model(**inputs)
            if not hasattr(outputs, 'logits'):
                current_app.logger.warning("Model output missing 'logits'.")
                return {"error": "Model output is incomplete."}

            # Apply softmax to logits to get probabilities
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

            # Process the predictions
            return self._process_predictions(predictions)

        except Exception as e:
            current_app.logger.error(f"Error during vulnerability analysis: {str(e)}")
            return {"error": f"An error occurred during analysis: {str(e)}"}

    def _process_predictions(self, predictions):
        """
        Processes the raw predictions into a more readable format with vulnerability types.

        Args:
            predictions (torch.Tensor): The raw predictions from the model.

        Returns:
            dict: A dictionary of vulnerability types and their corresponding scores.
        """
        # Define possible vulnerability types corresponding to the model outputs
        vulnerability_types = ['sql_injection', 'xss', 'csrf', 'rce']

        # Convert the tensor to a list for easier processing
        scores = predictions[0].tolist()

        # Return a dictionary of vulnerability types and their corresponding scores
        return {
            vuln_type: score
            for vuln_type, score in zip(vulnerability_types, scores)
        }
