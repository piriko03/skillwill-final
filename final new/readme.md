# Book Lending API

A Django REST Framework-based API for managing book lending operations. It includes user management, book tracking, and
lending requests.

---

## Installation

### **Option 1: Local Development**

#### **1. Set up the virtual environment**

```bash
  python -m venv .venv
```

```bash
  .venv\Scripts\activate
```

#### **2. Navigate to src directory**

```bash
  cd src
```

#### **3. Install dependencies**

```bash
  pip install -r requirements.txt
```

### **Option 2: Docker**

```bash
  # Build and run with Docker
  docker-compose -f docker/docker-compose.yml up --build
```

```bash
  # Run migrations (if needed)
  docker-compose -f docker/docker-compose.yml exec web python manage.py migrate
```

---

## Running the Project

### **Local Development**

Run this command in terminal, via **src** folder:

```bash
  python manage.py runserver
```

### **Docker**

```bash
  docker-compose -f docker/docker-compose.yml up
```

Access the API documentation at:

- [Swagger UI `http://127.0.0.1:8000/swagger/`](http://127.0.0.1:8000/swagger/)

---

## Testing

### **Run Tests Locally**

```bash
# From src directory
  pytest
```

### **Run Tests in Docker**

```bash
  docker-compose -f docker/docker-compose.yml exec web pytest
```

---

## Authentication

The API uses **Basic Authentication** for secured endpoints.

1. Use your credentials (username and password) to authenticate.

### You can use default test user for testing, click **Authorize** button on Swagger UI

### email: test@test.com

### password: test

---