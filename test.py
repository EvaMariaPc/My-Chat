from langchain_community.agent_toolkits import OpenAPIToolkit, create_openapi_agent
from langchain_community.tools.json.tool import JsonSpec
from langchain_openai import OpenAI
import json

with open("flights_data.json") as f:
    data = json.load(f)
json_spec = JsonSpec(dict_=data, max_value_length=4000)


openapi_toolkit = OpenAPIToolkit.from_llm(
    OpenAI(temperature=0), json_spec, openai_requests_wrapper, verbose=True
)
openapi_agent_executor = create_openapi_agent(
    llm=OpenAI(temperature=0),
    toolkit=openapi_toolkit,
    allow_dangerous_requests=ALLOW_DANGEROUS_REQUEST,
    verbose=True,
)