from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import streamlit as st
from utils import preprocess_text

class TextMatcher:
    def __init__(self):
        self.vectorizer = None

    def set_vectorizer(self, vectorizer):
        self.vectorizer = vectorizer
    
    def match_papers(self, papers, business_description):
        """
        Match papers with business description using TF-IDF and cosine similarity
        """
        # Process business description
        processed_desc = self.vectorizer.transform([preprocess_text(business_description)])
        
        matched_papers = []
        for paper in papers:
            # Calculate similarity score
            similarity = cosine_similarity(
                processed_desc,
                paper['processed_text']
            )[0][0]
            
            # Add similarity score to paper
            matched_paper = {
                **paper,
                'relevance': float(similarity)  # Convert to float for JSON serialization
            }
            matched_papers.append(matched_paper)
        
        # Sort papers by relevance
        matched_papers.sort(key=lambda x: x['relevance'], reverse=True)
        
        return matched_papers
