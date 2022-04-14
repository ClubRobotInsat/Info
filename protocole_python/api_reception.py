import sys
import subprocess
from time import sleep
from threading import Thread


def process_message_reçu(mess):
    print(mess)

# réception 
reception = subprocess.Popen(["candump","any"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
while True: 
    output=reception.stdout.readline()
    if output:
        process_message_reçu(output.strip()) #output.strip() est un string 