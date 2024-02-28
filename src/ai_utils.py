"""
Utility functions
"""

import re
from io import BytesIO
from PIL import Image
import tempfile
import streamlit as st
import pandas as pd

from langchain.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType

from pyairtable import Table

def extract_ids_from_base_url(base_url):
    """
    Extract base and table ID or name from the base URL using regular expressions
    """
    pattern = r'https://airtable.com/([\w\d]+)/(.*?)(?:/|$)'
    match = re.match(pattern, base_url)
  
    if match:
        base_id = match.group(1)
        table_id = match.group(2)

        return dict(base_id=base_id, table_id=table_id)
    else:
        raise ValueError("Invalid base URL")
    
def get_airtable_table(access_token, airtable_url):
    """
    Get Airtable Table
    """

    # Extract the base and table ID from the base URL
    ids_from_url = extract_ids_from_base_url(airtable_url) 
    base_id, table_id = ids_from_url['base_id'], ids_from_url['table_id']
    
    # Initialize Airtable Python SDK
    table = Table(access_token, base_id, table_id)

    return table
    
def airtable_to_df(access_token, airtable_url):
    """
    Convert Airtable contents into df
    """

    # Get airtable Table
    table = get_airtable_table(access_token, airtable_url)

    # Get all records from the table
    all_records = table.all()

    # Extract the data from the JSON response and create a pandas DataFrame
    rows = []
    for record in all_records:
        row = record['fields']
        row['id'] = record['id']
        rows.append(row)
    df = pd.DataFrame(rows)

    return df

def df_to_csv(df):
    """
    Convert df contents into csv
    """

    with tempfile.NamedTemporaryFile(dir="src/tables", delete=False, suffix=".csv") as tmp_file:
        df.to_csv(tmp_file.name, index=False)
    
    return tmp_file.name

def airtable_to_csv(access_token, airtable_url):
    """
    Convert Airtable contents into csv
    """

    df = airtable_to_df(access_token, airtable_url)

    return df_to_csv(df)

def run_agent(file_name, query, openai_key, openai_model_chosen):
    """
    Runs the agent on the given file with the specified query.
    """
    agent = create_csv_agent(ChatOpenAI(openai_api_key=openai_key, model=openai_model_chosen, temperature=0), file_name, verbose=True, agent_type=AgentType.OPENAI_FUNCTIONS, agent_executor_kwargs={"handle_parsing_errors":True})
    return agent.run(query).__str__()

def validate_api_key(api_key_input):
    """
    Validates the provided API key.
    """
    api_key_regex = r"^sk-"
    api_key_valid = re.match(api_key_regex, api_key_input) is not None
    return api_key_valid

def validate_pat(airtable_pat_input):
    """
    Validates the provided Airtable personal access token (PAT).
    """
    airtable_pat_regex = r"^pat"
    airtable_pat_valid = re.match(airtable_pat_regex, airtable_pat_input) is not None
    return airtable_pat_valid

def validate_base_url(airtable_base_url_input):
    """
    Validates the provided Airtable base URL.
    """
    airtable_base_url_regex = r"^https:\/\/airtable.com\/app[^\/]+\/tbl[^\/]"
    airtable_base_url_valid = re.match(airtable_base_url_regex, airtable_base_url_input) is not None
    return airtable_base_url_valid