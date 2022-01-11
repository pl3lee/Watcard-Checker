from watcard import *
import datetime
if __name__ == '__main__':
    print("Please enter your Student ID number:")
    id = input()
    print("Please enter your password:")
    password = input()
    w1 = Watcard(id, password)
    print("What do you want to do today?")
    print("Enter \'b\' if you want to check your balance check your balance.")
    print("Enter \'t\' if you want to check your transactions.")
    while True:
        ans = input()
        if ans == 'b':
            w1.print_balance()
            break
        elif ans == 't':
            print("Do you want to see your transactions from the last 30 days, 60 days, or would you like to input a range?")
            print("Enter \'30\' if you want to check for your transactions from the last 30 days.")
            print("Enter \'60\' if you want to check for your transactions from the last 60 days.")
            print("Enter \'range\' if you want to check for your transactions from the last 60 days.")
            while True:
                ans = input()
                if ans == '30':
                    w1.print_transactions30()
                    break
                elif ans == '60':
                    w1.print_transactions60()
                    break
                elif ans == 'range':
                    print("Please indicate the start date (format: 'MM/DD/YYYY): '")
                    start = None
                    end = None
                    while True:
                        start = input()
                        try:
                            date = datetime.datetime(int(start[6:10]), int(start[0:2]), int(start[3:5]))
                            break
                        except:
                            print("Invalid input, please try again.")   
                    print("Please indicate the end date (format: 'MM/DD/YYYY): '")
                    while True:
                        end = input()
                        try:
                            date = datetime.datetime(int(end[6:10]), int(end[0:2]), int(end[3:5]))
                            break
                        except:
                            print("Invalid input, please try again.")
                    w1.print_transactions_range(start, end)   
                    break
                else:
                    print("Invalid input, please try again.")
            print('=================================')
            print("Do you want a frequency chart of your transactions in your selected range?")
            print("\'y\' for yes, \'n\' for no.")
            while True:
                ans = input()
                if ans == 'y' or ans == 'Y':
                    w1.graph(w1.most_recent_lookup)
                    break
                elif ans == 'n' or ans == 'N':
                    break
                else:
                    print("Invalid input, please try again.")
            break
        else:
            print("Invalid selection. Please try again.")