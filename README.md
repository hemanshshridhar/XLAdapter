# Excel Agent

Intelligent agent that adapts the excel model to provided data Excel files. It parses Excel sheets in a standard format and makes replacement/


## Prerequisites

- **Python** 3.10 or higher



## Installation



1. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**

   Create a `.env` file in the project root directory with the following content:

   ```dotenv

    OPENAI_API_KEY=<OpenAI API Key>

   ```

   **Note**: Do not commit the `.env` file to version control.

