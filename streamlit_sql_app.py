import streamlit as st
#changing the model and indexing the content for vector store
from llama_index.llms import OpenAI
llm = OpenAI(temperature=0, model="gpt-4-1106-preview")
#llm = OpenAI(temperature=0, model="gpt-3.5-turbo-1106")
from llama_index import ServiceContext

system_prompt="""You are an expert in salmon fish farming, salmon busines and 
    trade and fish business in general. You have the knowledge up until January 2024 inclusive.  
    You data is in SQL database, the schema is:
    date: datetime description: this is the date of the article
    header: str description: this is the header or the article
    tags: str description: this is tags to help you search, inlude companies, people, locations
    article: str description: actual article
    Limit yourself with maximum 20 artciles except the case where you are asked to provide the list of articles 
    """

service_context = ServiceContext.from_defaults(llm=llm, system_prompt=system_prompt )
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine
from llama_index import SQLDatabase

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
    column,
    text,
    inspect,
    sql
)


# Create an engine that connects to an existing SQLite database
engine = create_engine('sqlite:///salmon_articles1.db', future=True)


# Build query for SQL
sql_database = SQLDatabase(engine, include_tables=["articles_salmon"])
query_engine = NLSQLTableQueryEngine(sql_database=sql_database, service_context=service_context, tables=["articles_salmon"])

# Streamlit interface
#st.title()
st.markdown("<h2 style='text-align: justify; color: grey;'>Industry data about salmon fish farming and fish industry in general 🐠 🍣</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: justify; color: grey;'>The knowledge base is from 2021</h3>", unsafe_allow_html=True)

# Check for the session state key, initialize if not present
if 'history' not in st.session_state:
    st.session_state.history = []

# User input
prompt = st.text_input("Ask your question about here:", key="query_input", value="")

# Use a separate key for the submit button to avoid conflicts
submit_button = st.button('Submit Query', key='submit')

if submit_button and prompt:
    response = query_engine.query(prompt).response
    xxx=query_engine.query(prompt).metadata
    st.session_state.history.append({"Query": prompt, "Response": response})
    print(xxx)

# Display conversation history
st.subheader("Your chat history:")
for interaction in st.session_state.history:
    st.text(f"Q: {interaction['Query']}")
    st.markdown(f"A: {interaction['Response']}")




