from pyappi.api_base import app
from pyappi.block.endpoints import *
from pyappi.document.endpoints import *
from pyappi.user.endpoints import *
from pyappi.sync.endpoints import *
from pyappi.stats.endpoints import *


@app.get("/pyappi")
async def pyappi_get_document():
    return {"message": "Hello World"}

@app.get("/stats")
async def get_stats(type, id):
    return {}

