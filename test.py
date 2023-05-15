import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes": 55, "name": "tede", "views": 321}, {"likes": 864, "name": "edzio", "views": 33413},
        {"likes": 553, "name": "peja", "views": 33653}, {"likes": 54645, "name": "50cent", "views": 5326},
        {"likes": 255, "name": "50cent", "views": 31431}, {"likes": 4636, "name": "eminem", "views": 875453}]

for i in range(len(data)):
    response = requests.put(f"{BASE}video/{i}", data[i])
    print(response.json())
# response = requests.put(BASE + "video/3", {"likes":55, "name":"50cent", "views":333})
# print(response.json())
input()
response = requests.delete(BASE + "video/0")
print(response)
input()
response = requests.delete(BASE + "video/2")
print(response)
input()
response = requests.get(BASE + "video/4")
print(response.json())
input()
response = requests.get(BASE + "video/2")
print(response.json())
