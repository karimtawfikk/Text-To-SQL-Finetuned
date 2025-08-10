import streamlit as st
from llama_cpp import Llama

st.set_page_config(page_title="SQL Generator", layout="centered")
st.title("🦥 Ask Anything, Get SQL — Powered by Mistral-7B")

MODEL_PATH = "model_gguf/unsloth.Q4_K_M.gguf"

@st.cache_resource
def load_mistral():
    return Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=8,
        n_gpu_layers=33,
    )

llm = load_mistral()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask a SQL-related question...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input:
    with st.chat_message("assistant"):
        with st.spinner("Generating SQL..."):

            db_info = (
                "CREATE SCHEMA IF NOT EXISTS company; "
                "CREATE TABLE IF NOT EXISTS company.departments ("
                "id INT PRIMARY KEY, name TEXT, budget INT); "

                "CREATE TABLE IF NOT EXISTS company.employees ("
                "id INT PRIMARY KEY, name TEXT, department_id INT, salary INT, hire_date DATE, "
                "FOREIGN KEY (department_id) REFERENCES company.departments(id)); "

                "CREATE TABLE IF NOT EXISTS company.projects ("
                "id INT PRIMARY KEY, name TEXT, start_date DATE, end_date DATE, budget INT); "

                "CREATE TABLE IF NOT EXISTS company.employee_projects ("
                "employee_id INT, project_id INT, "
                "FOREIGN KEY (employee_id) REFERENCES company.employees(id), "
                "FOREIGN KEY (project_id) REFERENCES company.projects(id)); "
            )

            full_prompt = (
                f"Below is an instruction that describes a task, paired with an input that provides further context. "
                f"Write a response that appropriately completes the request.\n\n"
                f"### Instruction:\n"
                f"Company database: {db_info}\n\n"
                f"### Input:\n"
                f"SQL Prompt: {user_input}\n\n"
                f"### Response:"
                f"### Explanation:"
            )

            
            response = llm.create_chat_completion(
            messages=full_prompt,
            max_tokens=256,
            temperature=0.7
            )

            output_text = response["choices"][0]["message"]["content"]
            st.markdown(output_text)

            st.session_state.chat_history.append({"role": "assistant", "content": output_text.strip()})
