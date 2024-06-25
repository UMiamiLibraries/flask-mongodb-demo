# Common Commands Reference Guide: Flask-MongoDB-Docker

This guide provides a quick reference for commonly used commands when working with a Flask application using MongoDB, both running in Docker containers.

## Docker Commands

### Start the containers
```bash
docker-compose up -d
```
Starts all services defined in your docker-compose.yml file in detached mode.

### Stop the containers
```bash
docker-compose down
```
Stops and removes all containers defined in your docker-compose.yml file.

### View running containers
```bash
docker-compose ps
```
Lists all containers defined in your docker-compose.yml file and their current status.

### View container logs
```bash
docker-compose logs <service_name>
```
Displays the logs for a specific service. Replace `<service_name>` with 'web' for Flask app logs or 'mongo' for MongoDB logs.

### Rebuild a specific service
```bash
docker-compose build <service_name>
```
Rebuilds the Docker image for a specific service. Use this after making changes to your application code.

### Execute a command in a running container
```bash
docker exec -it <container_name> <command>
```
Runs a command inside a running container. Useful for accessing shells or running one-off commands.

## MongoDB Commands

### Access MongoDB shell
```bash
docker exec -it <mongodb_container_name> mongosh
```
Opens the MongoDB shell in your MongoDB container.

### Switch to a specific database
```javascript
use <database_name>
```
Switches to a specific database (e.g., `use library_db`).

### Insert a document
```javascript
db.<collection_name>.insertOne({key: "value"})
```
Inserts a single document into a collection (e.g., `db.books.insertOne({title: "1984", author: "George Orwell"})`).

### Find documents
```javascript
db.<collection_name>.find()
```
Retrieves all documents from a collection (e.g., `db.books.find()`).

### Find specific documents
```javascript
db.<collection_name>.find({key: "value"})
```
Retrieves documents matching specific criteria (e.g., `db.books.find({author: "George Orwell"})`).

### Update a document
```javascript
db.<collection_name>.updateOne({filter}, {$set: {update}})
```
Updates a single document (e.g., `db.books.updateOne({title: "1984"}, {$set: {year: 1949}})`).

### Delete a document
```javascript
db.<collection_name>.deleteOne({key: "value"})
```
Deletes a single document matching the criteria (e.g., `db.books.deleteOne({title: "1984"})`).

## Flask Application Commands

### Run Flask development server (if not using Docker)
```bash
flask run
```
Starts the Flask development server.

### Set Flask environment variables (if not using Docker)
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```
Sets environment variables for Flask application.

## Git Commands (for version control)

### Initialize a new Git repository
```bash
git init
```

### Add files to staging area
```bash
git add .
```
Adds all changed files to the staging area.

### Commit changes
```bash
git commit -m "Your commit message"
```
Commits staged changes with a descriptive message.

### Create a new branch
```bash
git branch <branch_name>
```
Creates a new branch.

### Switch to a branch
```bash
git checkout <branch_name>
```
Switches to the specified branch.

### Push changes to remote repository
```bash
git push origin <branch_name>
```
Pushes local commits to the remote repository.

Remember to replace placeholders (text inside `<>`) with actual values relevant to your setup. This guide covers basic operations; for more complex tasks, refer to the official documentation of Docker, MongoDB, Flask, and Git.