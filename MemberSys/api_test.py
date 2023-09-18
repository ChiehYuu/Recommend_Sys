import requests
import json
import numpy as np

np.random.seed(1)

path = 'http://127.0.0.0'
user_id = np.random.randint(0 , 10)
action = input('Enter action: ')
var = '/items/{user_id}/{status}'.format(user_id=user_id, status=action)

req = requests.get(path + var)
print(req)
text = req.text
print(text)
json_data = json.loads(text)

if __name__ == '__main__':

    print(user_id)
    print(action)
    print(json_data)



