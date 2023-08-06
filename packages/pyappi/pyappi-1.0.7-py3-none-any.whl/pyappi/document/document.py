
from typing import Any
from .random_handler import random_handler
from .type import type_lookup
from .exceptions import *
from .file_handler import file_handler
from pyappi.document.lock import global_appi_mutex
from pyappi.document.transaction import Transaction
from pyappi.document.local import update_user_local_transaction
from pyappi.document.history import update_document_history
from pyappi.util.merge import dict_merge
from pyappi.util.filename import clean_filename

import json
import os
import time








document_config = {
    "root": "appidb/documents"
}

if document_config["root"]:
    os.makedirs(document_config["root"],exist_ok=True)


class Document():
    def __init__(self, name, who, path=None, read_only=False, auto_nav=True):
        self.__dict__['__path'] = document_config["root"] if not path else path
        self.__dict__['__auto_nav'] = auto_nav
        self.__dict__['name'] = name
        self.__dict__['__who'] = who
        self.__dict__['__tsx'] = 0
        self.__dict__['__lock'] = False
        self.__dict__['__mutated'] = False
        self.__dict__['__read_only'] = read_only
        self.__dict__['__document'] = {}
        self.__dict__['__delta'] = {}

    def __len__(self):
        return len(self.__dict__['__document'])
    
    def __contains__(self, key):
        return key in self.__dict__['__document']

    def unwrap(self):
        return self.__dict__['__document']

    def __update(self, tsx, key, delta):
        self.__dict__['__delta'][key] = self.__dict__['__delta'].get(key,{})
        dict_merge(self.__dict__['__delta'][key],delta)

        self.__dict__['__mutated'] = True
        self.__dict__['__document']["_cmt"] = tsx
        self.__dict__['__document']["_lmt"] = int(time.time())

    def __setattr__(self, __name: str, __value: Any) -> None:
        if self.__dict__['__read_only']:
            raise ReadOnlyDocument()

        if not self.__dict__['__lock']:
            raise DocumentNotLocked()

        if not isinstance(__value, dict):
            raise "Root values not allowed in Appi"
        
        if len(__value):
            raise "You can't create a pre-populated dictionary"

        self.__dict__['__document'][__name] = __value
        self.__update(self.__dict__['__tsx'],__name, self.__dict__['__document'][__name])

    def __getattr__(self, key):
        if not self.__dict__['__lock']:
            raise DocumentNotLocked()

        if key == '_Transaction__update':
            return self._Document__update
        doc = self.__dict__['__document'].get(key,None)
        if not doc:
            if self.__dict__['__auto_nav'] and not self.__dict__['__read_only']:
                if key.startswith("__") and key.endswith("__"):
                    return None
                self.__dict__['__document'][key] = {}
                doc = self.__dict__['__document'][key]
            else:
                raise PathDoesntExist()
            
        if isinstance(doc, dict):  
            return Transaction(doc, self.__dict__['__tsx'],key, self, type_lookup(key,doc), self)
        else:
            return doc

    def __setitem__(self, __name: str, __value: Any) -> None:
        return self.__setattr__(__name,__value)
    
    def __getitem__(self, __name: str):
        return self.__getattr__(__name)

    def __enter__(self):
        global_appi_mutex.acquire()

        self.__dict__['__lock'] = True
        try:
            filename = clean_filename(f'{self.__dict__["__path"] }/{self.name}.json')
            with open(filename) as document_handle:
                self.__dict__['__document'] = json.load(document_handle)
        except Exception as e:
            if self.__dict__['__read_only']:
                self.__dict__['__lock'] = False
                global_appi_mutex.release()
                raise e
            
            self.__dict__['__document'] = {}

        self.__dict__['__tsx'] = self.__dict__['__document'].get("_cmt",0) + 1

        return self
    
    def delete(self):
        record = f'{self.__dict__["__path"]}/{self.__dict__["name"]}.json'
        backup = f'{self.__dict__["__path"]}/{self.__dict__["name"]}.backup.json'

        try:
            os.remove(backup)
        except OSError:
            pass

        try:
            os.remove(record)
        except OSError:
            pass
    
    def __exit__(self, type, value, traceback):
        if not self.__dict__['__mutated'] or self.__dict__["__read_only"]:
            self.__dict__['__lock'] = False
            global_appi_mutex.release()

            return
        
        record = clean_filename(f'{self.__dict__["__path"]}/{self.__dict__["name"]}.json')
        backup = clean_filename(f'{self.__dict__["__path"]}/{self.__dict__["name"]}.backup.json')

        try:
            os.remove(backup)
        except OSError:
            pass

        try:
            os.rename(record, backup)
        except OSError:
            pass
        
        with open(record, "w") as doc:
            doc.write(json.dumps(self.__dict__['__document'] , indent=4))

        tsx = self.__dict__['__tsx']
        permissions = self.__dict__['__document'].get("_perm",{})
        is_public = permissions.get("public","") == "read"

        for user,level in permissions.items():

            if user == "public" or user[0] == '_' or value == "level":
                continue

            update_user_local_transaction(user, self.__dict__["name"], tsx, is_public)

        update_document_history(self.__dict__['__who'],self.__dict__['name'],tsx, is_public, self.__dict__['__delta'])

        self.__dict__['__lock'] = False
        global_appi_mutex.release()




