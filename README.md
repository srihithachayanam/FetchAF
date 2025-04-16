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

## Requirements

- Python 3.7+
- PostgreSQL database
- Cohere API key

## Installation

1. Clone this repository
2. Install required packages:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables:

```
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
DB_NAME=your_db_name
COHERE_API_KEY=your_cohere_api_key
```

## Usage

1. Start the application:

```bash
streamlit run main.py
```

2. Open your browser and navigate to http://localhost:8501
3. Enter your question in the text input field
4. Click "Generate Report" to see the results

## Example Queries

- "Show all drivers from Germany"
- "Who are the top 5 drivers with the most points?"
- "What is the average age of drivers by nationality?"

## Troubleshooting

- **Database Connection Issues**: Check your database credentials in the `.env` file
- **API Key Error**: Ensure your Cohere API key is correctly set in the `.env` file
- **Query Errors**: Try rephrasing your question if you get unexpected results

## License

MIT

## Contributors

- Your Name
