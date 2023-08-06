from pyappi.api_base import app
from pyappi.block.endpoints import *
from pyappi.user.session import verify_session  
from pyappi.document.access import read_document_with_session_access, write_document_with_session_access
from fastapi import Response
from pyappi.document.merge import server_merge
from pyappi.document.enumeration import prepare_new_document, is_new_document, lookup_document_id


@app.get("/document/{id}")
@verify_session
async def get_document(id, request: Request):
    if id.startswith("!"):
        id = lookup_document_id(id[1:].split(".")[0])

    result = read_document_with_session_access(id, request.state.session)

    return result if result else Response(status_code=404)

@app.put("/document/{id}")
@verify_session
async def update_document(id, request: Request):
    write = await request.json()

    def handler(document):
        if document._cmt and write["_bmt"] != -1 and document._cmt != write["_bmt"]:
            return Response(status_code=409)
        
        del write["_bmt"]

        if is_new_document(document):
            prepare_new_document(document,id)
            
        server_merge(document,write)

        return Response(status_code=202)

    return write_document_with_session_access(id, request.state.session, handler)

@app.post("/document/{id}")
async def create_document(id):
    return {}
