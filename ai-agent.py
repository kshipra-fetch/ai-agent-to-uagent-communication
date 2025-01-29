import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from fetchai.crypto import Identity
from fetchai.registration import register_with_agentverse
from fetchai.communication import parse_message_from_agent, send_message_to_agent
import logging
from dotenv import load_dotenv
from uagents import Model

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
app = Flask(__name__)

CORS(app)

client_identity = None
agent_response = None

class Request(Model):
    message: str


def init_client():
    """Initialize and register the client agent."""
    global client_identity
    try:
        # Load the client identity from environment variables
        client_identity = Identity.from_seed("Sample AI AGENT SEED PHRASE", 0)
        logger.info(f"Client agent started with address: {client_identity.address}")

        # Define the client agent's metadata
        readme = """
        ![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)
                
        **Description**:  This AI Agent only communicates with an uAgent.
        
        **Input Data Model**
        ```
        class Request(Model):
            message: str
        ```
        
        **Output Data Model**
        ```
        class Response(Model):
            response: str
        ```
        """

        # Register the agent with Agentverse
        register_with_agentverse(
            identity=client_identity,
            url="http://localhost:5002/api/webhook",
            agentverse_token = os.getenv("AGENTVERSE_API_KEY"),
            agent_title="Sample AI Agent",
            readme=readme
        )

        logger.info("Client agent registration complete!")

    except Exception as e:
        logger.error(f"Initialization error: {e}")
        raise


@app.route('/request', methods=['POST'])
def send_data():
    """Send payload to the selected agent based on provided address."""
    global agent_response
    agent_response = None

    try:
        # Parse the request payload
        data = request.json
        payload = data.get('payload')  # Extract the payload dictionary
        target_address = "agent1qgyqf7l0djgvnd37f4fwvrv8xu7he2eatht328u05uy3vc9j33p7qe2dxtr" #run the uagent.py copy the address and paste here
        model_digest = Model.build_schema_digest(Request)

        # Send the payload to the specified agent
        send_message_to_agent(
            client_identity,  # Frontend client identity
            target_address,  # Agent address where we have to send the data
            payload,  # Payload containing the data
            model_digest=model_digest
        )

        return jsonify({"status": "request_sent", "payload": payload})

    except Exception as e:
        logger.error(f"Error sending data to agent: {e}")
        return jsonify({"error": str(e)}), 500



# app route to get recieve the messages on the agent
@app.route('/api/webhook', methods=['POST'])
def webhook():
    """Handle incoming messages from the dashboard agent."""
    global agent_response
    try:
        # Parse the incoming webhook message
        data = request.get_data().decode("utf-8")
        logger.info("Received response")
        message = parse_message_from_agent(data)
        agent_response = message.payload
        logger.info(f"Processed response: {agent_response}")
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    load_dotenv()
    init_client()
    app.run(host="0.0.0.0", port=5002)