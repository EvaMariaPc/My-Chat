from llama_index.core import ServiceContext, VectorStoreIndex, download_loader
from llama_index.llms.openai import OpenAI
from typing import Optional
from dotenv import load_dotenv
import json

load_dotenv()

query = '''Extract all the flights and the data of departure and arrive from the provided site. Provide them as follows: { "Departure":"departure_name","Destination":"destination_name", "Flight_price":int, "Outbound":["day_of_the_week", day_of_the_month, "name_of_the_month", hour], "Inbound":["day_of_the_week", day_of_the_month, "name_of_the_month", hour]}. If you get loading, try again.'''


def extract_information_from_url(restaurant_url: str, query: str) -> Optional[str]:
    try:
        bs_web_reader = download_loader("BeautifulSoupWebReader")
        loader = bs_web_reader()
        documents = loader.load_data(urls=[restaurant_url])
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-4o-2024-05-13", temperature=0))
        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine(service_context=service_context)
        response = query_engine.query(query)

        # Log the response for debugging purposes
        print("Response:", response.response)

        return response.response

    except Exception as e:
        print("Error occurred:", e)
        return None


def parse_string(menu_string: str):
    try:
        return json.loads(menu_string)
    except json.JSONDecodeError as e:
        print("Error occurred while parsing flight string:", e)
        return None


def save_to_json(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Error occurred while saving to JSON file:", e)

