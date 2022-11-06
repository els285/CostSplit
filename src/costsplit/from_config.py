import yaml
import sys

from costsplit.Trip import Trip 
from costsplit.Person import Person 
from costsplit.Transaction import Transaction

def main():

    # Parse YAMl
    with open(sys.argv[1], "r") as stream:
        try:
            input_data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # Build Trip
    for trip_name,trip_data in input_data.items():

        list_of_attendees    = [Person(p) for p in trip_data["Attendees"]]
        list_of_transactions = [Transaction(t_name,t_data) for t_name,t_data in trip_data["Transactions"].items()]
        
        trip = Trip(trip_name=trip_name, 
                    attendees=list_of_attendees , 
                    transactions=list_of_transactions)

    trip.calculate()

main()

        







        
