import streamlit as st
import plotly.express as px
from arxiv_fetcher import ArxivFetcher
from paper_processor import PaperProcessor
from text_matcher import TextMatcher
from visualizations import create_category_chart, create_relevance_chart
from utils import preprocess_text

st.set_page_config(
    page_title="Startup-Paper Matcher",
    page_icon="📚",
    layout="wide"
)

# Initialize components
@st.cache_resource
def init_components():
    return ArxivFetcher(), PaperProcessor(), TextMatcher()

arxiv_fetcher, paper_processor, matcher = init_components()
st.session_state['matcher'] = matcher

# Page Header
st.title("📚 Startup-Paper Matcher")
st.markdown("""
Find relevant academic papers for your startup from arXiv's extensive collection.
Enter your startup's details below to discover papers that align with your business model.
""")

# Sidebar for startup profile input
st.sidebar.header("Startup Profile")

company_name = st.sidebar.text_input("Company Name")
business_model = st.sidebar.text_area("Business Model Description")
industry = st.sidebar.selectbox(
    "Industry",
    ["AI/ML", "Biotechnology", "Clean Energy", "Fintech", "Healthcare", "Robotics", "Other"]
)
keywords = st.sidebar.text_input("Keywords (comma-separated)")

# Main content area
if st.sidebar.button("Find Relevant Papers") and business_model:
    with st.spinner("Processing your request..."):
        # Prepare search query
        search_query = preprocess_text(f"{business_model} {keywords}")
        
        # Fetch papers
        papers = arxiv_fetcher.fetch_papers(search_query)
        
        # Process and match papers
        processed_papers = paper_processor.process_papers(papers)
        matched_papers = matcher.match_papers(processed_papers, business_model)
        
        # Display results
        st.header("📑 Matching Papers")
        
        # Create two columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            for paper in matched_papers[:10]:
                with st.expander(f"📄 {paper['title']} (Relevance: {paper['relevance']:.2f})"):
                    st.markdown(f"**Authors:** {paper['authors']}")
                    st.markdown(f"**Published:** {paper['published']}")
                    st.markdown(f"**Abstract:** {paper['abstract']}")
                    st.markdown(f"**arXiv URL:** [{paper['id']}](https://arxiv.org/abs/{paper['id']})")
        
        with col2:
            st.subheader("📊 Paper Statistics")
            
            # Create and display visualizations
            category_fig = create_category_chart(matched_papers)
            st.plotly_chart(category_fig, use_container_width=True)
            
            relevance_fig = create_relevance_chart(matched_papers)
            st.plotly_chart(relevance_fig, use_container_width=True)
else:
    st.info("👈 Please enter your startup's details in the sidebar and click 'Find Relevant Papers'")
