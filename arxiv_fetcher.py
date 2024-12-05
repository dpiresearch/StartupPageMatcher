import arxiv
import streamlit as st

class ArxivFetcher:
    def __init__(self):
        self.client = arxiv.Client()
    
    @st.cache_data(ttl=3600)
    def fetch_papers(_self, query: str, max_results: int = 50):
        """
        Fetch papers from arXiv based on the search query
        """
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        papers = []
        for result in _self.client.results(search):
            paper = {
                'id': result.get_short_id(),
                'title': result.title,
                'abstract': result.summary,
                'authors': ', '.join(author.name for author in result.authors),
                'categories': result.categories,
                'published': result.published.strftime("%Y-%m-%d"),
                'url': result.entry_id
            }
            papers.append(paper)
        
        return papers
