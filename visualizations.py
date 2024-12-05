import plotly.express as px
from collections import Counter

def create_category_chart(papers):
    """
    Create a bar chart of paper categories
    """
    # Flatten categories list
    all_categories = [cat for paper in papers for cat in paper['categories']]
    category_counts = Counter(all_categories)
    
    # Create bar chart
    fig = px.bar(
        x=list(category_counts.keys()),
        y=list(category_counts.values()),
        title="Paper Categories Distribution",
        labels={'x': 'Category', 'y': 'Count'},
        color_discrete_sequence=['#1f77b4']
    )
    
    fig.update_layout(
        showlegend=False,
        xaxis_tickangle=-45
    )
    
    return fig

def create_relevance_chart(papers):
    """
    Create a line chart of paper relevance scores
    """
    relevance_scores = [paper['relevance'] for paper in papers[:10]]
    paper_titles = [paper['title'][:30] + '...' for paper in papers[:10]]
    
    fig = px.line(
        x=paper_titles,
        y=relevance_scores,
        title="Paper Relevance Scores",
        labels={'x': 'Paper', 'y': 'Relevance Score'},
        markers=True
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    return fig
