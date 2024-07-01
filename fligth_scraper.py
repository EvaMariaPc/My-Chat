from dotenv import load_dotenv
import requests
from lxml import html
import logging

# Assuming langchain is the correct library, import necessary components
from langchain.llms import OpenAI
from langchain.chains import create_extraction_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

load_dotenv()  # Load environment variables from .env file

xpath_expressions = {
    "check": "//body//a",
    "destinations": "//body/div[@class='mb-sm grid auto-rows-picture-card gap-sm tb:mb-md tb:grid-cols-3 tb:gap-md de:grid-cols-4 xl:grid-cols-5']//a[@class='group relative flex h-full w-full flex-col justify-end overflow-hidden rounded-large shadow-action transition-shadow duration-normal hover:shadow-action-active'][@href]",
    "prices": "//your/xpath/for/prices"  # Replace with actual XPath
}

FLIGHT_DEALS = {}  # Define the schema for flight deals


def extract(content: str, schema: dict):
    try:
        llm = OpenAI()
        result = create_extraction_chain(schema=schema, llm=llm).run(content)
        if not isinstance(result, list):
            result = [result]
        return result
    except Exception as e:
        logging.error(f"Error in extract: {e}")
        raise


def fetch_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def get_splits(documents):
    try:
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=10000, chunk_overlap=0
        )
        print(f"your splits are created by: {type(splitter).__name__}")
        return splitter.split_documents(documents)
    except TypeError as e:
        print(f"{e}")


def flight_deals_crawler_base_function(url):
    try:
        html_content = fetch_url(url)
        tree = html.fromstring(html_content)
        a_elements = tree.xpath(xpath_expressions["check"])
        elements = ' '.join([html.tostring(el, encoding='unicode') for el in a_elements])
        documents = [Document(page_content=elements, metadata={"source": url})]
        splits = get_splits(documents)
        extracted_data = []
        for split in splits:
            try:
                extracted = extract(content=split.page_content, schema=FLIGHT_DEALS)
                extracted_data.append(extracted)
            except Exception as e:
                logging.error(f"Error during extraction: {e}")
                print(f"Error during extraction: {e}")
        print(f"your extracted data: {extracted_data}")
        return extracted_data
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        print(f"Error scraping {url}: {e}")
        return []


class FlightScraper:
    def __init__(self, schema_file):
        self.schema_file = schema_file

    def extract_data(self, content: str):
        return extract(content, self.schema_file)

    def scrape_popular_flights(self):
        url = "https://www.kiwi.com/en/"
        response = fetch_url(url)
        print("Response status code:", response.status_code)  # Print status code
        response_text = response.text

        tree = html.fromstring(response_text)

        '''destination_xpath = xpath_expressions["destinations"]
        price_xpath = xpath_expressions["prices"]

        destination_elements = tree.xpath(destination_xpath)
        destinations = [element.text_content().strip() for element in destination_elements]
        print("Destinations:", destinations) '''

        a_elements=xpath_expressions["destinations"]
        price_elements = tree.xpath(a_elements)
        print(price_elements)
        prices = [element.text_content().strip() for element in price_elements]
        print("destinations:", prices)  # Print prices

        popular_flights = []
        for price in zip(prices):
            popular_flights.append({"departure": "Bucharest", "price": price})

        return popular_flights
