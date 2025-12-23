# 🧠 AI Task Manager

A smart to-do list that thinks for you.

This project is a **Task Manager Application** that uses a local AI agent to help you complete your tasks. When you start a task, the AI searches the web for the best advice and generates a step-by-step action plan instantly.

**Powered by:** Python, Flask, Ollama (Llama 3.2), and DuckDuckGo Search.

## ✨ Features

* **Smart Planning:** specific, research-backed steps for any task (e.g., "Plan a bicep workout").
* **Live Web Search:** The AI uses DuckDuckGo to find real-time info (no outdated knowledge).
* **Local Privacy:** Runs entirely on your computer using Ollama.
* **Simple UI:** Clean interface built with Bootstrap 5.

## 🛠️ Prerequisites

Before running the project, make sure you have these installed:

1.  **Python 3.8+**
2.  **[Ollama](https://ollama.com/)** (to run the AI model locally).

## 🚀 Setup Guide

### 1. Prepare the AI
First, install Ollama and pull the model we are using. Open your terminal/command prompt and run:
```bash
ollama pull llama3.2


### 2. Install Python Dependencies

Install the required libraries for the web server and the agent:

pip install flask flask-cors strands duckduckgo-search requests


3. Run the Backend

Start the Python server. This listens for requests from the webpage:

python agent.py