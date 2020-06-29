import cv2
import numpy as np
import random 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time
import os

# Load Yolo
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))


def mensaje ():
  c = time.strftime("%c")
  
  sender_email_address = 'vigilanciapymensajes@gmail.com'
  sender_email_password = '@Mrtnz1970'
  receiver_email_address = 'marlonnar@gmail.com'

  email_subject_line = 'Se detecto movimiento en su casa'

  msg = MIMEMultipart()
  msg['From'] = sender_email_address
  msg['To'] = receiver_email_address
  msg['Subject'] = email_subject_line

  email_body = 'Se detecto movimiento en su vivienda consulte el video para mas informacion \n'+'Fecha y Hora:' + c
  msg.attach(MIMEText(email_body, 'plain'))

  email_content = msg.as_string()
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(sender_email_address, sender_email_password)

  server.sendmail(sender_email_address, receiver_email_address, email_content)
  server.quit()

def archivo ():
    s = time.strftime("%c")
    file = open("Control de detecciones.txt", "a")
    file.write("Se detecto movimiento \n"+"Fecha y Hora "+s +"\n")
    file.close()

cont=1
y = str(cont)+'.avi'
video = cv2.VideoCapture(0)
ret = video.set(3,320)
ret = video.set(4,240)

salida = cv2.VideoWriter(y,cv2.VideoWriter_fourcc(*'XVID'),15.0,(320,240))
k = 0
s = 200

while True:
  ret, frame = video.read()

  
  if ret == False: break
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray, (21, 21), 0)
  if k == 20:
    bgGray = gray
  if k > 20:
    dif = cv2.absdiff(gray, bgGray)
    dif = cv2.dilate(dif, None, iterations=2)
    _, th = cv2.threshold(dif, 40, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame, cnts, -1, (0,0,255),2)        
  
    
    for c in cnts:
      area = cv2.contourArea(c)
      if area > 9000 and s == 200:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)
        s = s-1
        mensaje ()
        archivo()
        
      if s!=0 and s <200:
                  
        b = salida

        ret, frame = video.read()
        
        height, width, channels = frame.shape
        
        ##deteccion de objetos
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        ##informacion q  aparece en pantalla
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Objecto detectedo
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_PLAIN
        
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y + 30), font, 2, color, 2)

        b.write(frame)
     
        if s>0:
          s=s-1         
          if s==0:
            b.release()
            cont=cont+1
            y = str(cont)+'.avi'
            salida = cv2.VideoWriter(y,cv2.VideoWriter_fourcc(*'XVID'),15.0,(320,240))
            b = salida
            s=200
        
          
       
  cv2.imshow('Frame',frame)
  k = k+1
  if cv2.waitKey(30) & 0xFF == ord ('q'):
    break
video.release()





