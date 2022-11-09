from flask import Flask, json, Response, jsonify, request, session
from flask_cors import CORS

import uuid
from square.client import Client
import os

from twilio.twiml.voice_response import VoiceResponse, Say, Gather
import requests


app = Flask(__name__)
CORS(app)
app.secret_key = '2abceVR5ENE7FgMxXdMwuzUJKC2g8xgy'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/v1/twilio/<api_key>', methods=['POST'])
def twilioResponse(api_key):
    voice_response = VoiceResponse()
    action_url = f"https://311b-50-88-215-98.ngrok.io/v1/twilio/{api_key}"
    call_id = request.form.get("CallSid")

    text = request.form.get("SpeechResult")
    if text == None:
        text = 'Hello'
    print(text)

    body = {"request": {"type": "text", "payload": text}}
    response = requests.post(
        f"https://general-runtime.voiceflow.com/state/user/{call_id}/interact",
        json=body,
        headers={"Authorization": api_key},
    )
    req_json = response.json()
    for response in req_json:
        try:
            voice_response.say(response['payload']['message'])
        except:
            pass

    gather = Gather(
        input="speech",
        action=action_url,
        actionOnEmptyResult=True,
        speechTimeout=0,
        speechModel='phone_call',
        enhanced=True,
    )
    voice_response.append(gather)
    return Response(str(voice_response), mimetype="text/xml")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)