import os

def tranning_data():
    path = os.path.join('./data')
    for i in os.walk(path):
        print(i)

tranning_data()