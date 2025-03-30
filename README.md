# Designing an Automatic Data Collection and Storage System with AWS Lambda and Slack Integration for Server Availability Monitoring and Slack Notification

## Overview
This project sets up an **AWS Lambda function** that:
- Fetches data from an external API.
- Stores data in an **Amazon RDS (PostgreSQL)** database.
- Uses **Amazon CloudWatch** to monitor errors.
- Sends alerts to **Slack** using a Webhook.

## Prerequisites
- **AWS Lambda** function.
- **Amazon RDS** PostgreSQL instance.
- **CloudWatch Alarm** to track errors.
- **Slack Webhook URL** (for notifications).

## Setup Instructions

### Create a Slack Webhook
1. Go to [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks).
2. Create a new **Incoming Webhook** for your Slack channel.
3. Copy the generated **Webhook URL**.

### Deploy AWS Lambda
1. Install the required dependencies:
   ```bash
   pip install psycopg2-binary requests -t .
   ```
2. Zip the files and upload them to AWS Lambda:
   ```bash
   zip -r lambda_function.zip .
   ```
3. Set up the **Lambda function** with Python 3.x runtime.

### Configure CloudWatch Alarm
1. Go to **AWS CloudWatch → Alarms → Create Alarm**.
2. Select **Metric:** `AWS/Lambda → Errors`.
3. Set **Threshold:** `Errors > 0`.
4. Set **Action:** Trigger your Lambda function.

## Conclusion
This setup ensures real-time monitoring of your Lambda function, with **automated Slack alerts** whenever failures occur.

