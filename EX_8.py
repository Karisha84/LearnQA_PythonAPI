import json
import time

import requests


response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")

token = json.loads(response.text)
seconds = json.loads(response.text)['seconds']
response_1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=token)
assert response_1.text == '{"status":"Job is NOT ready"}'

time.sleep(seconds)
response_2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=token)
assert response_2.text == '{"result":"42","status":"Job is ready"}'
