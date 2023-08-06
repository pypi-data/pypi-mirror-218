import unittest
from pyappi import VolatileDocument, Document
from pyappi import NoPrepopulatedObjects, DocumentNotLocked

class TestAppiCore(unittest.TestCase):
    def __init__(self):
        self.test_documents = [(VolatileDocument,"vdtest"), (Document,"dtest")]

    def setUp(self):
        [doc(name).delete() for (doc,name) in self.test_documents]

    def _test_transaction_base(self,_doc_type, _doc_name):
        with _doc_type(_doc_name) as doc:

            self.assertRaises(NoPrepopulatedObjects, lambda: setattr(doc,"invalid", {"pre-defined":"not allowed because it prevents the pre-processor from running"}))    

            doc.types = {}
            doc.types.int = 1
            doc.types.string = "string"
            doc.types.float = 63.437

            self.assertEqual(1,doc.types.int)
            self.assertEqual("string",doc.types.string)
            self.assertEqual(63.437,doc.types.float)


            doc.types.subobj = {}
            doc.types.subobj["test~pre"] = "after"
            doc.types.subobj["test~pre"] = "before-"

            self.assertEqual("before-after",doc.types.subobj["test~pre"])

        self.assertRaises(DocumentNotLocked, lambda: doc.types)
        self.assertRaises(DocumentNotLocked, lambda: setattr(doc.types,"int",2))
            

    def test_transaction(self):
        [self._test_transaction_base(doc,name) for (doc,name) in self.test_documents]



if __name__ == "__main__":
    unittest.main()
