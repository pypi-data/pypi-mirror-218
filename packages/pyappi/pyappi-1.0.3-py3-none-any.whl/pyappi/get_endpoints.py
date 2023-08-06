from .api_base import app


@app.get("/test")
async def pyappi_get_document():
    return {"message": "Hello World"}

@app.get("/bulk/{type}/{id}")
async def get_bulk(type, id):
    return {}

@app.get("/bulk2/{type}/{id}")
async def get_bulk2(type, id):
    return {}

@app.get("/is/{type}/{id}")
async def get_is(type, id):
    return {}

@app.get("/is2/{type}/{id}")
async def get_is2(type, id):
    return {}

@app.get("/appi/{id}")
async def get_appi(id):
    return {}

@app.get("/stats")
async def get_stats(type, id):
    return {}

@app.get("/user/token")
async def get_user_token():
    return {}