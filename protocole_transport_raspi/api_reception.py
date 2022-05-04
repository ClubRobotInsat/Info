import sys
import subprocess
from time import sleep
from threading import Thread

id_raspi = 0 

def process_message_reçu(mess):
    print("process message...")
    #récupérer id dans une variable 
    #si le message est pour moi, traiter et mettre dans buffer 
    #sinon break 
    print(mess)

# réception 
#reception = subprocess.Popen(["candump","any"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
reception=subprocess.Popen(['ping', 'geekflare.com'], stdout=subprocess.PIPE, text=True)
while True: 
    output=reception.stdout.readline()
    if output:
        process_message_reçu(output.strip()) #output.strip() est un string 

