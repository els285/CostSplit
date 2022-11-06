class Settlement:

    def __init__(self,_from,_to,amount):
        self._from    = _from
        self._to      = _to 
        self.amount   = amount
        self.complete = False

    def mark_complete(self):
        self.complete = True
