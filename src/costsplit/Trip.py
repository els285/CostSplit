class Trip:

    def __init__(self,trip_name:str, attendees=None, transactions=None, **kwargs):
        self.trip_name          =   trip_name
        self.attendees          =   attendees or []       #  A list of participants 
        self.all_attendee_names = set([p.name for p in self.attendees])
        self.transactions       =   transactions or []    #  A list of transactions
        self.check_participants()

        self.credit_list = []
        self.debt_list   = []

        self.settlements = []

        # Attach the Person objects to the Transactions
        for trans in self.transactions:
            trans.match_to_Person_object(self.attendees)

        # Attach the Transactions to the Person objects
        for trans in self.transactions:
            for person in self.attendees:
                if person in trans.payees_oop:
                    spent_amount = trans.payees_oop[person]
                    person.add_payment(trans,spent_amount)
                if person in trans.participants_oop:
                    owe_amount = trans.participants_oop[person]
                    person.add_expense(trans,owe_amount)

        # Compute all individual totals plus net
        for person in self.attendees:
            person.self_total()
            if person.net >= 0:
                self.credit_list.append(person)
            else:
                self.debt_list.append(person)
    


    def check_participants(self):
        for trans in self.transactions:
            all_people_in_transaction = set(list(trans.true_payees.keys()) + list(trans.true_participants.keys()))
            spurious_participants = self.all_attendee_names.symmetric_difference(all_people_in_transaction)
            assert len(spurious_participants)==0, f"The following persons are defined in transactions but not in the trip: {spurious_participants}"


    def calculate(self):

        for indiv1 in self.credit_list:
                while indiv1.running_net > 0.00:
                    for indiv2 in self.debt_list:

                        if indiv2.running_net != 0.00:
                            difference = (indiv1.running_net + indiv2.running_net)

                            if difference >= 0.00:
                                paid = indiv1.running_net - difference
                                indiv1.running_net = difference
                                indiv2.running_net = 0.00
                                print(indiv2.name + " paid " + indiv1.name + " the amount of " + str(paid) )
                                indiv1.paid_by = {**indiv1.paid_by , **{indiv2 : paid}}
                                indiv2.paid_to = {**indiv2.paid_to , **{indiv1 : paid}}

                                self.settlements.append({"giver": indiv2,"recipient":indiv1,"amount":paid})
                            else:
                                paid = abs(indiv2.running_net - difference)
                                left = abs(difference)
                                indiv1.running_net = 0.00
                                indiv2.running_net = difference
                                indiv1.paid_by = {**indiv1.paid_by , **{indiv2 : paid}}
                                indiv2.paid_to = {**indiv2.paid_to , **{indiv1 : paid}}
                                if paid != 0:
                                    print(indiv2.name + " pays " + indiv1.name + " " + str(paid) + " but has " + str(left) + " left over")
                                    self.settlements.append({"giver": indiv2,"recipient":indiv1,"amount":paid})

                                else: 
                                    pass
                        else: 
                            pass




    # def add_participant(self,new_attendee):
    #     """ Append participant"""
    #     assert not new_attendee in self.attendees, f"Person {new_attendee} already added."
    #     self.participants.append(new_attendee)

    # def add_transaction(self,new_transaction):
    #     """ Append transaction """
    #     assert not new_transaction in self.transactions, f"Transaction {new_transaction} already added."
    #     self.transactions.append(new_transaction)


    def doOverallCalculation(self):
        self.credit_list,self.debt_list,self.splitwise


# from Person import Person

# Ethan = Person("Ethan")
# Fun = Trip(trip_name="LadyG" , attendees=[Ethan])
# print(Fun.__dict__)