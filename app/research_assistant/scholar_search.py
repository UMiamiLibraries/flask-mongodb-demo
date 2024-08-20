from scholarly import scholarly

def search_google_scholar(query, num_results=10):
    search_query = scholarly.search_pubs(query)
    results = []
    try:
        for i in range(num_results):
            publication = next(search_query)
            results.append({
                'title': publication['bib'].get('title', 'N/A'),
                'author': publication['bib'].get('author', 'N/A'),
                'year': publication['bib'].get('pub_year', 'N/A'),
                'url': publication.get('pub_url', 'N/A')
            })
    except StopIteration:
        pass
    return results