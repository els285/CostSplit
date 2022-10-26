class Person

    '''
    Person class
    '''

    attr_reader :name
    
    def initialize(name)
        @name = name
        @net        = 0
        @net_paid   = 0
        @net_due    = 0
        @payments   = {}
        @expenses   = {}

        @splitwise_net = 0
        @paid_by = {}
        @paid_to = {}
    end

    def add_payment(new_payment)
    end 

    def add_expense(new_expense)
    end

end


ethan = Person.new("Ethan")


puts ethan.inspect