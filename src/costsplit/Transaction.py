class Transaction:

    '''
    The Transaction class defines any one payment, in terms of those who paid and those who pariticipated in the transaction.
    They main point of the Transaction class is assigning payments and participation to Person through the assign_to_persons funciton.
    There is also a per_transaction_compute function which does an individual
    splitwise calculation 
    
        """
        type defines how the costs are split: 
            weights    = float weights
            real       = actual amount
            percentage = percentage
        """
    '''

    @staticmethod
    def compute_total(d):
        ''' Compute the sum of all values in a dictionary'''
        return sum(list(d.values()))

    def parse_participants(self,input_dict):

        """
        From an input dictionary of participants, compute their actual amounts
        """

        t_type  = input_dict.get("Type","Real")
        assert t_type in ["weights" , "real" , "percentage"] , "Please specify a legitimate type"
        people = {k:v for k,v in input_dict.items() if k!="Type" and k!="Total"}
        total = self.compute_total(people)

        return self.distribute_costs(t_type,people)
        

    def parse_payees(self,input_dict):

        '''
        From an input dictionary of payees, compute their actual amounts and the
        total cost
        '''

        t_type  = input_dict.get("Type","real")
        assert t_type in ["weights" , "real" , "percentage"] , "Please specify a legitimate type"
        people = {k:v for k,v in input_dict.items() if k!="Type" and k!="Total"}
        total = input_dict.get("total") #Defaults to none


        if t_type == "real":
            if total is None:
                total = self.compute_total(people)
            else:
                assert total==self.compute_total(), "Totals dont match"
                total = total

        if t_type != "real":
            assert total is not None, "Please specify a total"
            total = total

        self.total_cost = total

        return self.distribute_costs(t_type,people)


    def distribute_costs(self,t_type,people):

        if t_type == "real":
            true_people_dict = people 

        elif t_type == "weights":
            sum_weights = self.compute_total(people)
            f = lambda a: a/sum_weights*self.total_cost
            true_people_dict = {k:f(v) for k,v in people.items()}

        elif t_type == "percentage":
            f = lambda a: a/100*self.total_cost
            true_people_dict = {k:f(v) for k,v in people.items()}

        return true_people_dict


    def match_to_Person_object(self,list_of_Person_objects):
        for k,v in self.true_payees.items():
            for po in list_of_Person_objects:
                if po.name==k:
                    self.payees_oop[po] = v

        for k,v in self.true_participants.items():
            for po in list_of_Person_objects:
                if po.name==k:
                    self.participants_oop[po] = v


    def __init__(self,transaction_name,td):
        self.transaction_name   = transaction_name
        self.input_payees       = td["Payees"]
        self.input_participants = td["Participants"]
        self.additional_info    = td.get("Other",None)

        self.true_payees        = self.parse_payees(self.input_payees)
        self.true_participants  = self.parse_participants(self.input_participants)

        self.payees_oop         = {}
        self.participants_oop   = {}







