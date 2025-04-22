# BusyBee Assistant

This Python Flask application provides a web interface for interacting with a multi-agent system. It leverages the `phi` library to create agents powered by Groq and Gemini models, enabling web searching and financial data analysis.

## Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.7 or higher:** You can download it from [python.org](https://www.python.org/downloads/).
* **pip:** Python package installer (usually comes with Python).

## Setup

1.  **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You might need to create a `requirements.txt` file with the following content if you don't have one)*:
    ```
    python-dotenv
    flask
    phi-ai
    yfinance
    duckduckgo-search
    ```

2.  **Set up environment variables:**
    Create a `.env` file in the same directory as your Python script and add your API keys:
    ```
    GROQ_API_KEY=YOUR_GROQ_API_KEY
    GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
    ```
    Replace `YOUR_GROQ_API_KEY` and `YOUR_GOOGLE_API_KEY` with your actual API keys. You'll need to obtain these from Groq and Google Cloud (for Gemini).

## Running the Application

1.  **Navigate to the application directory** in your terminal.

2.  **Run the Flask application:**
    ```bash
    python your_script_name.py
    ```
    *(Replace `your_script_name.py` with the actual name of your Python file, e.g., `app.py`)*

3.  **Open your web browser** and go to `http://127.0.0.1:5000/`.

You should see the "BusyBee Assistant" web interface.

## Using the Assistant

1.  **Enter your question** in the text area provided.
2.  **Click the "Submit" button.**
3.  The assistant will process your request using the configured multi-agent system and display the response below the button.

The assistant can perform tasks like:

* Searching the web for information.
* Analyzing financial data (stock prices, analyst recommendations, key ratios, company news).
* Combining information from web searches and financial analysis.

## Code Explanation

The Python script does the following:

* **Imports necessary libraries:** `sys`, `os`, `phi`, `dotenv`, `flask`.
* **Sets up UTF-8 encoding** for the console.
* **Loads environment variables** from the `.env` file.
* **Initializes three agents:**
    * `web_search_Agent`: Uses the Groq model and the DuckDuckGo tool for web searching.
    * `financial_analysis_Agent`: Uses the Gemini model and the YFinanceTools for financial data analysis.
    * `multi_model_Agent`: Orchestrates the `web_search_Agent` and `financial_analysis_Agent` using the Groq model.
* **Defines Flask routes:**
    * `/`: Renders the `index.html` page, providing the user interface.
    * `/ask`: Handles POST requests containing the user's question. It runs the `multi_model_Agent` with the question and streams the response back as a JSON object.
* **Creates `index.html` if it doesn't exist:** This provides a basic HTML interface with a text area for input and a div to display the response.
* **Runs the Flask development server** on `http://127.0.0.1:5000/`.

## Notes

* Ensure your API keys are kept secure and are not shared publicly.
* The `phi` library simplifies the creation and management of AI agents and tools.
* The `.env` file is crucial for managing sensitive information like API keys.
* The basic HTML interface in `index.html` can be further enhanced for a better user experience.
* The `stream=True` in `multi_model_Agent.run()` allows for a more interactive experience by displaying the response in chunks as it's generated.

This `README.md` should provide a good starting point for anyone looking to understand and run your application. Let me know if you have any other questions!
