import requests
import json

url = "http://192.168.30.3/predict"
# url = "http://api.career-izuka.lab/predict"
# url = "http://api.edge-izuka.lab/predict"

img_list = [0] * 10

for i in range(10):
    with open("./mnist_test/"+str(i)+".png", mode='rb') as f:
        img_list[i] = f.read()

for i in range(10):
    response = requests.post(url, files={"file":img_list[i]})
    response_json = response.json()
    print(response_json["result"],i,response_json["progress_time"])