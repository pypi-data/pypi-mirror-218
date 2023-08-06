import unittest
import time

from pyappi import VolatileDocument, Document

class TestAppiLog(unittest.TestCase):
    def setUp(self):
        self.test_documents = [(VolatileDocument,"vdtest"), (Document,"dtest")]
        [doc(name).delete() for (doc,name) in self.test_documents]

    def _test_log_base(self,_doc_type, _doc_name):
        with _doc_type(_doc_name) as doc:
            doc["comments~log"] = {}
            log  = doc["comments~log"]

            log._depth = 8
            log._size = 256
            log._interval = 1000* 60 * 60
            log._server_t = -1

            now = int(time.time())

            for i in range(9):
                log[now + i] = { "message": "message"+str(i) }

            self.assertEqual(log[now+0], None)

            for i in range(1, 9):
                self.assertEqual(log[now+i].message, "message"+i)

    def test_log(self):
        [self._test_log_base(doc,name) for (doc,name) in self.test_documents]



if __name__ == "__main__":
    unittest.main()
