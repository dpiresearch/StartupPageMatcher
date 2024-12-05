from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st
from utils import preprocess_text

class PaperProcessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
    
    def process_papers(self, papers):
        """
        Process papers using TF-IDF vectorization
        """
        processed_papers = []
        
        # Prepare texts for vectorization
        texts = [f"{paper['title']} {paper['abstract']}" for paper in papers]
        preprocessed_texts = [preprocess_text(text) for text in texts]
        
        # Fit and transform the texts
        vectors = self.vectorizer.fit_transform(preprocessed_texts)
        
        # Get the TextMatcher instance from main and set its vectorizer
        matcher = st.session_state.get('matcher')
        if matcher:
            matcher.set_vectorizer(self.vectorizer)
        
        for paper, vector in zip(papers, vectors):
            # Add processed information to paper
            processed_paper = {
                **paper,
                'processed_text': vector
            }
            processed_papers.append(processed_paper)
        
        return processed_papers