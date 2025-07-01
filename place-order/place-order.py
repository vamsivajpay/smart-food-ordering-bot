import json
import requests

def handle_webhook_request(request):
    # Parse the incoming JSON request
    request_data = request.get_json()

    # Extract fulfillment info and tag
    fulfillment_info = request_data.get("fulfillmentInfo", {})
    session_info = request_data.get("sessionInfo", {})
    tag = fulfillment_info.get("tag", "")

    # Placeholder API URL - users should replace this with their actual endpoint
    API_URL = "https://your-api-endpoint.com/api/items/"

    # Check for the specific intent tag
    if tag == "get_food_items":
        try:
            response = requests.get(API_URL, timeout=5)
            response.raise_for_status()  # Raise an error for HTTP issues
            food_items = response.json()  # Convert response to JSON

            if not isinstance(food_items, list):
                text = "Invalid response from API."
            else:
                # Format food items into a readable list
                text = "Available food items:\n" + "\n".join(
                    [f"{item.get('name', 'Unknown')}" for item in food_items]
                )
        except requests.exceptions.RequestException as e:
            text = f"Error fetching food items: {str(e)}"
    else:
        text = "Welcome! How can I help you?"

    # Construct the response with chips
    # NOTE: Image URLs are intentionally left blank.
    # Users should add their own image links to enhance the chatbot's visual experience.
    # Without images, the chips will still display text but won't show any visuals.
    response = {
        "fulfillment_response": {
            "messages": [
                {
                    "payload": {
                        "richContent": [
                            [
                                {
                                    "type": "chips",
                                    "options": [
                                        {
                                            "text": "🍕 Pizza",
                                            "image": {
                                                "src": {
                                                    "rawUrl": ""  # Add your image URL here
                                                }
                                            }
                                        },
                                        {
                                            "text": "🍔 Burger",
                                            "image": {
                                                "src": {
                                                    "rawUrl": ""  # Add your image URL here
                                                }
                                            }
                                        },
                                        {
                                            "text": "🥤 Coke",
                                            "image": {
                                                "src": {
                                                    "rawUrl": ""  # Add your image URL here
                                                }
                                            }
                                        },
                                        {
                                            "text": "🍟 Fries",
                                            "image": {
                                                "src": {
                                                    "rawUrl": ""  # Add your image URL here
                                                }
                                            }
                                        },
                                        {
                                            "text": "🍝 Pasta",
                                            "image": {
                                                "src": {
                                                    "rawUrl": ""  # Add your image URL here
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        ]
                    }
                }
            ]
        }
    }

    return json.dumps(response)
