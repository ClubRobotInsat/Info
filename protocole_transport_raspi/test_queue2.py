from time import sleep

def f1(q):
    print("f1 met dans la queue")
    q.put([42, None, 'hello'])

