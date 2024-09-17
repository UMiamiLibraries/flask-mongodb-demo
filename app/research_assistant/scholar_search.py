from scholarly import scholarly, ProxyGenerator

def initialize_proxy():
    pg = ProxyGenerator()
    pg.FreeProxies()
    success = scholarly.use_proxy(pg)
    if not success:
        print("Failed to initialize proxy. Searches may be limited.")
    return success

def search_google_scholar(query, num_results=10):
    if not hasattr(search_google_scholar, "proxy_initialized"):
        search_google_scholar.proxy_initialized = initialize_proxy()

    results = []
    try:
        search_query = scholarly.search_pubs(query)
        for i in range(num_results):
            try:
                publication = next(search_query)
                results.append({
                    'title': publication['bib'].get('title', 'N/A'),
                    'author': publication['bib'].get('author', 'N/A'),
                    'year': publication['bib'].get('pub_year', 'N/A'),
                    'url': publication.get('pub_url', 'N/A')
                })
            except StopIteration:
                break
    except Exception as e:
        print(f"An error occurred while searching: {str(e)}")

    return results