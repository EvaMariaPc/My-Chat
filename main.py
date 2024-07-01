from fligth_scraper import FlightScraper

if __name__ == "__main__":
    flight_scraper = FlightScraper("schema.json")
    popular_flights_data = flight_scraper.scrape_popular_flights()
    for flight in popular_flights_data:
        print(flight)
