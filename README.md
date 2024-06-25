# flask-mongodb-demo
This project demonstrates a Flask application with MongoDB integration using Docker Compose.

## Setup

1. Install Docker and Docker Compose
2. Run `docker-compose up -d` to start the application
3. Access the application at `http://localhost:5001`

## Using MongoDB Compass

1. Download and install MongoDB Compass
2. Connect to `mongodb://localhost:27017`
3. You can now view and manipulate the database using the GUI

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