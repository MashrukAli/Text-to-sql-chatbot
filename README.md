# Text-to-sql-chatbot
A chatbot that generates sql and shows output from the database based on natural language questions. 





Legend:
• A: User interacts via web browser.
• B: Streamlit app (your main Python file).
• C: Database (local or cloud, e.g., SQLite, Postgres, MySQL).
• D: OpenAI API for natural language to SQL.
• E: CSV files for data import/export.
• F: .env file for secrets.
• G: Session state for chat memory.

2. Step-by-Step Setup Instructions
A. Prerequisites
• Python 3.8+
• pip (Python package manager)
• OpenAI API key
B. Clone/Download the Project

bash

Apply to app.py
C. Set Up a Virtual Environment

bash

Apply to app.py
Run
git clone <your-repo-url>
cd ml-agent
D. Install Dependencies

bash

Apply to app.py
Run
python3 -m venv .venv
source .venv/bin/activate
E. Prepare Your Data
• Place your mydatabase.db, orders.csv, customers.csv, and stocks.csv in the project directory.
• If you need to import CSVs into SQLite, use the .import command in the SQLite shell.
F. Set Up Your OpenAI API Key
• Create a .env file in the project root:

shellscript

Apply to app.py
pip install streamlit openai python-dotenv pandas
G. Run the App

bash

Apply to app.py
Run
  OPENAI_API_KEY=sk-...
• The app will open in your browser (usually at http://localhost:8501).

3. Manual (User & Developer Guide)
A. User Manual
• Ask a Question:
Type a natural language question about your data (e.g., "Show me all orders from Paris") and press Enter.
• View Results:
The app will display the generated SQL, the results, and (if applicable) chart options.
• Visualize Data:
If your query returns multiple rows and numeric columns, you can select chart types and axes to visualize the data.
• Chat History:
The sidebar shows your previous questions, SQL, and results.
• Suggest Insights:
Click the "Suggest Insights" button to get AI-generated ideas for exploring your data.
B. Developer Manual
• Add More Data:
Update your CSVs and re-import them into the database as needed.
• Change Database:
Modify the connection string in app.py to use Postgres, MySQL, etc.
• Customize AI Behavior:
Edit the prompt in ask_chatgpt to guide the AI for your use case.
• Add More Translations:
Update the item_translation dictionary for more language support.
• Extend Functionality:
Add new Streamlit widgets, backend endpoints, or ML features as needed.

4. Tech Stack
Layer	Technology	Purpose
Frontend	Streamlit	Web UI, charts, user input
Backend	Python	App logic, data processing, API calls
Database	SQLite (default)	Data storage (can swap for Postgres/MySQL)
AI/ML	OpenAI API	Natural language to SQL, suggestions
Data Import	CSV	Initial data loading
Secrets Mgmt	python-dotenv	API key management
Data Science	pandas	Data manipulation, DataFrame support

5. How It Works (Step-by-Step)
1. Python & pip Installation
On Ubuntu/Debian (WSL, Linux):

bash

Apply to app.py
Run
# Update package list
sudo apt update

# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv

# Check versions
python3 --version
pip3 --version

2. Virtual Environment Setup

bash

Apply to app.py
Run
# Create a virtual environment named .venv
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# (To deactivate later)
deactivate

3. Install Required Python Libraries

bash

Apply to app.py
Run
pip install streamlit openai python-dotenv pandas
• If you use other databases:
• For PostgreSQL: pip install psycopg2-binary
• For MySQL: pip install pymysql
• For SQLAlchemy (ORM): pip install sqlalchemy

4. SQLite Installation & Usage
Install SQLite (if not already installed):

bash

Apply to app.py
Run
sudo apt install sqlite3
Basic SQLite Commands:

bash

Apply to app.py
Run
# Open a database (creates it if it doesn't exist)
sqlite3 mydatabase.db

# Show tables
.tables

# Show schema for a table
.schema tablename

# Run a SQL query
SELECT * FROM tablename;

# Import CSV into a table
.mode csv
.import filename.csv tablename

# Exit SQLite shell
.exit

5. Running the Streamlit App

bash

Apply to app.py
Run
# From your project directory (with .venv activated)
streamlit run app.py
• The app will open in your browser at http://localhost:8501

1. User enters a question in the Streamlit web app.
2. App translates (if needed) and sends the question, schema, and context to OpenAI.
3. OpenAI returns an SQL query (or suggestion).
4. App runs the SQL on the database and fetches results.
5. Results and SQL are displayed in the app, with charting options if applicable.
6. Chat history is updated in the sidebar.
7. User can request AI suggestions for further exploration.

6. Extending/Deploying
• Deploy to the cloud:
Use Streamlit Cloud, Heroku, AWS, or Azure for public access.
• Switch to a production database:
Change the connection string and install the appropriate driver.
• Add authentication:
Use Streamlit’s secrets or a custom login system.
• Integrate with other platforms:
Embed the app in Salesforce, SharePoint, or other portals via iframe.
![image](https://github.com/user-attachments/assets/a4f636fe-9c6e-4abf-b97c-2034107ba940)
