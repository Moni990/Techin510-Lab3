import os
from dataclasses import dataclass
import streamlit as st

import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Establish a connection to the database
con = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = con.cursor()

# Create the table if it does not exist
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS prompts (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        prompt TEXT NOT NULL,
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    )
    """
)
con.commit()

@dataclass
class Prompt:
    id: int = None
    title: str = ""
    prompt: str = ""

def upsert_prompt(prompt):
    if prompt.id is None:
        cur.execute(
            "INSERT INTO prompts (title, prompt) VALUES (%s, %s) RETURNING id",
            (prompt.title, prompt.prompt)
        )
        prompt.id = cur.fetchone()[0]
        con.commit()
        return "Prompt added successfully!"
    else:
        cur.execute(
            "UPDATE prompts SET title = %s, prompt = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
            (prompt.title, prompt.prompt, prompt.id)
        )
        con.commit()
        return "Prompt updated successfully!"

def prompt_form(key, prompt=Prompt()):
    with st.form(key=key):
        title = st.text_input("Title", value=prompt.title)
        prompt_text = st.text_area("Prompt", height=200, value=prompt.prompt)
        submitted = st.form_submit_button("Submit")
        if submitted and title and prompt_text:
            prompt.title = title
            prompt.prompt = prompt_text
            return prompt
        return None

st.title("Promptbase")
st.subheader("A simple app to store and retrieve prompts")

# Edit existing prompt
edit_id = st.session_state.get('edit_id', None)
if edit_id is not None:
    cur.execute("SELECT id, title, prompt FROM prompts WHERE id = %s", (edit_id,))
    data = cur.fetchone()
    if data:
        prompt = Prompt(*data)
        edited_prompt = prompt_form(f"prompt_{prompt.id}_edit", prompt)
        if edited_prompt:
            message = upsert_prompt(edited_prompt)
            st.success(message)
            del st.session_state['edit_id']  # Clear the edit state
else:
    # Add new prompt
    new_prompt = prompt_form("prompt_new")
    if new_prompt:
        message = upsert_prompt(new_prompt)
        st.success(message)

# Display prompts with edit and delete options
cur.execute("SELECT id, title, prompt FROM prompts ORDER BY created_at DESC")
prompts = cur.fetchall()
for p in prompts:
    with st.expander(p[1]):
        st.code(p[2])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Edit", key=f"edit_{p[0]}"):
                st.session_state['edit_id'] = p[0]
        with col2:
            if st.button("Delete", key=f"delete_{p[0]}"):
                cur.execute("DELETE FROM prompts WHERE id = %s", (p[0],))
                con.commit()
                st.experimental_rerun()
