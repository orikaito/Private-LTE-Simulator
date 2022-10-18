import json
from requests import post
from sys import argv
from time import sleep

url = "http://192.168.30.3/predict"
# url = "http://api.career-izuka.lab/predict"
# url = "http://api.edge-izuka.lab/predict"

img_list = [0] * 10

file_set = ""

if len(argv)==1:
    file_set = ".png"
else:
    file_set = "-"+str(argv[1])+".jpg"

for i in range(10):
    with open("./mnist_test/"+str(i)+file_set, mode='rb') as f:
        img_list[i] = f.read()

for i in range(10):
    response = post(url, files={"file":img_list[i]})
    response_json = response.json()
    print(response_json["result"], str(i)+file_set, response_json["probability"], response_json["progress_time"])
    sleep(0.01)