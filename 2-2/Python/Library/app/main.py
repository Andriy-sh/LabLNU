# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from app.db.database import init_db
# from app.utils.logger import setup_logger
# from app.api import books, authors, categories, users, borrowed_books
# from sqlalchemy.exc import SQLAlchemyError
from app.api.associations import router as associations_router

# from fastapi import FastAPI
# from app.db.database import init_db
# from app.utils.logger import setup_logger

# app = FastAPI(
#     title="Library Management System",
#     description="RESTful API for managing library resources",
#     version="1.0.0"
# )

# # Setup CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Setup logging
# logger = setup_logger()

# # Error handling
# @app.exception_handler(SQLAlchemyError)
# async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
#     logger.error(f"Database error: {str(exc)}")
#     return JSONResponse(
#         status_code=500,
#         content={"message": "Database error occurred"}
#     )

# # Include routers
# app.include_router(books.router, prefix="/api/v1")
# app.include_router(authors.router, prefix="/api/v1")
# app.include_router(categories.router, prefix="/api/v1")
# app.include_router(users.router, prefix="/api/v1")
# app.include_router(borrowed_books.router, prefix="/api/v1")

# @app.on_event("startup")
# async def startup_event():
#     init_db()
#     logger.info("Application started")

# @app.get("/")
# async def root():
#     return {
#         "message": "Library Management System API",
#         "docs_url": "/docs",
#         "endpoints": {
#             "books": "/api/v1/books",
#             "authors": "/api/v1/authors",
#             "categories": "/api/v1/categories",
#             "users": "/api/v1/users",
#             "borrowed_books": "/api/v1/borrowed-books"
#         }
#     }

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy"}


# 

# from fastapi import FastAPI
# from app.db.database import init_db
# from app.utils.logger import setup_logger

# app = FastAPI(
#     title="Library Management System",
#     description="RESTful API for managing library resources",
#     version="1.0.0"
# )

# # Setup logging
# logger = setup_logger()

# @app.on_event("startup")
# async def startup_event():
#     init_db()
#     logger.info("Application started")

# @app.get("/")
# async def root():
#     return {"message": "Library Management System API"}


from fastapi import FastAPI
from app.db.database import init_db
from app.utils.logger import setup_logger
from app.api import books, authors, categories, users, borrowed_books
from app.models import book, author, category, user, borrowed_book, associations
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Library Management System",
    description="RESTful API for managing library resources",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
app.include_router(books.router)
app.include_router(authors.router)
app.include_router(categories.router)
app.include_router(users.router)
app.include_router(borrowed_books.router)
app.include_router(associations_router)

logger = setup_logger()

@app.on_event("startup")
async def startup_event():
    init_db()
    logger.info("Application started")

@app.get("/")
async def root():
    return {"message": "Library Management System API"}