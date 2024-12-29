# Items API

## Overview
Items API is a FastAPI-based application that provides CRUD (Create, Read, Update, Delete) operations for managing items. The application supports asynchronous operations and includes robust error handling, edge-case testing, and validation using Pydantic.

## Features
- Create, retrieve, update, and delete items.
- Asynchronous database operations using SQLAlchemy.
- Comprehensive test coverage using `pytest` and `pytest-asyncio`.
- Pre-commit hooks for consistent code quality and formatting.

## Installation

### Prerequisites
- Python 3.10+
- SQLite

### Clone the Repository
```bash
git clone https://github.com/wallravit/items-service
cd items-service
```

### Set Up the Environment
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Running the Application

### Run Locally
Start the FastAPI application using Uvicorn:
```bash
uvicorn items_api.main:app --reload
```

The application will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### API Documentation
FastAPI provides auto-generated Swagger UI for API documentation:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Testing
Run all tests using `pytest`:
```bash
pytest
```

## Pre-Commit Hooks
Ensure consistent code quality using `pre-commit` hooks:
1. Install `pre-commit`:
   ```bash
   pip install pre-commit
   ```

2. Install hooks:
   ```bash
   pre-commit install
   ```

3. Run hooks manually:
   ```bash
   pre-commit run --all-files
   ```

## Docker Support
Build and run the application in a Docker container:

### Build the Docker Image
```bash
docker build -t items-api .
```

### Run the Docker Container
```bash
docker run -p 8000:8000 items-api
```

### Running and Automatically Removing a Docker Container
```bash
docker run --rm -it -p 8000:8000 $(docker build -q .)
```

The application will be accessible at [http://localhost:8000](http://localhost:8000).

## API Endpoints

### Create an Item
- **POST** `/api/v1/items`
- **Payload**:
  ```json
  {
      "name": "Item Name",
      "description": "Item Description"
  }
  ```
- **Response**:
  ```json
  {
      "id": 1,
      "name": "Item Name",
      "description": "Item Description"
  }
  ```

### List All Items
- **GET** `/api/v1/items`
- **Response**:
  ```json
  [
      {
          "id": 1,
          "name": "Item Name",
          "description": "Item Description"
      }
  ]
  ```

### Get Item by ID
- **GET** `/api/v1/items/{id}`
- **Response**:
  ```json
  {
      "id": 1,
      "name": "Item Name",
      "description": "Item Description"
  }
  ```

### Update an Item
- **PUT** `/api/v1/items/{id}`
- **Payload**:
  ```json
  {
      "name": "Updated Item Name",
      "description": "Updated Item Description"
  }
  ```
- **Response**:
  ```json
  {
      "id": 1,
      "name": "Updated Item Name",
      "description": "Updated Item Description"
  }
  ```

### Delete an Item
- **DELETE** `/api/v1/items/{id}`
- **Response**:
  ```json
  {
      "message": "Item deleted successfully"
  }
  ```
