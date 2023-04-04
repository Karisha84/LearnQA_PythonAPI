import requests

"""
Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
"""
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)
print(response.status_code)

"""
Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
"""
response_2 = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response_2.text)
print(response_2.status_code)

"""
Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
"""
payload = {"method": "GET"}
response_3 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payload)
print(response_3.text)
print(response_3.status_code)

"""
С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method. 
Например с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее. 
И так для всех типов запроса. Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра, 
но сервер отвечает так, словно все ок. Или же наоборот, когда типы совпадают, но сервер считает, что это не так.
"""
methods = ["get", "post", "put", "delete"]
parameters_methods = [{"method": "GET"}, {"method": "POST"}, {"method": "PUT"}, {"method": "DELETE"}]

for methods in methods:
    for param in parameters_methods:
        if methods == "get":
            response = requests.request(method=methods, url="https://playground.learnqa.ru/ajax/api/compare_query_type",
                                        params=param)
        else:
            response = requests.request(method=methods, url="https://playground.learnqa.ru/ajax/api/compare_query_type",
                                        data=param)
        if response.text == '{"success":"!"}' and response.status_code == 200:
            print(f"method {methods} with parameter params={param} has following result {response.text}"
                  f" with status code {response.status_code}")
