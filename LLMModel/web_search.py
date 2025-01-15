from googlesearch import search
from newspaper import Article

# Utility functions for doing a web search and returning the main contents of the articles found
def _fetch_main_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text 
    except Exception as e:
        return f"Failed to fetch content from {url}: {e}"

def web_search(question, max_words=400):
    results = []
    for result in search(question, num_results=2):
        # Fetch and process content with newlines
        content = " ".join(_fetch_main_content(result).split()[:max_words])
        formatted_result = f"{result}:\n{content}\n"  # Add newline at the end
        results.append(formatted_result)
    
    # Join results with an extra newline between entries
    return "\n\n".join(results)

