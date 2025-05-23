# Library Management System

A full-stack library management system built with FastAPI and PostgreSQL.

## 🚀 Features

- RESTful API for library management
- PostgreSQL database for data storage
- Docker containerization
- PgAdmin for database management
- User authentication and authorization
- Book management (add, update, delete, search)
- User management
- Borrowing system

## 📋 Prerequisites

- Docker
- Docker Compose
- FastAPI
- NextJS

## 🛠️ Installation and Setup

1. Clone the repository:
```bash
git clone https://github.com/Andriy-sh/Library.git
cd <project-directory>
```
2.Create a `.env` file in the root directory with the following content:
```env
  - DATABASE_URL=postgresql://postgres:postgres@db:5432/library_db
  - DATABASE_TEST_URL=postgresql://postgres:postgres@db:5432/library_test
  - LOG_LEVEL=INFO
```
3. Start the application using Docker Compose:
```bash
docker-compose up --build
```

The application will be available at:
- Backend API: http://localhost:8000
- PgAdmin: http://localhost:5050
- PostgreSQL: localhost:5432
- Frontend[NextJS]: http://localhost:3050

## 🔧 Configuration

### Environment Variables

The following environment variables are configured in docker-compose.yml:

- Database:
  - POSTGRES_USER: user
  - POSTGRES_PASSWORD: password
  - POSTGRES_DB: library_db or db

- PgAdmin:
  - PGADMIN_DEFAULT_EMAIL: admin@admin.com
  - PGADMIN_DEFAULT_PASSWORD: admin

## 📚 API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoints

#### Books
```http
GET /books
GET /books/{book_id}
POST /books
PUT /books/{book_id}
DELETE /books/{book_id}
```

#### Users
```http
GET /users
GET /users/{user_id}
POST /users
PUT /users/{user_id}
DELETE /users/{user_id}
```

#### Borrowings
```http
POST /borrowed-books
GET /borrowed-books
GET /borrowed-books/active
GET /{borrowed_book_id}/return
```

#### Category
```http
GET /category
GET /category/{category_id}
POST /category
PUT /category/{category_id}
DELETE /category/{category_id}
```

#### Author
```http
GET /author
GET /author/{author_id}
POST /author
PUT /author/{author_id}
DELETE /author/{author_id}
```
#### Association
```http
GET /book/{book_id}/authors
GET /book/{book_id}/categories
```

## 🗄️ Database Management

1. Access PgAdmin at http://localhost:5050
2. Login with:
   - Email: admin@admin.com
   - Password: admin
3. Add a new server:
   - Host: db
   - Port: 5432
   - Database: postgres
   - Username: user
   - Password: password

## 🔍 Development

The project structure:
```
.
├── app/                 # Backend application
├── frontend/           # Frontend application
├── alembic/            # Database migrations
├── logs/              # Application logs
├── docker-compose.yml # Docker configuration
└── README.md         # Project documentation
```

## 🧪 Testing

The project includes comprehensive unit tests for all API endpoints using pytest.

### Running Tests

To run all tests:
```bash
python -m pytest tests/
```

