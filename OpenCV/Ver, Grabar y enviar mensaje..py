import cv2
import numpy as np
import random 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time

def mensaje ():
  c = time.strftime("%c")
  
  sender_email_address = 'vigilanciapymensajes@gmail.com'
  sender_email_password = '@Mrtnz1970'
  receiver_email_address = 'vigilanciapymensajes@gmail.com'

  email_subject_line = 'Se le metieron Pa'

  msg = MIMEMultipart()
  msg['From'] = sender_email_address
  msg['To'] = receiver_email_address
  msg['Subject'] = email_subject_line

  email_body = 'Se le metieron al chante rasta \n'+'Fecha y Hora:' + c
  msg.attach(MIMEText(email_body, 'plain'))

  email_content = msg.as_string()
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(sender_email_address, sender_email_password)

  server.sendmail(sender_email_address, receiver_email_address, email_content)
  server.quit()



cont=1
y = str(cont)+'.avi'
video = cv2.VideoCapture(0)

salida = cv2.VideoWriter(y,cv2.VideoWriter_fourcc(*'XVID'),70.0,(640,480))
b= salida
i = 0
s = 2000

while True:
  ret, frame = video.read()
  if ret == False: break
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray, (21, 21), 0)
  if i == 20:
    bgGray = gray
  if i > 20:
    dif = cv2.absdiff(gray, bgGray)
    dif = cv2.dilate(dif, None, iterations=2)
    _, th = cv2.threshold(dif, 40, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame, cnts, -1, (0,0,255),2)        
  
    
    for c in cnts:
      area = cv2.contourArea(c)
      if area > 9000 and s == 2000:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)
        s = s-1
        b.write(frame)
        mensaje ()
        
      if s!=0 and s <2000:
        if area > 9000:
          x,y,w,h = cv2.boundingRect(c)
          cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)
        b.write(frame)
        if s>0:
          s=s-1
          if s==0:
            b.release()
            s=2000
            cont=cont+1
            y = str(cont)+'.avi'
            salida = cv2.VideoWriter(y,cv2.VideoWriter_fourcc(*'XVID'),45.0,(640,480))
            b = salida

        
          
       
  cv2.imshow('Frame',frame)
  i = i+1
  if cv2.waitKey(30) & 0xFF == ord ('q'):
    break
video.release()





