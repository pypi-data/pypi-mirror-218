from pyappi.api_base import app
from pyappi.block.endpoints import *
from pyappi.user.session import verify_session
from pyappi.document.local import sync_user_local_transaction


@app.get("/sync/status/{tsx}")
@verify_session
async def sync_status(tsx, request: Request):
    result = sync_user_local_transaction(int(tsx),request.state.session["user"])

    return result
