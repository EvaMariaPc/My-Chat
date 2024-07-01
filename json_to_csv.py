import json
import csv


def json_to_csv(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as jf:
        data = json.load(jf)

    with open(csv_file, 'w', newline='', encoding='utf-8') as cf:
        writer = csv.writer(cf)
        # Write the header
        writer.writerow(["Departure", "Destination", "Flight_price", "Outbound", "Inbound"])

        # Write the data
        for flight in data:
            departure = flight["Departure"]
            destination = flight["Destination"]
            flight_price = flight["Flight_price"]
            outbound = flight["Outbound"]
            inbound = flight["Inbound"]
            writer.writerow([departure, destination, flight_price, outbound, inbound])


json_file_path = 'lights_data.json'
csv_file_path = 'flights_data.csv'
