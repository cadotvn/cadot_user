# User Management API

A FastAPI-based REST API for user management with authentication and authorization features.

## Features

- **User Management**: Create, read, update, and delete user accounts
- **Authentication**: JWT-based authentication system
- **Authorization**: Role-based access control (superuser privileges)
- **Security**: Password hashing with bcrypt
- **Database**: SQLAlchemy ORM with PostgreSQL (easily configurable for other databases)
- **Validation**: Pydantic schemas for request/response validation
- **Documentation**: Auto-generated OpenAPI/Swagger documentation

## Project Structure

```
cadot_user/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── api.py
│   │   │   └── endpoints/
│   │   │       └── users.py
│   │   └── deps.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── crud/
│   │   ├── base.py
│   │   └── crud_user.py
│   ├── db/
│   │   ├── base.py
│   │   ├── base_class.py
│   │   ├── init_db.py
│   │   └── session.py
│   ├── models/
│   │   └── user.py
│   └── schemas/
│       ├── token.py
│       └── user.py
├── tests/
├── docs/
├── main.py
├── requirements.txt
├── env.example
└── README.md
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cadot_user
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Set up PostgreSQL database**
   ```bash
   # Option 1: Use the automated setup script
   python setup_db.py
   
   # Option 2: Manual setup
   createdb cadot_user
   psql -d cadot_user -c "CREATE SCHEMA IF NOT EXISTS cadot;"
   ```

6. **Initialize application database**
   ```bash
   python start.py
   ```

## Running the Application

### Development Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the application is running, you can access:

- **Interactive API docs**: http://localhost:8000/docs
- **Alternative API docs**: http://localhost:8000/redoc
- **OpenAPI schema**: http://localhost:8000/openapi.json

## API Endpoints

### Authentication
- `POST /api/v1/login/access-token` - Login and get access token

### Users
- `GET /api/v1/users/` - List users (requires authentication)
- `POST /api/v1/users/` - Create new user
- `GET /api/v1/users/me` - Get current user info
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/{user_id}` - Get user by ID

## Database Models

### User
- `id`: Primary key
- `email`: Unique email address
- `username`: Unique username
- `full_name`: User's full name
- `phone_number`: Contact phone number
- `avatar_url`: Profile picture URL
- `hashed_password`: Encrypted password
- `is_active`: Account status
- `is_superuser`: Admin privileges
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Tokens**: Secure authentication with configurable expiration
- **CORS Protection**: Configurable cross-origin resource sharing
- **Input Validation**: Pydantic schemas for data validation
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## Configuration

The application uses environment variables for configuration. Key settings include:

- `SECRET_KEY`: JWT signing key
- `DATABASE_URL`: Database connection string
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time
- `BACKEND_CORS_ORIGINS`: Allowed CORS origins

### PostgreSQL Configuration

The application is configured to use PostgreSQL with the following settings:
- **Default Schema**: cadot (automatically appended to all connections)
- **Connection**: All database settings must be provided in the `.env` file

#### Configuration Options

**Option 1: Complete DATABASE_URL (recommended)**
```bash
DATABASE_URL=postgresql://postgres:1qazxsw2@localhost/cadot_user
```
The schema `cadot` will be automatically appended.

**Option 2: Individual Components**
```bash
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=cadot_user
DATABASE_USER=postgres
DATABASE_PASSWORD=1qazxsw2
DATABASE_SCHEMA=cadot
```

#### Environment Variables Required

The following database-related environment variables must be set in your `.env` file:
- `DATABASE_URL` (complete connection string), OR
- `DATABASE_HOST`, `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD` (individual components)
- `DATABASE_SCHEMA` (optional, defaults to "cadot")

## Development

### Adding New Models
1. Create model in `app/models/`
2. Create schemas in `app/schemas/`
3. Create CRUD operations in `app/crud/`
4. Create API endpoints in `app/api/v1/endpoints/`
5. Update imports in respective `__init__.py` files

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Database Migrations
The project is set up to use Alembic for database migrations:

```bash
# Initialize Alembic (first time)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.
