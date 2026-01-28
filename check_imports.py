try:
    from langchain.agents import AgentExecutor
    print("AgentExecutor found in langchain.agents")
except ImportError as e:
    print(f"Error 1: {e}")

try:
    from langchain.agents.agent import AgentExecutor
    print("AgentExecutor found in langchain.agents.agent")
except ImportError as e:
    print(f"Error 2: {e}")

try:
    from langchain.agents import create_openai_functions_agent
    print("create_openai_functions_agent found in langchain.agents")
except ImportError as e:
    print(f"Error 3: {e}")
