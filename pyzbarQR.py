import cv2
import numpy as np
from pyzbar.pyzbar import decode
# from dronekit import connect

# connection_string="/dev/ttyACM0"
# baud_rate = 115200
# vehicle = connect(connection_string, baud=115200, wait_ready=True)

cap=cv2.VideoCapture(0) #video yakalama ve çözünürlük için gerekli kodlar
cap.set(3,640)
cap.set(4,480)

with open('AuthorizedShipList') as f: #yetkili gemilerin listesinin bulundugu text dosyası
    myDataList=f.read().splitlines()

while True:
    success, img=cap.read()#videodan gelen görüntüyü okuma
    for barcode in decode(img):#döngü yardımı ile  okunan qr'ın çözülmesi
        myData = barcode.data.decode('utf-8') # qr'ın içerisindeki bilginin çözülüp değişkene aktarılması
        print(myData)
        if myData in myDataList: # degiskenin icerisindeki verinin yetkili gemiler listesine ait olup olmadiğinin kontrolu ve ona gore inis yapmasi veya yapmamasi
            myOutput='Dogrulama Basarili'
            myColor=(0,255,0)
        else:
            myOutput='Erisim Engellendi'
            myColor=(0,0,255)
        pts=np.array([barcode.polygon],np.int32)
        pts=pts.reshape((-1,1,2))                       # okunan qr'ın dikdortgene alması
        cv2.polylines(img,[pts],True,myColor,5)
        pts2=barcode.rect
        cv2.putText(img,myOutput,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,
        0.9,(255,0,255),2)
    cv2.imshow('Result',img) #sonucun ekranda gosterilmesi
    cv2.waitKey(1)
