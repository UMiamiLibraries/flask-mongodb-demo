# flask-mongodb-demo
This project demonstrates a Flask application with MongoDB integration using Docker Compose.

The repo is broken up into version numbers so you can follow along at different points in the development cycle.

## Tech Stack

1. python:3.11-slim
2. mongo:7.0.11
3. Flask==3.0.3 
4. pymongo==4.7.3

## Local Environment

1. Mac Studio
2. Apple M1 Max
3. macOS Sonoma 14.5
4. IntelliJ IDEA 2024.1.3
5. Docker v4.19.0

# Repo

1. https://github.com/UMiamiLibraries/flask-mongodb-demo

# Docker and Docker Compose
Install Docker and Docker Compose

https://www.docker.com/products/docker-desktop/

# Mongo Compass
Download and install MongoDB Compass

https://www.mongodb.com/products/tools/compass

## Setup

### Clone the repo 

1. **Create a directory named `Flask-Mongodb-Demo`**:
    ```bash
    mkdir Flask-Mongodb-Demo
    ```

2. **Change the current directory to `Flask-Mongodb-Demo`**:
    ```bash
    cd Flask-Mongodb-Demo
    ```

3. **Clone the repository from GitHub into the current directory**:
    ```bash
    git clone https://github.com/UMiamiLibraries/flask-mongodb-demo.git
    ```

4. **Change the current directory to the cloned repository directory**:
    ```bash
    cd flask-mongodb-demo
    ```

5. **Verify the current status of the Git repository**:
    ```bash
    git status
    ```
6. **Fetch all tags**
   ```bash
   git fetch --all --tags
   ```

7. **(Optional) List all tags**
    ```bash
    git tag
    ```
8. **Checkout a specific tag and create a new branch**
   ```bash
   git checkout tags/v0.2 -b v0.2-branch
   ```
   
### Using Docker
1. Run `docker-compose up -d` to start the application
2. Access the application at `http://localhost:5000`

## Using MongoDB Compass
1. Connect to `mongodb://localhost:27017`
2. You can now view and manipulate the database using the GUI

### Creating a Collection and Adding Data

1. In MongoDB Compass, connect to `mongodb://localhost:27017`
2. You should see a database called `library_db`. If not, create it.
3. Inside `library_db`, create a new collection called `books`.
4. To add a sample document, click on the `books` collection, then click "Add Data" > "Insert Document".
5. Enter the following JSON and click "Insert":

   ```json
   {
     "title": "To Kill a Mockingbird",
     "author": "Harper Lee",
     "isbn": "9780446310789",
     "published_year": 1960,
     "genre": "Fiction"
   }
   ```

6. You should now see this document in your `books` collection.

## Development

To make changes to the application:

1. Modify the files in the `app` directory
2. The changes will be reflected immediately due to volume mounting

To add new dependencies:

1. Add them to `docker/requirements.txt`
2. Rebuild the Docker image: `docker-compose build`
3. Restart the containers: `docker-compose up -d`