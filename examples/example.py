from dappier.dappier import DappierApp


def main():
    # Initialize the DappierApp with your API key
    app = DappierApp(api_key="your-api-key")

    # Example 1: Perform a real-time search
    try:
        realtime_result = app.realtime_search_api("When is the next election?")
        print("Real-Time Search Results:", realtime_result.response['response']["results"])
    except Exception as e:
        print(f"Error during real-time search: {e}")

    # Example 2: AI Recommendations with default options
    try:
        ai_result = app.ai_recommendations(query="latest tech news", datamodel_id="dm_02hr75e8ate6adr15hjrf3ikol")
        print("AI Recommendations (default options):", ai_result.results)
    except Exception as e:
        print(f"Error during AI recommendations: {e}")

    # Example 3: AI Recommendations with custom options
    try:
        ai_custom_result = app.ai_recommendations(
            query="latest tech news",
            datamodel_id="dm_02hr75e8ate6adr15hjrf3ikol",
            similarity_top_k=5,
            ref="techcrunch.com",
            num_articles_ref=2
        )
        print("AI Recommendations (custom options):", ai_custom_result.results)
    except Exception as e:
        print(f"Error during custom AI recommendations: {e}")


if __name__ == "__main__":
    main()
