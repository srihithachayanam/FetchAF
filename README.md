# FetchAF: Natural Language to SQL Query Generator

FetchAF is an interactive web application that allows users to query PostgreSQL databases using natural language. Built with Streamlit and powered by Cohere's AI, it translates English questions into properly formatted SQL queries.

## Features

- **Natural Language Queries**: Ask questions about your data in plain English
- **Interactive Database Explorer**: Browse available tables and their schema in the sidebar
- **Real-time Query Generation**: Converts questions to properly formatted PostgreSQL queries
- **Downloadable Results**: Export query results as CSV files
- **Schema-aware**: Adapts to your database structure automatically
- **Case-sensitive Handling**: Properly handles capitalization in database values

## Tech Stack

- **Streamlit**: Frontend web application
- **SQLAlchemy**: Database connection and query execution
- **PostgreSQL**: Database backend
- **Cohere AI**: Natural language processing for SQL generation
- **pandas**: Data manipulation and CSV export
- **Docker**: Containerization for easy deployment and sharing

## Requirements

- Python 3.7+
- PostgreSQL database
- Cohere API key
- Docker and Docker Compose (for containerized setup)

## Installation

### Local Setup

1. Clone this repository
2. Install required packages:

```bash
pip install -r requirements.txt
```

### Docker Setup

1. Ensure Docker and Docker Compose are installed on your system
2. Configure your `.env` file (see Configuration section)
3. Build and start the containers:

```bash
docker-compose up -d
```

## Configuration

Create a `.env` file in the project root with the following variables:

```
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=your_db_host  # Use "localhost" for local setup, no need to change for Docker
DB_PORT=your_db_port
DB_NAME=your_db_name
COHERE_API_KEY=your_cohere_api_key
```

## Usage

### Local Usage

1. Start the application:

```bash
streamlit run main.py
```

2. Open your browser and navigate to http://localhost:8501

### Docker Usage

1. Start the containers:

```bash
docker-compose up -d
```

2. Open your browser and navigate to http://localhost:8501

## Sharing Your Docker Container

To share your Docker container with others:

1. Make sure your Docker containers are running:

```bash
docker-compose up -d
```

2. For local network sharing, find your machine's IP address:

   - On macOS/Linux: `ifconfig` or `ip addr show`
   - On Windows: `ipconfig`

3. Others on your network can access the application at `http://<your-ip-address>:8501`

4. For cloud deployment:

   - Push your Docker image to Docker Hub:

   ```bash
   # Log in to Docker Hub
   docker login

   # Tag your images
   docker tag fetchaf-app yourusername/fetchaf-app:latest
   docker tag fetchaf-postgres yourusername/fetchaf-postgres:latest

   # Push images
   docker push yourusername/fetchaf-app:latest
   docker push yourusername/fetchaf-postgres:latest
   ```

   - Share your docker-compose.yml and .env template (remove sensitive data) with others

5. For database data persistence and sharing:

   - The Postgres data is stored in a Docker volume named `postgres_data`
   - To export your database for sharing:

   ```bash
   docker exec -t fetchaf-postgres pg_dump -U ${DB_USER} -d ${DB_NAME} > backup.sql
   ```

   - To import database data (on another system):

   ```bash
   # Start only the DB container
   docker-compose up -d db

   # Wait for DB to initialize
   sleep 10

   # Import data
   cat backup.sql | docker exec -i fetchaf-postgres psql -U ${DB_USER} -d ${DB_NAME}

   # Start the app container
   docker-compose up -d app
   ```

## Example Queries

- "Show all drivers from Germany"
- "Who are the top 5 drivers with the most points?"
- "What is the average age of drivers by nationality?"

## Troubleshooting

- **Database Connection Issues**: Check your database credentials in the `.env` file
- **API Key Error**: Ensure your Cohere API key is correctly set in the `.env` file
- **Query Errors**: Try rephrasing your question if you get unexpected results
- **Docker Issues**: Make sure ports 8501 and your DB_PORT are not in use by other applications

## License

MIT

## Contributors

- Your Name
