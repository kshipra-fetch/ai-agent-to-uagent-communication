from uagents import Agent, Context, Model

class Request(Model):
    message: str

class Response(Model):
    response: str

# Instantiate the agent
agent = Agent(
    name="Sample uAgent",
    port=8000,
    seed="Sample uAgent SEED PHRASE",
    endpoint="http://localhost:8000/submit"
)

ai_agent_address="agent1qdaeq9k7ty2xjp5ylpex0ezxzlg30cc8n3lpvrgh4sqjm863hm0vusghkzu" #run the ai-agent.py file copy the address and paste it here

@agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info(f"My name is {ctx.agent.name} and my address is {agent.address}")

@agent.on_message(model=Request)
async def generic_message_handler(ctx: Context, sender: str, msg: Request):
    """
    Handler for any incoming message using the GenericModel.
    """
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    await ctx.send(ai_agent_address, Response(response="hey there!"))


if __name__ == "__main__":
    agent.run()