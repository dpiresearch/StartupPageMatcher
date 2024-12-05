import re
import string

def preprocess_text(text: str) -> str:
    """
    Preprocess text by removing special characters and normalizing
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and extra whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    return text.strip()
