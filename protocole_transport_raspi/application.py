from api_envoi import main as envoyer

def main(q):
    # q.put("hello world")
    print("queue est vide :",q.empty())
    message=q.get() # le get est bloqué en attente visiblement, la queue est vide 
    print("data reçue dans app : ",message.data)