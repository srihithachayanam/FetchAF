import streamlit as st
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.sql.schema import Table
from langchain_community.utilities.sql_database import SQLDatabase
import os
from dotenv import load_dotenv
import pandas as pd
import time
import cohere  
import re

load_dotenv()


st.set_page_config(layout="wide", page_title="FetchAF", page_icon=":bar_chart:")


db_status = st.empty()

db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "delusional")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "postgres")

# Connect to PostgreSQL using SQLAlchemy
def get_db_engine():
    try:
        db_status.info("Connecting to database...")
        connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(connection_string, pool_pre_ping=True, pool_recycle=3600)
        db_status.success("Database connected!")
        time.sleep(0.5)
        db_status.empty()
        return engine
    except Exception as e:
        db_status.error(f"Database connection error: {str(e)}")
        return None


engine = get_db_engine()
if engine:
    db = SQLDatabase(engine)
else:
    st.error("Failed to establish database connection. Please check your connection settings.")

# Get schema information
@st.cache_data(ttl=3600)
def get_simplified_schema():
    if not engine:
        return {}
        
    try:
        tables_info = {}
        schema = "public"
        
        inspector = inspect(engine)
        tables = inspector.get_table_names(schema='public')
        
        for table in tables:
            columns = []
            for col in inspector.get_columns(table, schema='public'):
                columns.append((col['name'], str(col['type'])))
            tables_info[table] = columns
        
        return {"public": tables_info}
    except Exception as e:
        st.warning(f"Error getting schema: {str(e)}")
        return {"public": {}}

# Execute SQL query
def run_query(sql_query):
    if not engine:
        return []
        
    try:
        with engine.connect() as connection:
            result_proxy = connection.execute(text(sql_query)) 
            columns = list(result_proxy.keys())
            # Fetch all rows
            results = result_proxy.fetchall()
            
            if not results:
                return []
                
            return [dict(zip(columns, row)) for row in results]
    except Exception as e:
        st.error(f"Query failed: {str(e)}")
        return []

def generate_sql_query(question, tables_info, timeout=15):
    table_name = "f1drivers_dataset" # default
    
    schema_info = ""
    all_identifiers = set() 
    
    # Get sample data for the prompt to show correct values
    sample_values = ""
    
    for schema, tables in tables_info.items():
        if schema == "public" and tables:
            for table, columns in tables.items():
                all_identifiers.add(table)
                schema_info += f"Table: {table}\n"
                columns_list = []
                for name, type_info in columns:
                    all_identifiers.add(name)
                    columns_list.append(f'{name}')
                schema_info += f"Columns: {', '.join(columns_list)}\n\n"
    
    api_key = os.getenv("COHERE_API_KEY", "").strip()
    if not api_key:
        st.error("Cohere API key not found in .env file. Please add COHERE_API_KEY=your_key to your .env file (without spaces around =).")
        return f'SELECT * FROM "{table_name}" LIMIT 10;'
    
    try:
        # Create a direct cohere client
        co = cohere.Client(api_key)
        
        # Create a simple, direct prompt with PostgreSQL specific instructions
        prompt = f"""Generate a PostgreSQL query to answer this question: "{question}"

Database Schema:
{schema_info}

CRITICAL FORMATTING RULES FOR POSTGRESQL:
1. Every column name and table name MUST always be enclosed in double quotes (")
2. Example: SELECT "Driver" FROM "f1drivers_dataset" WHERE "Driver" = 'Max Verstappen';
3. String values and literal values must be in single quotes (')
4. Return ONLY the raw SQL query without any explanations, markdown, or code blocks.
5. The coulmn name are case-sensitive.Make sure not to change them.

IMPORTANT INFORMATION ABOUT THE DATA:
- All text values are case-sensitive and properly capitalized in the database
- Driver names are stored as "Max Verstappen" (not "max verstappen")
- Country names are stored with proper capitalization: "Italy", "Netherlands", "Germany" (not lowercase)
- {sample_values}

Your query:"""

        # Call the Cohere API directly
        response = co.chat(
            message=prompt,
            model="command",
            temperature=0.2
        )
        
        ################################
        sql_query = response.text.strip()
        ################################

        if "```sql" in sql_query:
            start = sql_query.find("```sql") + 6
            end = sql_query.find("```", start)
            if end != -1:
                sql_query = sql_query[start:end].strip()
        elif "```" in sql_query:
            start = sql_query.find("```") + 3
            end = sql_query.find("```", start)
            if end != -1:
                sql_query = sql_query[start:end].strip()
        
        if "SELECT" in sql_query:
            select_pos = sql_query.find("SELECT")
            sql_query = sql_query[select_pos:].strip()
            
            # Find last semicolon if there's text after it
            semicolon_pos = sql_query.rfind(";")
            if semicolon_pos != -1 and semicolon_pos < len(sql_query) - 1:
                sql_query = sql_query[:semicolon_pos+1]
        
        # Add semicolon if missing
        if not sql_query.endswith(";"):
            sql_query += ";"
            
        # Fix quote issues
        sql_query = sql_query.replace("`", "\"")
        
        for identifier in all_identifiers:
            pattern = r'\b{}\b(?!")'.format(re.escape(identifier))
            sql_query = re.sub(pattern, f'"{identifier}"', sql_query, flags=re.IGNORECASE)
        
        while '"""' in sql_query:
            sql_query = sql_query.replace('"""', '"')
        
        while '""' in sql_query:
            sql_query = sql_query.replace('""', '"')
            
        country_capitalization = {
            "'netherlands'": "'Netherlands'",
            "'italy'": "'Italy'",
            "'germany'": "'Germany'",
            "'france'": "'France'",
            "'spain'": "'Spain'",
            "'australia'": "'Australia'",
            "'belgium'": "'Belgium'",
            "'brazil'": "'Brazil'",
            "'finland'": "'Finland'",
            "'united kingdom'": "'United Kingdom'",
            "'uk'": "'UK'",
            "'england'": "'England'"
        }
        
        for lowercase, capitalized in country_capitalization.items():
            sql_query = sql_query.replace(lowercase, capitalized)
            
        return sql_query
        
    except Exception as e:
        st.error(f"Error from Cohere: {str(e)}")
        st.write("API Key used:", api_key[:4] + "..." + api_key[-4:]) # Show part of key to debug
        return f'SELECT * FROM "{table_name}" LIMIT 10;'

# Get schema early
schema = get_simplified_schema()

# Main app UI with sidebar
with st.sidebar:
    st.title("Database Explorer")
    st.write(f"Connected to: {db_host}/{db_name}")
    
    if schema and "public" in schema and schema["public"]:
        st.subheader("Available Tables")
        for table_name, columns in schema["public"].items():
            with st.expander(f"📊 {table_name}"):
                # Display the column names
                st.write("**Columns:**")
                for col in columns:
                    st.write(f"- {col[0]} ({col[1]})")
                
                # Add a button to preview the table
                if st.button(f"Preview {table_name}", key=f"preview_{table_name}"):
                    try:
                        query = f"SELECT * FROM {table_name} LIMIT 5;"
                        with engine.connect() as conn:
                            result = conn.execute(text(query))
                            df = pd.DataFrame(result.fetchall(), columns=result.keys())
                            st.dataframe(df, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error previewing table: {str(e)}")
    else:
        st.warning("No tables found or schema information unavailable.")

# Main content area
st.title("FetchAF")

# Question input
question = st.text_input("Enter your question about your data:", placeholder="e.g., Show top customers by volume")

if st.button("Generate Report", type="primary"):
    if not question:
        st.warning("Please enter a question first.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Update progress
        status_text.text("Generating SQL query...")
        progress_bar.progress(25)
        
        # Generate SQL
        sql_query = generate_sql_query(question, schema)
        progress_bar.progress(75)
        
        if sql_query:
            st.subheader("SQL Query")
            st.code(sql_query, language="sql")
            
            status_text.text("Executing query...")
            progress_bar.progress(85)
            
            results = run_query(sql_query)
            progress_bar.progress(100)
            status_text.text("Done!")
            time.sleep(0.5)
            status_text.empty()
            
            if results:
                st.subheader("Results")
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)
                
                # Add CSV download option
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    f"query_results_{int(time.time())}.csv",
                    "text/csv"
                )
            else:
                st.info("Query returned no results. Try rephrasing your question.")
        else:
             # Clear progress if SQL generation failed
             progress_bar.empty()
             status_text.empty()