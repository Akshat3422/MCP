import asyncio
from langchain_groq import ChatGroq
from dotenv import load_dotenv

from mcp_use import MCPAgent,MCPClient
import os

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY") or ""

async def run_memory_chat():
    """Run a chat MCPAgent's built in conversation memory """
    config_file=r"C:\Users\user\Desktop\ML\MCP_Complete\server\weather.json"

    print("Initializing chat...")

    # Creating MCP Clientt and agent with memory enabled
    client=MCPClient.from_config_file(config_file)
    llm=ChatGroq(model="openai/gpt-oss-120b")

    # Create agent with memory enabled=True

    agent=MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True
    )
    print("\n===== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("==================================\n")

    try:
        # Main chat loop
        while True:
            # Get user input
            user_input = input("\nYou: ")

            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break

            # Check for clear history command
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            # Get response from agent
            print("\nAssistant: ", end="", flush=True)

            try:
                # Run the agent with the user input (memory handling is automatic)
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\nError: {e}")

    finally:
        # Clean up
        if client and client.sessions:
            await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(run_memory_chat())




