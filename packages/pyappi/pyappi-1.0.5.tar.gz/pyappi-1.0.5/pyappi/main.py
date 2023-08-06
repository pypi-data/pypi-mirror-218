from pyappi.api_base import app,set_document_type
from pyappi.document.document import Document
from pyappi.endpoints import *
import pyappi

import uvicorn

set_document_type(Document)

def main():
    print(f"pyappi version {pyappi.__version__}")
    uvicorn.run("pyappi.main:app", port=8099, log_level="info")

if __name__ == "__main__":
    main()