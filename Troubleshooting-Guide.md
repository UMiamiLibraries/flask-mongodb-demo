# Troubleshooting Guide: Flask-MongoDB-Docker Setup

This guide is designed to help librarians troubleshoot common issues with a Flask application using MongoDB, both running in Docker containers.

## 1. Verifying Docker Setup

First, ensure your Docker containers are running:

```bash
docker-compose ps
```

This command lists all containers defined in your docker-compose.yml file and their current status.

If containers are not running, start them with:

```bash
docker-compose up -d
```

The `-d` flag runs the containers in detached mode (in the background).

## 2. Checking MongoDB Connection

To check if MongoDB is running and accessible, try connecting to it:

```bash
docker exec -it <mongodb_container_name> mongosh
```

Replace `<mongodb_container_name>` with your actual MongoDB container name (e.g., flask-mongodb-demo-mongo-1).

If successful, you'll see the MongoDB shell prompt.

## 3. Inserting Test Data

Once in the MongoDB shell, you can insert a test record:

```javascript
use library_db
db.books.insertOne({
  title: "To Kill a Mockingbird",
  author: "Harper Lee",
  isbn: "9780446310789",
  published_year: 1960,
  genre: "Fiction"
})
```

To verify the insertion, run:

```javascript
db.books.find()
```

This should display the document you just inserted.

## 4. Checking Data Persistence

To ensure data persists across container restarts:

1. Exit the MongoDB shell (type `exit`)
2. Stop and remove the containers:

   ```bash
   docker-compose down
   ```

3. Start the containers again:

   ```bash
   docker-compose up -d
   ```

4. Connect to MongoDB again and check for the data:

   ```bash
   docker exec -it <mongodb_container_name> mongosh
   use library_db
   db.books.find()
   ```

If you see the document, data persistence is working correctly.

## 5. Checking Flask Application

If MongoDB is working but your Flask application can't see the data:

1. Check Flask logs:

   ```bash
   docker-compose logs web
   ```

   Look for any error messages related to MongoDB connection.

2. Verify the MongoDB connection string in your Flask app (usually in `app/main.py`). It should look like:

   ```python
   client = MongoClient('mongodb://mongo:27017/')
   ```

   'mongo' is the service name defined in docker-compose.yml.

3. If needed, rebuild the Flask container:

   ```bash
   docker-compose build web
   docker-compose up -d
   ```

## 6. Checking Docker Volumes

To ensure your MongoDB data is being stored persistently:

1. List Docker volumes:

   ```bash
   docker volume ls
   ```

   Look for a volume related to your MongoDB data.

2. Inspect the volume:

   ```bash
   docker volume inspect <volume_name>
   ```

   This shows where Docker is storing the data on your host machine.

## 7. Reviewing Docker Compose File

Ensure your `docker-compose.yml` file correctly defines the services and volume:

```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: docker/Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - ./app:/app
    depends_on:
      - mongo

  mongo:
    image: mongo:7.0.11
    ports:
      - "27017:27017"
    volumes:
      - mongodata:/data/db

volumes:
  mongodata:
```

This configuration sets up a persistent volume for MongoDB data.

## 8. Rebuilding from Scratch

If all else fails, you can try rebuilding everything from scratch:

```bash
docker-compose down -v  # The -v flag removes named volumes
docker-compose build
docker-compose up -d
```

Then, reinsert your data and check if the issue is resolved.

Remember, always backup your data before performing operations that might lead to data loss.

By following these steps, you should be able to troubleshoot most common issues with your Flask-MongoDB-Docker setup. If problems persist, consider checking your application code for any logic errors in database interactions.