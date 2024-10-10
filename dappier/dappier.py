import requests
import json

# Constants for the API
BASE_URL = "https://api.dappier.com/app/datamodel"
CONTENT_TYPE = "application/json"

# SearchRequest represents the request payload structure for the Dappier Search API
class SearchRequest:
    def __init__(self, query, similarity_top_k=9, ref="", num_articles_ref=0):
        self.query = query  # Natural language query or URL
        self.similarity_top_k = similarity_top_k  # Number of articles to return (default is 9)
        self.ref = ref  # Domain from which to fetch recommendations (e.g., techcrunch.com)
        self.num_articles_ref = num_articles_ref  # Guaranteed number of articles from the specified domain


# SearchResult represents the response structure for the Dappier Search API
class SearchResult:
    def __init__(self, results, status):
        self.results = results
        self.status = status


# DappierApp manages API interaction with optional configurations
class DappierApp:
    def __init__(self, api_key, base_url=None, session=None):
        if not api_key:
            raise ValueError("API key cannot be empty")
        self.api_key = api_key
        self.base_url = base_url or BASE_URL
        self.session = session or requests.Session()

    # RealtimeSearchAPI makes a request to the Dappier API for real-time data retrieval
    def realtime_search_api(self, query):
        if not query:
            raise ValueError("query cannot be empty")

        # Create request payload
        request_data = {"query": query}
        headers = {
            "Content-Type": CONTENT_TYPE,
            "Authorization": f"Bearer {self.api_key}",
        }

        # Make the HTTP request
        response = self.session.post(self.base_url, json=request_data, headers=headers)

        # Handle the response
        if response.status_code != 200:
            raise Exception(f"Received non-OK response status: {response.status_code}")

        data = response.json()
        if not data:
            raise ValueError("No results found")

        return RealtimeSearchResult(response=data[0])

    # AIRecommendations makes a request to the Dappier API for AI recommendations
    def ai_recommendations(self, query, datamodel_id, similarity_top_k=9, ref="", num_articles_ref=0):
        if not query:
            raise ValueError("query cannot be empty")
        if not datamodel_id:
            raise ValueError("datamodelID cannot be empty")

        # Create the request payload
        request_data = {
            "query": query,
            "similarity_top_k": similarity_top_k,
            "ref": ref,
            "num_articles_ref": num_articles_ref
        }

        url = f"{self.base_url}/{datamodel_id}"
        headers = {
            "Content-Type": CONTENT_TYPE,
            "Authorization": f"Bearer {self.api_key}",
        }

        # Make the HTTP request
        response = self.session.post(url, json=request_data, headers=headers)

        # Handle the response
        if response.status_code != 200:
            raise Exception(f"Received non-OK response status: {response.status_code}")

        data = response.json()
        if not data:
            raise ValueError("No results found")

        return AiRecommendationsResult(results=data)

    # Search makes a request to the Dappier Search API with a provided data model ID
    def search(self, query, datamodel_id, similarity_top_k=9, ref="", num_articles_ref=0):
        if not query:
            raise ValueError("query cannot be empty")
        if not datamodel_id:
            raise ValueError("datamodelID cannot be empty")

        # Create the request payload
        request_data = {
            "query": query,
            "similarity_top_k": similarity_top_k,
            "ref": ref,
            "num_articles_ref": num_articles_ref
        }

        url = f"https://api.dappier.com/app/v2/search?data_model_id={datamodel_id}"
        headers = {
            "Content-Type": CONTENT_TYPE,
            "Authorization": f"Bearer {self.api_key}",
        }

        # Make the HTTP request
        response = self.session.post(url, json=request_data, headers=headers)

        # Handle the response
        if response.status_code != 200:
            raise Exception(f"Received non-OK response status: {response.status_code}")

        data = response.json()
        if not data:
            raise ValueError("No results found")

        return SearchResult(results=data.get("response", {}).get("results"), status=data.get("status"))

