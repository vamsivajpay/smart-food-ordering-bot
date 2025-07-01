from flask import Flask, request, jsonify
import requests
 
def hello_http(request):
    try:
        # Parse the incoming JSON request
        req_data = request.get_json()
        print("Request data:", req_data)
 
        # Extract order_number from session parameters
        order_number = req_data.get("sessionInfo", {}).get("parameters", {}).get("order_number")
        print("Order number:", order_number)

        # Validate and convert order_number to an integer
        if order_number is None:
            return jsonify({"fulfillment_response": {"messages": [{"text": {"text": ["Error: No order number provided."]}}]}}), 400
 
        try:
            order_number = int(order_number)
        except ValueError:
            return jsonify({"fulfillment_response": {"messages": [{"text": {"text": ["Error: Invalid order number format."]}}]}}), 400

            

        # Call the external API to fetch order details
        api_url = "https://ca58c33c3c01741c76b7.free.beeceptor.com/api/users/"
        response = requests.get(api_url)
        response.raise_for_status()
        print("API response status:", response.status_code)
 
        data = response.json()  # Expecting a list of order records
        print("API response data:", data)
 
        # Find the record matching the order_number
        matched_order = next((item for item in data if item.get("id") == order_number), None)
        print("Matched order:", matched_order)
 
        # Prepare the fulfillment response
         
        if matched_order:
            response_text = (
                f"Order Details:\n"
                f"ID: {matched_order['id']}\n"
                f"Name: {matched_order['name']}\n"
                f"Items: {matched_order['items']}\n"
                f"Quantity:{matched_order['quantity']}\n"
                f"Address: {matched_order['address']}\n"
                f"Payment Mode: {matched_order['modeof_payment']}\n\n"
                "Kindly specify the reason for cancellation."
            )
       
            # Attempt to cancel the order via DELETE request
            delete_url = f"{api_url}{order_number}"
            requests.delete(delete_url)
        else:
            response_text = "No matching order found.Please enter valid order number."
 
        print("Response text:", response_text)
 
        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": [response_text]
                        }
                    }
                ]
            }
        })
 
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"fulfillment_response": {"messages": [{"text": {"text": [f"Error processing request: {str(e)}"]}}]}}), 500
