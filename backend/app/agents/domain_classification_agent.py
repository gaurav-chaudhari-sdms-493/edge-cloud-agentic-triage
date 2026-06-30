from app.agents.base import AgentState
import logging

# Global instance of the classifier, to be initialized lazily.
classifier = None
CLASSIFIER_AVAILABLE = False

def initialize_classifier():
    """Initializes the zero-shot classification pipeline if it hasn't been already."""
    global classifier, CLASSIFIER_AVAILABLE
    if classifier is None:
        try:
            from transformers import pipeline
            logging.info("Initializing zero-shot classification pipeline...")
            # Using a CPU-based pipeline to avoid issues with Celery and GPU memory.
            classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=-1)
            CLASSIFIER_AVAILABLE = True
            logging.info("Zero-shot classification pipeline initialized successfully.")
        except ImportError:
            logging.error("The 'transformers' library is not installed. Domain classification is unavailable.")
            classifier = None
            CLASSIFIER_AVAILABLE = False
        except Exception as e:
            logging.error(f"Failed to load zero-shot model: {e}")
            classifier = None
            CLASSIFIER_AVAILABLE = False

class DomainClassificationAgent:
    """
    Classifies the domain of the input text using a zero-shot learning model
    to determine if the content is related to healthcare.
    """
    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "domain_classification"
        state.execution_path.append("domain_classification")

        # Initialize the classifier on the first run in this process.
        initialize_classifier()

        if not CLASSIFIER_AVAILABLE:
            state.validation_errors.append("Domain classification model is not available or failed to load.")
            state.route = "validation_failed"
            return state

        input_text = state.content
        # The model works best with text that isn't excessively long.
        # We truncate to the first 512 characters for performance and accuracy.
        truncated_text = input_text[:512]
        candidate_labels = ["healthcare"] # We only care about the score for this label
        
        try:
            # We can ask the model to check for multiple labels and not assume they are mutually exclusive
            result = classifier(truncated_text, candidate_labels, multi_label=True)
            
            healthcare_score = result['scores'][0]

            logging.info(f"Domain classification result: Label={result['labels'][0]}, Score={healthcare_score}")

            # If the model is more than 50% confident, we classify it as healthcare.
            if healthcare_score > 0.50:
                state.domain = "healthcare"
                state.supported_domain = True
                state.domain_confidence = healthcare_score
            else:
                state.domain = "other"
                state.supported_domain = False
                state.domain_confidence = 1 - healthcare_score # Confidence in it being "other"
                state.route = "out_of_domain"
                state.output = "The provided text is not related to healthcare and is considered out of scope for this service."

        except Exception as e:
            error_message = f"Domain classification using the model failed: {e}"
            logging.error(error_message)
            state.validation_errors.append(error_message)
            state.route = "validation_failed"

        return state