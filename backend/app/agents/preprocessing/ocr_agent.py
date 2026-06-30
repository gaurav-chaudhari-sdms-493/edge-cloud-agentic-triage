import os
from app.agents.base import AgentState
import easyocr
import logging

# Global instance of the reader, to be initialized lazily in each worker process.
reader = None
EASYOCR_AVAILABLE = False

def initialize_reader():
    """Initializes the EasyOCR reader if it hasn't been already."""
    global reader, EASYOCR_AVAILABLE
    if reader is None:
        try:
            # Initialize for English, Hindi, and Marathi.
            # Explicitly disable GPU to avoid potential hangs in a CPU-only environment.
            logging.info("Initializing EasyOCR reader...")
            reader = easyocr.Reader(['en', 'hi', 'mr'], gpu=False)
            EASYOCR_AVAILABLE = True
            logging.info("EasyOCR reader initialized successfully.")
        except Exception as e:
            logging.error(f"EasyOCR failed to initialize: {e}. OCR functionality will be unavailable.")
            reader = None
            EASYOCR_AVAILABLE = False

class OCRAgent:
    """
    Extracts text from an image using EasyOCR, a free and offline OCR library
    that supports multiple languages (including Hindi and Marathi) and handwritten text.
    This agent only runs if the input_type is 'image'. The extracted text then
    replaces the image path in state.content for downstream processing.
    """

    def run(self, state: AgentState) -> AgentState:
        # This agent only runs for image inputs.
        if state.input_type != "image":
            return state

        state.current_agent = "ocr"
        state.execution_path.append("ocr")

        # Initialize the reader on the first run in this process.
        initialize_reader()

        if not EASYOCR_AVAILABLE:
            state.validation_errors.append("EasyOCR is not installed or failed to initialize on the server.")
            return state

        image_path = state.content
        if not os.path.exists(image_path):
            state.validation_errors.append(f"OCRAgent: Image path does not exist: {image_path}")
            return state

        try:
            logging.info(f"Performing OCR on image: {image_path}")
            # The reader.readtext method returns a list of tuples, where each tuple
            # contains the bounding box, the recognized text, and the confidence score.
            result = reader.readtext(image_path)
            
            # We are interested in the text, so we extract it from the result.
            extracted_text = "\\n".join([text for _, text, _ in result])

            if not extracted_text or not extracted_text.strip():
                state.validation_errors.append("EasyOCR failed to extract any text from the image.")
            else:
                # The extracted text now becomes the main content for the rest of the pipeline
                state.content = extracted_text
                logging.warning("--- OCR Agent: Extracted Text ---")
                logging.warning(extracted_text)
                logging.warning("---------------------------------")
            logging.info("OCR processing finished.")

        except Exception as e:
            error_message = f"EasyOCR failed: {e}"
            state.validation_errors.append(error_message)
            logging.error(error_message)

        return state
