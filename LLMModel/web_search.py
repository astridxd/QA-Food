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

def web_search(question):
    results = []
    for result in search(question, num_results=2):
        results.append(result + ":\n" + _fetch_main_content(result))
    
    return "\n".join(results)
