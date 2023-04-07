import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
first_response = response.history[0]
print(first_response.url)
for i in response:
    response = response
    if response.status_code == 200:
        print(response.url)
print(response.history)

