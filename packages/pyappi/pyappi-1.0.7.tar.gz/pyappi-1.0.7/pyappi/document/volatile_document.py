from pyappi.document.transaction import Transaction
from pyappi.document.lock import global_appi_mutex
from pyappi.document.exceptions import *
from pyappi.document.type import *
from typing import Any

import time


volatile_documents = {}


class VolatileDocument:
    def __init__(self, name):
        self.__dict__['__name'] = name
        self.__dict__['__tsx'] = 0
        self.__dict__['__lock'] = False
        self.__dict__['__document'] = {}

    def delete(self):
        try:
            del volatile_documents[self.__dict__['__name']]
            return True
        except Exception as _:
            return False

    def __update(self, tsx):
        self.__dict__['__document']["_cmt"] = tsx
        self.__dict__['__document']["_lmt"] = int(time.time())

    def __setattr__(self, __name: str, __value: Any) -> None:
        if not self.__dict__['__lock']:
            raise DocumentNotLocked()

        if not isinstance(__value, dict):
            raise "Root values not allowed in Appi"
        
        if len(__value):
            raise NoPrepopulatedObjects()

        self.__dict__['__document'][__name] = __value

    def __getattr__(self, key):
        if not self.__dict__['__lock']:
            raise DocumentNotLocked()

        if key == '_Transaction__update':
            return self._VolatileDocument__update
        
        doc = self.__dict__['__document'][key]
        return Transaction(doc, self.__dict__['__tsx'], self, type_lookup(key,doc))

    def __setitem__(self, __name: str, __value: Any) -> None:
        return self.__setattr__(__name,__value)
    
    def __getitem__(self, __name: str):
        return self.__getattr__(__name)

    def __enter__(self):
        global_appi_mutex.acquire()

        self.__dict__['__lock'] = True
        self.__dict__['__document'] = volatile_documents.get(self.__dict__['__name'],{})
        self.__dict__['__tsx'] = self.__dict__['__document'].get("_cmt",0) + 1

        return self
    
    def __exit__(self, type, value, traceback):
        volatile_documents[self.__dict__['__name']] = self.__dict__['__document']
        self.__dict__['__lock'] = False

        global_appi_mutex.release()