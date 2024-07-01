import math
from datetime import datetime, timedelta
from langchain.agents import Tool


def math_tool(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": None}, {"math": math})
        return str(result)
    except Exception as e:
        return str(e)


def datetime_tool(operation: str) -> str:
    try:
        if operation == "current_time":
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif operation.startswith("add_days"):
            days = int(operation.split()[1])
            future_date = datetime.now() + timedelta(days=days)
            return future_date.strftime("%Y-%m-%d %H:%M:%S")
        elif operation.startswith("subtract_days"):
            days = int(operation.split()[1])
            past_date = datetime.now() - timedelta(days=days)
            return past_date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return "Invalid operation"
    except Exception as e:
        return str(e)


# Define the tools with clear names and descriptions
math_tool_instance = Tool(name="math", func=math_tool, description="Evaluates mathematical expressions.")
datetime_tool_instance = Tool(name="datetime", func=datetime_tool, description="Performs date and time operations.")

# List of all tool instances for agent_invoke
agent_tools = [math_tool_instance, datetime_tool_instance]


# Optionally, you can define a function to invoke tools
def agent_invoke(tool_name: str, input: str) -> str:
    for tool in agent_tools:
        if tool.name == tool_name:
            return tool.func(input)
    return "Tool not found"
