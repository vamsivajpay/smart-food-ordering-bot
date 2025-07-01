import requests
from flask import jsonify

# URL for the Orders API (replace with the actual API endpoint)
ORDERS_API_URL = "https://cad8ba970a3a8cf7ea0d.free.beeceptor.com/api/users/"

# Variables to store order details
order_details = {"name": "", "address": "", "modeof_payment": ""}

# Main webhook handler
def webhook_handler(request):
    try:
        req = request.get_json()
        print("Request payload:", req)
        # Extract parameters safely
        order_no = req.get("sessionInfo", {}).get("parameters", {}).get("order_no", None)
        item_name = req.get("sessionInfo", {}).get("parameters", {}).get("item_name", None)
        quantity_item = req.get("sessionInfo", {}).get("parameters", {}).get("quantity_item", None)
        tag = req.get("fulfillmentInfo", {}).get("tag", None)
        print(f"Order number: {order_no}, Tag: {tag}")
        # Validate order_no, item, and quantity for update_order
        if tag == "update_order" and (not item_name or not quantity_item):
            return jsonify({
                "fulfillment_response": {
                    "messages": [
                        {"text": {"text": ["Order number, item name, and quantity are required to update the order."]}}
                    ]
                }
            })
        # Route based on tag
        if tag == "update_order":
            return update_order(order_no, item_name, quantity_item)
        elif tag == "validate_order":
            return validate_order(order_no)
        else:
            return jsonify({
                "fulfillment_response": {
                    "messages": [
                        {"text": {"text": ["Invalid request. Please check your request and try again."]}}
                    ]
                }
            })
    except Exception as e:
        print("Error handling request:", str(e))
        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": ["An unexpected error occurred. Please try again later."]}}
                ]
            }
        })

# Webhook 1: Validate Order
def validate_order(order_no):
    global order_details
    try:
        # Fetch order details from Orders API
        response = requests.get(f"{ORDERS_API_URL}{order_no}")
        if response.status_code == 200:
            order_data = response.json()
            print(f"Order found: {order_data}")
            # Store order details in the global variable
            order_details["name"] = order_data.get("name", "")
            order_details["address"] = order_data.get("address", "")
            order_details["modeof_payment"] = order_data.get("modeof_payment", "")
            print(order_details["name"], order_details["address"], order_details["modeof_payment"])
            # If order found, ask for item name and quantity
            return jsonify({
                "fulfillment_response": {
                    "messages": [
                        {"text": {"text": [f"Hey {order_details['name']}, you have ordered {order_data['quantity']} {order_data['items']}(s), please update your order accordingly."]}}
                    ]
                }
            })
        else:
            # Order not found or invalid
            return jsonify({
                "fulfillment_response": {
                    "messages": [
                        {"text": {"text": ["Unable to fetch your order. Please provide a valid order number."]}}
                    ]
                },
                "sessionInfo": {
                    "parameters": {
                        "order_no": "null",
                    },
                }
            })
    except Exception as e:
        print(f"Error validating order: {str(e)}")
        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": ["An error occurred while validating your order."]}}
                ]
            }
        })

# Webhook 2: Update Order
def update_order(order_no, item_name, quantity_item):
    global order_details
    try:
        # Prepare data for update
        update_data = {
            "id": order_no,
            "name": order_details["name"],
            "items": item_name,
            "quantity": quantity_item,
            "address": order_details["address"],
            "modeof_payment": order_details["modeof_payment"]
        }
        print(update_data)
        # Send PUT request to update order
        response = requests.put(f"{ORDERS_API_URL}{order_no}", json=update_data)
        if response.status_code == 200:
            return jsonify({
                "fulfillment_response": {
                    "messages": [
                        {"text": {"text": ["Your order has been successfully updated."]}}
                    ]
                }
            })
        else:
            return jsonify({
                "fulfillment_response": {
                    "messages": [
                        {"text": {"text": ["Unable to update the order. Please try again later."]}}
                    ]
                }
            })
    except Exception as e:
        print(f"Error updating order: {str(e)}")
        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": ["An error occurred while updating your order."]}}
                ]
            }
        })

# Function entry point for Cloud Run
def hello_http(request):
    return webhook_handler(request)
