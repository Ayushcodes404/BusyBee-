import sys
import os
os.system('chcp 65001')  # Set console to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

from phi.agent import Agent
from phi.model.groq import Groq
from phi.model.vertexai import Gemini
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

web_search_Agent = Agent(
    name="web_search",
    role="A helpful assistant that can search the web and return the results",
    tools=[DuckDuckGo()],
    model=Groq(api_key=groq_api_key, id="llama-3.3-70b-versatile", model_type="chat"),
    instruction=["Always provide the source"],
    show_tools_calls=True,
    markdown=True,
) 

financial_analysis_Agent = Agent(
    name="financial_analysis",
    role="A helpful assistant that can analyze financial data",
    model=Gemini(api_key=google_api_key, id="gemini-1.5-pro", model_type="chat"),
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, key_financial_ratios=True, company_news=True),
    ], 
    instruction=["Use table to show the financial data"],
    show_tools_calls=True,
    markdown=True
)

multi_model_Agent = Agent(
   teams=[web_search_Agent, financial_analysis_Agent],
   instructions=["Always provide the source","Use table to show the financial data"], 
   show_tools_calls=True,
   markdown=True,
   model=Groq(api_key=groq_api_key, id="llama-3.3-70b-versatile", model_type="chat")
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        question = request.json.get('question', '')
        response_chunks = []
        
        for chunk in multi_model_Agent.run(question, stream=True):
            if hasattr(chunk, 'content') and chunk.content:
                response_chunks.append(chunk.content)
            elif isinstance(chunk, str) and chunk.strip():
                response_chunks.append(chunk)
            elif isinstance(chunk, dict) and 'content' in chunk:
                response_chunks.append(chunk['content'])
        
        response = ''.join(response_chunks).strip()
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': f"Error processing request: {str(e)}"}), 500

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    
    if not os.path.exists('templates/index.html'):
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write('''<!DOCTYPE html>
<html>
<head>
    <title>BusyBee Assistant</title>
    <meta charset="utf-8">
    <style>
        body { max-width: 800px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif; }
        #response { white-space: pre-wrap; margin-top: 20px; }
        textarea { width: 100%; height: 100px; margin: 10px 0; }
        button { padding: 10px 20px; }
        .loading { opacity: 0.5; }
    </style>
</head>
<body>
    <h1>BusyBee Assistant</h1>
    <textarea id="question" placeholder="Ask your question here..."></textarea>
    <br>
    <button onclick="askQuestion()" id="submitBtn">Submit</button>
    <div id="response"></div>

    <script>
    async function askQuestion() {
        const question = document.getElementById('question').value;
        const responseDiv = document.getElementById('response');
        const submitBtn = document.getElementById('submitBtn');
        
        if (!question.trim()) return;
        
        responseDiv.innerHTML = 'Loading...';
        submitBtn.disabled = true;
        
        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({question: question})
            });
            
            const data = await response.json();
            if (data.error) {
                responseDiv.innerHTML = `Error: ${data.error}`;
            } else {
                responseDiv.innerHTML = data.response;
            }
        } catch (error) {
            responseDiv.innerHTML = `Error: ${error}`;
        } finally {
            submitBtn.disabled = false;
        }
    }
    </script>
</body>
</html>''')
    
    app.run(debug=True, port=5000, host='127.0.0.1')