
euro2gbp = lambda  {|euro| euro/1.1738}
chf2gbp  = lambda  {|chf|  chf/1.12519}


class Regi_Expenses

    attr_reader :trip_name

    def initialize(trip_name)
        @trip_name = trip_name
    end 

    def update_petrol_tank(current_full_tank_cost)
        @current_full_tank_cost = current_full_tank_cost
        @octile_cost            = current_full_tank_cost/8
    end

    def toll_expenses(total_toll_cost)
        @total_toll_cost = total_toll_cost
    end 

    def assign(number_of_people,octile_usage,total_toll_cost)

        toll_expenses(total_toll_cost)
        @octile_usage = octile_usage
        @total_cost = @total_toll_cost + octile_usage*@octile_cost

        @individual_cost = @total_cost/number_of_people

        puts @individual_cost
    end


    def assign_with_weights(dic_of_people,octile_usage,total_toll_cost)

        toll_expenses(total_toll_cost)
        @octile_usage = octile_usage
        @total_cost = @total_toll_cost + @octile_usage*@octile_cost

        total_weight = 0

        dic_of_people.each_value {|value| total_weight += value} # This is a 

        normalised_cost = @total_cost/total_weight
        output_dic = {}
        dic_of_people.each do |person,weight|
            output_dic[person] = weight*normalised_cost
        end
        puts output_dic
    end 

end




