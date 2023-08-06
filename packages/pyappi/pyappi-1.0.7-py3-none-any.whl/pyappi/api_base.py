from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

description = """"""
version = "1.0.1"

app = FastAPI(title="pyappi", description=description, version=version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

document_type = None
def set_document_type(dt):
    global document_type

    document_type = dt

def get_document_type():
    return document_type