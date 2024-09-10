import os, json, logging, traceback 

from flask import Flask, request, jsonify 
from twilio.rest import Client

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_client = Client(account_sid, auth_token)

twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
admin_phone_number = os.getenv("ADMIN_PHONE_NUMBER")

api_key = os.getenv("API_KEY") 

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_authorization_header(headers):
    headers = request.headers
    auth = headers.get("Authorization")
    
    if auth == api_key:
        return True
    else:
        return False

@app.route("/", methods=['GET'])
def health_check():
    return jsonify({"status": "Ok"}), 200

@app.route("/auth-test", methods=["GET"])
def authorization_test():
    if check_authorization_header(request.headers):
        return jsonify({"status": "Ok"}), 200
    else:
        return jsonify({"error": "Unauthorized"}), 401

@app.route("/webhook", methods=['POST'])
def txt_message_notification():
    if check_authorization_header(request.headers) == False:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.get_json()
        logger.info(request.headers)
        logger.info(data)
        
        notification_type = data.get("notification_type")

        if notification_type == "TEST_NOTIFICATION":
            return jsonify({"status": "Ok"}), 200

        if notification_type == "MEDIA_PENDING":
            event = data.get("event")
            subject = data.get("subject")
            requested_by = data.get("request").get("requestedBy_username")
            message_to_send = f"{event} - {subject}. Requested by {requested_by}."

            twilio_message = twilio_client.messages.create(
                body=message_to_send,
                from_=twilio_phone_number,
                to=admin_phone_number
            )

            return jsonify({
                "status": "Ok",
                "message": "Twilio message sent successfully.",
                "twilio": {
                    "message": message_to_send,
                    "sid": twilio_message.sid
                }
            }), 200

        return jsonify({"message": "Notification type not supported"}), 204

    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
