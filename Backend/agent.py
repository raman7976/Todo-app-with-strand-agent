import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from ddgs import DDGS
from ddgs.exceptions import DDGSException, RatelimitException
from strands import Agent, tool
from strands_tools import http_request 
from strands.models.ollama import OllamaModel

# --- CONFIGURATION & SETUP ---

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains so your HTML file can access this

# Check Ollama connection
try:
    response = requests.get("http://localhost:11434/api/tags")
    print("✅ Ollama is running. Available models:")
    for model in response.json().get("models", []):
        print(f"- {model['name']}")
except requests.exceptions.ConnectionError:
    print("❌ Ollama is not running. Please start Ollama before proceeding.")

model_id = (
    "llama3.2"  # Change this to match your pulled model
)

ollama_model = OllamaModel(
    model_id=model_id,
    host="http://localhost:11434",
    max_tokens=4096,
    temperature=0.3,
    top_p=0.9,
)

# UPDATED SYSTEM PROMPT: Removed Memory/Mem0 references
SYSTEM_PROMPT = """
ROLE
You are a proactive Productivity & Lifestyle Assistant integrated into a Todo application. Your goal is to help the user not just list tasks, but execute them efficiently using external research.

1. CONTEXT: Rely on the information provided in the current conversation. If you lack context to give good advice, ask a clarifying question.
2. RESEARCH (DuckDuckGo): If a task requires external knowledge (e.g., "Fix a leaky faucet", "Find a vegan recipe", "Best way to learn React"), use the 'websearch' tool. Do not guess technical or real-time information.

- BE ACTIONABLE: Provide 10-12 clear, bulleted steps for every recommendation.
- BE CONCISE: Use Markdown for clarity. Avoid long conversational fillers.
- TONE: Professional, encouraging, and highly organized.

When providing a recommendation, follow this structure:
1. **Goal**: A 1-sentence summary of what we are achieving.
2. **Steps**: A numbered list of specific actions.
3. **Pro-Tip**: One extra piece of value-add advice based on search.

If a task is simple and personal (e.g., "Call Mom"), do not search the web. Simply provide a helpful reminder or a tip on how to make the call meaningful.
"""

@tool
def websearch(keywords: str, region: str = "in-en", max_results: int = 5) -> str:
    """Search the web for updated information.

    Args:
        keywords (str): The search query keywords.
        region (str): The search region: wt-wt, us-en, uk-en, ru-ru, etc..
        max_results (int | None): The maximum number of results to return.
    Returns:
        List of dictionaries with search results.
    """
    try:
        results = DDGS().text(keywords, region=region, max_results=max_results)
        return results if results else "No results found."
    except RatelimitException:
        return "Rate limit reached. Please try again later."
    except DDGSException as e:
        return f"Search error: {e}"

# Initialize agent
# Removed mem0_memory from tools and logic
memory_agent = Agent(
    system_prompt=SYSTEM_PROMPT,
    model=ollama_model,
    tools=[websearch],
)




# --- API ENDPOINTS ---


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    print(f"📩 Received task: {user_message}")
    
    try:
        # Run the agent
        # strands agents typically return the response string when called
        response = memory_agent(user_message)
        
        # If the agent returns an object, try to extract the text. 
        # If it returns a string directly, use it.
        final_response = str(response) 
        
        return jsonify({"response": final_response})

    except Exception as e:
        print(f"❌ Error generating response: {e}")
        return jsonify({"error": str(e)}), 500
    



if __name__ == "__main__":
    print("\n🚀 Server is running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)