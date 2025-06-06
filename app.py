import streamlit as st
import sqlite3
import openai
import os
from dotenv import load_dotenv
import pandas as pd

# Load API key from environment or .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

item_translation = {
    "キーボード": "Keyboard",
    "マウス": "Mouse",
    "ノートパソコン": "Laptop",
    "タブレット": "Tablet",
    "モニター": "Monitor",
    "電話": "Phone"
    # Add more as needed
}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Text-to-SQL Chatbot")

# User input
user_query = st.text_input("Ask a question about your database:")

def get_schema():
    # Connect to DB and get schema info
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    schema = "\n".join([row[0] for row in cursor.fetchall()])
    conn.close()
    return schema

def ask_chatgpt(nl_query, schema):
    # Build context from chat history, including results
    context = ""
    for chat in st.session_state.chat_history[-3:]:  # last 3 exchanges
        context += f"User: {chat['user']}\nSQL: {chat['sql']}\n"
        if chat['results']:
            # Try to summarize the result if it's a list of names or cities
            if chat['columns'] and "name" in chat['columns']:
                names = [row[chat['columns'].index("name")] for row in chat['results']]
                context += f"Result: The names are {', '.join(str(n) for n in names)}\n"
            elif chat['columns'] and "city" in chat['columns']:
                cities = [row[chat['columns'].index("city")] for row in chat['results']]
                context += f"Result: The cities are {', '.join(str(c) for c in cities)}\n"
            else:
                context += f"Result: {chat['results']}\n"
        elif chat['error']:
            context += f"Error: {chat['error']}\n"
    prompt = f"""You are an assistant that converts natural language to SQL.
Given this database schema:
{schema}

Here is the recent conversation (including results):
{context}

When the user asks how many items a customer can afford, calculate it as the integer division of the customer's total amount (from the orders table) by the item's cost (from the stocks table), for the relevant city and item.

Example:
Q: How many keyboards can Bob afford?
A: SELECT FLOOR(
       (SELECT SUM(amount) FROM orders JOIN customers ON customers.id = orders.customer_id WHERE LOWER(customers.name) = 'bob')
       /
       (SELECT cost FROM stocks WHERE LOWER(item_name) = 'keyboard' AND city = (SELECT city FROM customers WHERE LOWER(name) = 'bob'))
   ) AS max_keyboards;

When the user uses pronouns like "they", "it", or "there", resolve them using the most recent relevant result from the conversation.

When filtering by names or text columns, always make the comparison case-insensitive (e.g., use LOWER(column) or COLLATE NOCASE).

Write an SQLite SQL query for: "{nl_query}"
Only output the SQL query, nothing else."""
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def run_sql(sql_query):
    try:
        conn = sqlite3.connect('mydatabase.db')
        df = None
        try:
            df = conn.execute(sql_query).fetchall()
            columns = [description[0] for description in conn.execute(sql_query).description]
            conn.close()
            return columns, df, None
        except Exception as e:
            conn.close()
            return None, None, str(e)
    except Exception as e:
        return None, None, str(e)

def translate_items(user_query):
    for jp, en in item_translation.items():
        user_query = user_query.replace(jp, en)
    return user_query

if user_query:
    user_query_translated = translate_items(user_query)
    schema = get_schema()
    sql_query = ask_chatgpt(user_query_translated, schema)
    columns, results, error = run_sql(sql_query)
    # Store the interaction
    st.session_state.chat_history.append({
        "user": user_query,
        "sql": sql_query,
        "results": results,
        "error": error,
        "columns": columns
    })
    st.code(sql_query, language='sql')
    if error:
        st.error(f"SQL Error: {error}")
    else:
        if results:
            df = pd.DataFrame(results, columns=columns)
            st.write("Results:")
            st.dataframe(df)

            # Only show chart options if there are numeric columns and at least 2 rows
            numeric_cols = df.select_dtypes(include='number').columns.tolist()
            if len(numeric_cols) >= 1 and len(df) > 1:
                st.subheader("Visualize the results")
                chart_type = st.selectbox("Choose chart type", ["Bar Chart", "Line Chart", "Area Chart"])
                x_axis = st.selectbox("X-axis", df.columns)
                y_axis = st.selectbox("Y-axis", numeric_cols)

                # If X and Y are the same, plot as a series
                if x_axis == y_axis:
                    plot_data = df[y_axis]
                else:
                    plot_data = df.set_index(x_axis)[y_axis]

                if chart_type == "Bar Chart":
                    st.bar_chart(plot_data)
                elif chart_type == "Line Chart":
                    st.line_chart(plot_data)
                elif chart_type == "Area Chart":
                    st.area_chart(plot_data)
            elif len(df) == 1:
                st.info("Not enough data to plot a chart. Try a query that returns multiple rows.")
        else:
            st.info("No results found.")

if st.button("Suggest Insights"):
    schema = get_schema()
    # Optionally, sample some data from each table
    conn = sqlite3.connect('mydatabase.db')
    sample_data = ""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables:
        cursor.execute(f"SELECT * FROM {table} LIMIT 3;")
        rows = cursor.fetchall()
        sample_data += f"\nSample data from {table}:\n{rows}\n"
    conn.close()

    prompt = f"""You are a data analyst assistant.
Given this database schema:
{schema}
{sample_data}

Suggest 5 interesting questions, analyses, or recommendations I could explore with this data. Output them as a numbered list."""
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    suggestions = response.choices[0].message.content.strip()
    st.markdown("### AI Suggestions & Recommendations")
    st.markdown(suggestions)

st.sidebar.title("Chat History")
for i, chat in enumerate(st.session_state.chat_history):
    st.sidebar.markdown(f"**Q{i+1}:** {chat['user']}")
    st.sidebar.code(chat['sql'], language='sql')
    if chat['error']:
        st.sidebar.error(f"SQL Error: {chat['error']}")
    elif chat['results']:
        st.sidebar.write("Results:", chat['results'])
    else:
        st.sidebar.info("No results found.")
