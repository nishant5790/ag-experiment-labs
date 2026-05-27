# Aion-ai

Aion-ai is an AI research assistant platform combining a powerful Python-based AgentOS backend with a beautiful, fully-responsive React UI.

The system allows you to dynamically interact with AI Agents, Teams, and Workflows that stream their reasoning and execution steps back to the interface in real-time.

## Prerequisites

Before running the application, make sure you have the following installed:
- **Python 3.10+**
- **Node.js 18+** & **npm**

---

## 1. Starting the Backend Server

The backend is built with FastAPI and AgentOS, serving as the execution engine for all AI workflows. 

To start the backend, open a terminal window and run:

```bash
# Navigate to the project root directory
cd /Users/kumarnishant/PycharmProjects/ag-experiment-labs

# Run the AgentOS python file
python src/ag-os.py
```

**Note:** The backend server will start on `http://localhost:8000`. 
- You can access the API documentation at `http://localhost:8000/docs`.

---

## 2. Starting the Frontend React UI

The frontend is built using React and Vite, featuring dynamic glassmorphic design and real-time Server-Sent Events (SSE) streaming.

Open a **new** terminal window (keep the backend running in the first one) and run:

```bash
# Navigate to the React UI directory
cd /Users/kumarnishant/PycharmProjects/ag-experiment-labs/agent-react-ui

# Install dependencies (only required the very first time)
npm install

# Start the Vite development server
npm run dev
```

**Note:** The UI development server will start on `http://localhost:5173`. 
- Open your browser to `http://localhost:5173` to interact with Aion-ai.
- The UI proxy is pre-configured to automatically forward `/agents`, `/teams`, and `/workflows` requests securely to the backend on port `8000`.

---

## Features

- **Full-Screen Workspace**: A distraction-free UI utilizing 100% of your screen for deep work.
- **Dynamic Endpoints**: Seamlessly loads your available workflows, agents, and teams from the backend.
- **Real-Time Streaming**: Watch the models think, plan, and call tools in real-time.
- **Markdown Rendering**: Fully parsed markdown outputs displaying tables, code snippets, lists, and formatting.
- **History Management**: Clear chat history instantly without rebooting the server.
