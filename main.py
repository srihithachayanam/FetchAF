import streamlit as st
from sqlalchemy import create_engine, text, inspect
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline
from huggingface_hub import hf_hub_download
import time
import hashlib
from functools import lru_cache

# Load environment variables
load_dotenv()

# Database Connection
def get_db_connection():
    try:
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')
        
        db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(db_url)
        return engine
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return None

# Get Database Schema
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_db_schema():
    engine = get_db_connection()
    if not engine:
        return "Could not connect to database to extract schema"
    
    schema_info = []
    inspector = inspect(engine)
    
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        col_info = [f"{col['name']} ({col['type']})" for col in columns]
        schema_info.append(f"Table: {table_name}\nColumns: {', '.join(col_info)}")
    
    return "\n\n".join(schema_info)

# Execute SQL Query with caching
@st.cache_data(ttl=300)  # Cache for 5 minutes
def execute_sql_query(query_with_params):
    query, params = query_with_params
    engine = get_db_connection()
    if not engine:
        return None

    try:
        with engine.connect() as connection:
            result = connection.execute(text(query), params)
            columns = result.keys()
            rows = result.fetchall()
            return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        st.error(f"Query Execution Error: {e}")
        return None

# Load LangChain-compatible HF pipeline
@st.cache_resource
def load_langchain_llm():
    model_name =  "patrickNLP/Graphix-3B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    pipe = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=256,
        num_beams=5,
        early_stopping=True
    )
    return HuggingFacePipeline(pipeline=pipe)

# LangChain version of SQL generation
def generate_sql_query(natural_language, db_schema):
    try:
        llm = load_langchain_llm()

        prompt = PromptTemplate(
            input_variables=["schema", "question"],
            template="""
Given the following database schema:

{schema}

Translate the following natural language question into a valid SQL query:

Question: {question}
SQL:
""",
        )

        chain = LLMChain(llm=llm, prompt=prompt)

        response = chain.run({
            "schema": db_schema,
            "question": natural_language
        })

        # Clean SQL
        sql_query = response.strip()
        if "SELECT" in sql_query:
            sql_query = sql_query[sql_query.find("SELECT"):]
        if ";" in sql_query:
            sql_query = sql_query[:sql_query.rfind(";")+1]

        return sql_query
    except Exception as e:
        st.error(f"LangChain SQL generation failed: {e}")
        return None

# Visualization Function
def create_visualization(df, graph_type, x_column=None, y_column=None):
    if df is None or df.empty:
        return None

    graph_mapping = {
        "Bar Chart": px.bar,
        "Line Chart": px.line,
        "Scatter Plot": px.scatter,
        "Pie Chart": px.pie,
        "Boxplot": px.box,
        "Area Chart": px.area,
        "Histogram": px.histogram
    }

    # If columns aren't specified, try to determine appropriate ones
    if x_column is None:
        x_column = df.columns[0] if len(df.columns) > 0 else None
    if y_column is None and graph_type != "Pie Chart" and graph_type != "Histogram":
        numeric_cols = df.select_dtypes(include=['number']).columns
        y_column = numeric_cols[0] if len(numeric_cols) > 0 else None

    try:
        if graph_type == "Pie Chart":
            if x_column and y_column:
                return px.pie(df, names=x_column, values=y_column, title=f"{graph_type}")
            return None
        elif graph_type == "Histogram":
            if x_column:
                return px.histogram(df, x=x_column, title=f"{graph_type}")
            return None
        else:
            if x_column and y_column:
                return graph_mapping[graph_type](
                    df, 
                    x=x_column, 
                    y=y_column, 
                    title=f"{graph_type}"
                )
            return None
    except Exception as e:
        st.error(f"Visualization Error: {e}")
        return None

def main():
    st.set_page_config(layout="wide", page_title="Natural Language to SQL")

    # Sidebar for query history
    st.sidebar.title("Query History")
    if "query_history" not in st.session_state:
        st.session_state.query_history = []
        st.session_state.query_results = {}

    for i, query in enumerate(st.session_state.query_history):
        if st.sidebar.button(f"{query[:30]}...", key=f"history_{i}"):
            st.session_state.current_nl_query = query
            st.session_state.current_sql = st.session_state.query_results.get(query, {}).get('sql', '')

    # App Header
    st.title("Natural Language to SQL Dashboard")
    st.write("Enter your question about the data, and the application will convert it to SQL, retrieve the data, and display visualizations.")

    # Get database schema for context
    db_schema = get_db_schema()
    
    # Only show schema in debug mode
    if st.sidebar.checkbox("Show Database Schema", False):
        st.sidebar.code(db_schema)

    # Natural Language Input
    st.subheader("Ask a Question")
    natural_language_input = st.text_area(
        "Enter your question:", 
        value=st.session_state.get("current_nl_query", ""), 
        height=100,
        placeholder="E.g., Show me the total sales by region"
    )

    if st.button("Generate & Run Query"):
        if natural_language_input:
            with st.spinner("Generating SQL and fetching results..."):
                # Generate SQL query
                sql_query = generate_sql_query(natural_language_input, db_schema)
                
                if sql_query:
                    st.session_state.current_nl_query = natural_language_input
                    st.session_state.current_sql = sql_query
                    
                    # Add to history if not already present
                    if natural_language_input not in st.session_state.query_history:
                        st.session_state.query_history.append(natural_language_input)
                    
                    # Create a unique key for caching
                    query_hash = hashlib.md5(sql_query.encode()).hexdigest()
                    
                    # Execute query
                    results = execute_sql_query((sql_query, {}))
                    
                    # Store in session state
                    if natural_language_input not in st.session_state.query_results:
                        st.session_state.query_results[natural_language_input] = {}
                    
                    st.session_state.query_results[natural_language_input]['sql'] = sql_query
                    st.session_state.query_results[natural_language_input]['data'] = results
                    
                    # Force reload to show results
                    st.experimental_rerun()
                else:
                    st.error("Failed to generate SQL query from your question.")
        else:
            st.warning("Please enter a question first.")

    # Display current SQL query and results if available
    if hasattr(st.session_state, 'current_sql') and st.session_state.current_sql:
        sql_query = st.session_state.current_sql
        
        st.subheader("Generated SQL Query")
        st.code(sql_query, language="sql")
        
        # Get results if available
        current_query = st.session_state.get("current_nl_query", "")
        results = None
        
        if current_query in st.session_state.query_results:
            results = st.session_state.query_results[current_query].get('data')
        
        if results is not None and not results.empty:
            st.subheader("Query Results")
            st.dataframe(results)
            
            # Visualization options
            st.subheader("Visualization")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                graph_type = st.selectbox(
                    "Select chart type:", 
                    ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", 
                     "Boxplot", "Area Chart", "Histogram"]
                )
            
            with col2:
                x_column = st.selectbox("Select X-axis column:", results.columns)
            
            with col3:
                numeric_cols = results.select_dtypes(include=['number']).columns.tolist()
                if not numeric_cols:
                    numeric_cols = results.columns.tolist()
                y_column = st.selectbox("Select Y-axis column (for numeric charts):", numeric_cols) if graph_type != "Histogram" else None
            
            fig = create_visualization(results, graph_type, x_column, y_column)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Could not create visualization with the selected options.")
                
            # Export options
            if st.button("Export to CSV"):
                csv = results.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"query_results_{int(time.time())}.csv",
                    mime="text/csv",
                )
        elif results is not None:
            st.info("Query executed successfully, but returned no results.")

if __name__ == "__main__":
    main()
