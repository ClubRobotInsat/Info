from time import sleep 


def f2(q):
    print("je dors...")
    sleep(5)
    print(q.get())    
    q.put([42, None, 'hola'])