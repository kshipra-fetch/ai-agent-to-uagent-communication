# AI Agent Communication using Fetch.ai SDK and uAgents

This repository demonstrates communication between an AI Agent created using the Fetch.ai SDK and a uAgent. The Fetch.ai agent sends messages to the uAgent, which processes the request and responds accordingly. 


## Prerequisites
Ensure you have the following installed:
- Python 3.11+
- Fetch.ai SDK (`uagents` and `fetchai` packages)
- Flask (for API server)
- `flask-cors` (for handling CORS issues)
- `python-dotenv` (for environment variables management)

Install dependencies using:
```bash
pip install requirements.txt
```
## Agent Communication

### AI Agent Endpoints 
| Endpoint      | Method | Description |
|--------------|--------|-------------|
| `/request`   | POST   | Sends a message to the uAgent |
| `/api/webhook` | POST | Receives responses from the uAgent |

Example payload for `/request`:
```json
{
    "payload": {"message": "Hello uAgent!"}
}
```

### uAgent Behavior
-Listens for incoming messages and logs them using the `@agent.on_message` handler.
-Sends a response message back to the Fetch.ai AI Agent using `await ctx.send()`.

### Request Data Model

To send a message to a uAgent from an SDK basd AI Agent to uAgent, the Request Data Model should be defined in both the scripts `(ai-agent.py and uagent.py)`.
```python
class Request(Model):
    message: str
```


## Setup and Execution

### Step 1: Run the Fetch.ai AI Agent
1. Open `ai-agent.py`.
2. Ensure you have the correct `AGENTVERSE_API_KEY` set in your `.env` file. Get the AGENTVERSE_API_KEY from [Agentverse](https://agentverse.ai/profile/api-keys)
3. Run the Fetch.ai AI Agent:
   ```bash
   python ai-agent.py
   ```
4. Copy the agent address from the logs.
5. Paste the ai-agent address in uagent.py at the following location.

```python
ai_agent_address="PASTE YOUR AI AGENT ADDRESS HERE"
```

### Step 2: Run the uAgent
1. Open `uagent.py`.
2. Run the uAgent:
   ```bash
   python uagent.py
   ```
3. Copy the uAgent address from the logs.
4. Paste the uAgent address in ai-agent.py at the following location

```python
uagent_address="PASTE YOUR UAGENT ADDRESS HERE"
```

### Step 4: Restart the Agents
After updating the addresses, restart both agents to establish communication.


### Step 5: Test the Communication

1. Once both agents are running and their addresses are updated, you can test the communication using the following curl command:
```bash
curl -X POST http://localhost:5002/request \
-H "Content-Type: application/json" \
-d '{
  "payload": {"message" : "hey"}
}'
```
2. The Fetch.ai AI Agent sends a request to the uAgent.

3. The uAgent receives and processes the request using the on_message handler.

4. The uAgent logs the received message:
```bash
INFO:     [Sample uAgent]: Received message from agent1qdaeq9k7ty2xjp5ylpex0ezxzlg30cc8n3lpvrgh4sqjm863hm0vusghkzu: hey
```
5. The uAgent sends a response back to the Fetch.ai AI Agent using await ctx.send().

6. The Fetch.ai AI Agent logs the received response:
```bash
INFO:__main__:Received response
INFO:__main__:Processed response: {'response': 'hey there!'}
```

