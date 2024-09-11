# Jellyseer Twilio Webhook

This application is a simple Python web application that provides a webhook endpoint to use with Jellyseer so that you can recieve a text message when a new request is created in Jellyseer.

## Requirements

You will require a [Twilio](https://login.twilio.com/u/signup) account with a phone number that can send SMS messages in order to use this application.

## Usage

Add the following to your `docker-compose.yml` file for your Jellystack setup:

```yaml
jellyseer-twilio-webhook:
  image: ghcr.io/dobsondev/jellyseer-twilio-webhook:latest
  container_name: jellyseer-twilio-webhook
  environment:
    - TWILIO_ACCOUNT_SID=YOUR_TWILIO_ACCOUNT_SID
    - TWILIO_AUTH_TOKEN=YOUR_TWILIO_AUTH_TOKEN
    - TWILIO_PHONE_NUMBER=YOUR_TWILIO_PHONE_NUMBER
    - ADMIN_PHONE_NUMBER=YOUR_ADMIN_PHONE_NUMBER
    - AUTH_HEADER=YOUR_AUTH_HEADER_KEY
  ports:
    - "5050:5000"
  restart: unless-stopped
```

## Local Development Quick Start

Copy the contents of `.env.sample` to `.env` and fill out the appropriate values. This will be used by the `docker-compose.yml` file to generate all the required environment variables. Then simply run the following commands:

```bash
docker compose build --no-cache
docker compose up -d
```