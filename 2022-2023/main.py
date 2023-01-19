import aruco_code
import can_bus
import sys


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("usage : \n 'python3 main.py test' pour test en local \n 'python3 main.py raspi' pour test sur la raspi\n")
    elif sys.argv[1]== "test":
        print("test")
    elif sys.argv[1]=="raspi":
        print("production")
    else:
        print("usage : \n 'python3 main.py test' pour test en local \n 'python3 main.py raspi' pour test sur la raspi\n")



    print("démarrage")