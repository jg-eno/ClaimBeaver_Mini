# ClaimBeaver Mini

ClaimBeaver Mini is a healthcare claims inquiry system that uses natural language processing to answer questions about healthcare claims data. The system uses a language model to convert natural language questions into SQL queries, execute them against a database, and provide human-readable answers.

## Project Structure

```
ClaimBeaver_Mini/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── inquiry_agent.py
│   │   └── routes.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── db_config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── static/
│   │   └── index.html
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── llm_service.py
│   │   └── query_utils.py
│   └── __init__.py
├── .env.example
├── main.py
├── README.md
└── requirements.txt
```

## Prerequisites

- Python 3.8 or higher
- MySQL database with healthcare claims data
- API key for either OpenAI or Google Gemini (depending on which LLM you want to use)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ClaimBeaver_Mini
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on the `.env.example` template:
   ```bash
   cp .env.example .env
   ```

5. Edit the `.env` file with your configuration:
   ```
   # For Google Gemini (Default)
   LLM_TYPE=gemini
   GOOGLE_API_KEY=your_google_api_key_here
   LLM_MODEL_NAME=gemini-2.0-flash

   # For OpenAI/LM Studio (uncomment these lines and comment out the Gemini ones)
   # LLM_TYPE=openai
   # OPENAI_API_KEY=your_openai_api_key_here
   # LLM_API_BASE=http://localhost:1234/v1  # For LM Studio
   # LLM_MODEL_NAME=llama-3.2-3b-instruct
   ```

## API Key Setup

### Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an account or log in
3. Generate a new API key
4. Add the key to your `.env` file as `GOOGLE_API_KEY`

### OpenAI API Key
1. Go to [OpenAI's platform](https://platform.openai.com/account/api-keys)
2. Create an account or log in
3. Generate a new API key
4. Add the key to your `.env` file as `OPENAI_API_KEY`

### LM Studio (Local Alternative)
1. Download and install [LM Studio](https://lmstudio.ai/)
2. Launch LM Studio and download a model (e.g., Llama 3.2)
3. Start the local server in LM Studio
4. Set `LLM_API_BASE` to the local server URL (typically `http://localhost:1234/v1`)
5. Set `OPENAI_API_KEY` to any non-empty string (e.g., `not-needed`)

## Running the Application

1. If using LM Studio:
   - Start LM Studio first
   - Load a model (e.g., Llama 3.2)
   - Start the local server in LM Studio (usually on port 1234)

2. Start the application:
   ```bash
   python main.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

The application will attempt to use the configured LLM (Google Gemini or OpenAI/LM Studio) and will fall back to the other option if the primary one fails.

## Switching Between LLM Providers

### Using Google Gemini (Default)
Edit your `.env` file to use Google Gemini:
```
LLM_TYPE=gemini
GOOGLE_API_KEY=your_google_api_key_here
LLM_MODEL_NAME=gemini-2.0-flash
```

### Using OpenAI/LM Studio
Edit your `.env` file to use OpenAI or a local model via LM Studio:
```
LLM_TYPE=openai
OPENAI_API_KEY=your_openai_api_key_here
LLM_API_BASE=http://localhost:1234/v1  # For LM Studio, or remove for OpenAI
LLM_MODEL_NAME=llama-3.2-3b-instruct  # Or any other model name
```

## Database Configuration

By default, the application connects to a MySQL database with the following connection string:
```
mysql+pymysql://root:password@localhost:3306/HealthInsuraceEnquirySystem
```

To use a different database, update the connection string in the `.env` file:
```
DB_CONNECTION_STRING=mysql+pymysql://username:password@host:port/database_name
```

## License

[MIT License](LICENSE)
