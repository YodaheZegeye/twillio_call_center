from flask import Flask, request, send_from_directory, jsonify
from flask_sock import Sock
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Start, Stream
import os
from dotenv import load_dotenv
from state_machine import CallStateMachine

load_dotenv()
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')
TARGET_NUMBER = os.getenv('TARGET_NUMBER')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')

client = Client(TWILIO_SID, TWILIO_TOKEN)
app = Flask(__name__, static_folder='../client/build', static_url_path='/')
sock = Sock(app)

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/call', methods=['POST'])
def initiate_call():
    data = request.json
    call = client.calls.create(
        to=TARGET_NUMBER,
        from_=TWILIO_NUMBER,
        url=f"{request.url_root}webhook/outbound?user={data['user']}"
    )
    return jsonify({'callSid': call.sid}), 200

@app.route('/webhook/outbound', methods=['POST'])
def twilio_webhook():
    user_json = request.args.get('user')
    # you add the user data from the session here (something to do later if we have time)
    user_data = json.loads(user_json)
    resp = VoiceResponse()
    start = Start()
    start.stream(url=f"wss://{request.host}/stream?user={user_json}")
    resp.append(start)
    return str(resp)

# WebSocket for media stream
@sock.route('/stream')
def stream(ws):
    user_json = request.args.get('user')
    user_data = json.loads(user_json)
    fsm = CallStateMachine(user_data)

    # Send greeting
    greeting = fsm.next(None)
    ws.send(json.dumps({ 'type': 'status', 'text': 'Greeting sent' }))
    ws.send(json.dumps({ 'type': 'transcript', 'text': greeting }))

    while True:
        message = ws.receive()
        if message is None:
            break
        # here you would decode the Twilio media payload and run ASR
        # for demo, treat incoming `message` as the agent's question text
        reply = fsm.next(message)
        if reply:
            ws.send(json.dumps({ 'type': 'status', 'text': f'Injecting {fsm.step}' }))
            ws.send(json.dumps({ 'type': 'transcript', 'text': reply }))
        if fsm.step == 'SUMMARY':
            bullets = fsm.summary_bullets()
            ws.send(json.dumps({ 'type': 'summary', 'bullets': bullets }))
            break

    ws.close()

if __name__ == '__main__':
    app.run(host=os.getenv('HOST', '0.0.0.0'), port=int(os.getenv('PORT', 5000)))