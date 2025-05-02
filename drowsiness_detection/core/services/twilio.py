import logging

from django.conf import settings
from requests import ConnectTimeout, HTTPError, ConnectionError, exceptions
from twilio.rest import Client

log = logging.getLogger()


def send_whatsapp(msg: str, receiveNumber: str) -> dict:
    sid = settings.TWILIO_SID
    authToken = settings.TWILIO_AUTH_TOKEN
    client = Client(sid, authToken)

    message = None
    try:
      # TODO: run in background
      message = client.messages.create(
          from_ = f'whatsapp:{settings.TWILIO_WA_NUMBER}',
          body = msg,
          to = f'whatsapp:{receiveNumber}'
      )
    except (ConnectTimeout, HTTPError, ConnectionError, exceptions.Timeout) as exc:
        log.info(f"Twilio Error | {message} ")

    return message
