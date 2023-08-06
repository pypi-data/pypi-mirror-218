from pyappi.document.transaction import Transaction

def server_merge(document, write):
    for k, _ in write.items():
        if isinstance(write[k], dict): 
            server_merge(document[k], write[k])
        else:
            document[k] = write[k]
    