import requests
import json

url = "http://192.168.30.3/predict"

img_list = [[0] * 10 for i in range(10)]

for i in range(10):
    for j in range(10):
        with open("./mnist_test/"+str(i)+"-"+str("{:03}".format(j+1))+".jpg", mode='rb') as f:
            img_list[i][j] = f.read()

for i in range(10):
    for j in range(10):
        response = requests.post(url, files={"file":img_list[i][j]})
        response_json = response.json()
        print(response_json["result"],i,j,response_json["progress_time"])