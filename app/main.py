from fastapi import FastAPI
from app.api.routes import products, categories, auth
from app.middleware import LoggingMiddleware
from app.database import engine, Base
from app.api.routes import products, categories, auth

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Product Catalog API")

app.add_middleware(LoggingMiddleware)


app.include_router(auth.router)
app.include_router(products.router)
app.include_router(categories.router)

@app.get("/")
def health():
    return {"status": "healthy"}