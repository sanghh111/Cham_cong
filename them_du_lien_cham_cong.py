import json,os
from ntpath import join
from datetime import datetime
# import datetime

def them_du_lieu_cham_cong(name,present):
    present = str(present)
    present =  present.split(' ')
    day = present[0].split('-')
    time = present[1].split(':')
    path = os.path.join('./chamcong',day[0])    
    them_floder(path)
    path = os.path.join(path,day[1])
    them_floder(path)
    try:
        f =  open(os.path.join(path,'{}.json'.format(day[2])),'r+')
        data = json.load(f)
    except Exception as e:
        print(e)
        f =  open(os.path.join(path,'{}.json'.format(day[2])),'w')
        data =[]
    data_user =  {'id' : name,
                'time' : "{}:{}".format(time[0],time[1])}
    data.append(data_user)
    f.seek(0)
    json.dump(data,f,indent=3)
    f.close()
    pass

def them_floder(path):
    try:
        os.mkdir(path)
    except Exception as e:
        # print(e)
        pass

# them_du_lieu_cham_cong('sang',datetime.now())