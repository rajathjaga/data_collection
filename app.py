import os
import json
import psycopg2
import requests

# Database connection details
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_PORT = os.environ['DB_PORT']

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def send_slack_alert(message):
    payload = {"text": f"*Alert:* {message}"}
    requests.post(SLACK_WEBHOOK_URL, json=payload)

def lambda_handler(event, context):
    try:
        # Fetch ISS position data
        response = requests.get("http://api.open-notify.org/iss-now.json") #http://api.open-notify.org/iss-now.json
        data = response.json()

        if data.get("message") == "success":
            latitude = data["iss_position"]["latitude"]
            longitude = data["iss_position"]["longitude"]

            # Connect to PostgreSQL
            conn = psycopg2.connect(
                host=DB_HOST,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT
            )
            cur = conn.cursor()

            # Insert data into metrics table
            cur.execute("INSERT INTO metrics (latitude, longitude) VALUES (%s, %s)", (latitude, longitude))
            conn.commit()

            # Close connections
            cur.close()
            conn.close()

            return {
                'statusCode': 200,
                'body': json.dumps({"message": "Data inserted successfully", "latitude": latitude, "longitude": longitude})
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": "Failed to fetch ISS data"})
            }

    except Exception as e:
        send_slack_alert(f"Lambda failed: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }
