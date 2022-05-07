from multiprocessing import Process, Queue
from time import sleep 
from test_queue2 import f1
from test_queue3 import f2

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f1, args=(q,))
    p1 = Process(target=f2,args=(q,))
    p1.start()
    p.start()
    # print(q.get())    # prints "[42, None, 'hello']"
    # print(q.get()) 
    p.join()
    p1.join()