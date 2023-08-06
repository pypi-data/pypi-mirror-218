from pyappi.api_base import app,set_document_type
from pyappi.document.document import Document
from pyappi.endpoints import *

import uvicorn

set_document_type(Document)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8099, log_level="info")