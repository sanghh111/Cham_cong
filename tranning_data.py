import os,cv2
import numpy as np
from PIL import Image
from tkinter import messagebox

def tranning_data():
    path = os.path.join(os.getcwd()+'/data/')
    root,dirs,files = os.walk(path)
    
    subdirs = root[1]
        
    for subdir in subdirs:
        subpath = os.path.join(path,subdir+'/')

        faces = []
        ids = []
        pictures = {}
        for root2, dirs2, files2 in os.walk(subpath):
            pictures = files2
        if len(pictures)> 300:
            for pic in pictures:
                imgpath = subpath + pic
                img = Image.open(imgpath).convert('L')
                imgNp = np.array(img,'uint8')
                id = int(pic.split(subdir)[0])
                faces.append(imgNp)
                ids.append(id)

            ids = np.array(ids)

            # Train and save classifier
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces, ids)
            clf.write("./classifiers/" + subdir + "_classifier.xml")
            messagebox.showinfo("Thông báo","Dữ liệu của {} đã được tào thành công".format(subdir))
        else:
            messagebox.showinfo("Thông báo","Dữ liệu của {} không đủ 300 tấm hình".format(subdir))

