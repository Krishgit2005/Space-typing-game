import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import json
import uuid

BASE_URL = 'http://127.0.0.1:5000'

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)

username = f'testuser_{uuid.uuid4().hex[:6]}'
password = 'password123'

print(f"Registering as {username}...")
data = urllib.parse.urlencode({'username': username, 'password': password}).encode('utf-8')
req = urllib.request.Request(f'{BASE_URL}/register', data=data)
try:
    with urllib.request.urlopen(req) as response:
        print(f"Register status: {response.status}")
except urllib.error.HTTPError as e:
    print(f"Register err status: {e.code}")

print(f"Logging in as {username}...")
req = urllib.request.Request(f'{BASE_URL}/login', data=data)
try:
    with urllib.request.urlopen(req) as response:
        print(f"Login status: {response.status}")
except urllib.error.HTTPError as e:
    print(f"Login err status: {e.code}")

print(f"Cookies: {[c.name+'='+c.value for c in cj]}")

score = 50
print(f"Submitting a high score of {score}...")
req = urllib.request.Request(f'{BASE_URL}/submit_score', data=json.dumps({'score': score}).encode('utf-8'))
req.add_header('Content-Type', 'application/json')
try:
    with urllib.request.urlopen(req) as response:
        print(f"Submit score status: {response.status}")
        print(f"Submit score response: {response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    print(f"Submit score err status: {e.code}")

print("Fetching leaderboard...")
req = urllib.request.Request(f'{BASE_URL}/leaderboard')
try:
    with urllib.request.urlopen(req) as response:
        print(f"Leaderboard status: {response.status}")
        res_data = response.read().decode('utf-8')
        print(f"Leaderboard response: {res_data}")
        
        leaderboard = json.loads(res_data).get('scores', [])
        found = any(entry['name'] == username and entry['score'] == score for entry in leaderboard)

        if found:
            print("SUCCESS: The submitted score is verified in the leaderboard!")
        else:
            print("FAILURE: The submitted score was not found in the leaderboard.")
except urllib.error.HTTPError as e:
    print(f"Leaderboard err status: {e.code}")
