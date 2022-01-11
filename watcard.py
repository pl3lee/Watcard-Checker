from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import matplotlib.pyplot as plt

class Transaction:
    def __init__(self, date, amount, location):
        self.date = date
        self.amount = amount
        self.location = location

    def __repr__(self):
        str = f'Date: {self.date}\nAmount: $ {self.amount}\nLocation: {self.location}'
        return str

class Balance:
    def __init__(self, name, credit, amount):
        self.name = name
        self.credit = credit
        self.amount = amount

    def __repr__(self):
        str = f'Name: {self.name}\nCredit: {self.credit}\nAmount: {self.amount}'
        return str

class Watcard:
    def __init__(self, studentID, password):
        self.studentID = studentID
        self.password = password
        self.transactions_60days = None
        self.transactions_30days = None
        self.transactions_recent_range = None
        self.most_recent_lookup = None
        self.balances = None
    
    # Prints out balance of Watcard
    # print_balance: None -> None
    def print_balance(self):
        if self.balances is not None:
            for balance in self.balances:
                print('=================================')
                print(balance)
            print('=================================')
            total = 0
            for balance in self.balances:
                balance.amount = balance.amount.replace(',', '')
                total += float(balance.amount[2:])
            print(f"Total Balance: {round(total, 2)}")
        else:
            self.balance()
            self.print_balance()

    # Prints out transactions of Watcard for the past 60 days.
    # print_transactions60: None -> None
    def print_transactions60(self):
        if self.transactions_60days is not None:
            #Prints out the transactions
            for transaction in self.transactions_60days:
                print('=================================')
                print(transaction)
        else:
            self.transactions_60()
            self.print_transactions60()

    # Prints out transactions of Watcard for the past 30 days.
    # print_transactions30: None -> None
    def print_transactions30(self):
        if self.transactions_30days is not None:
            #Prints out the transactions
            for transaction in self.transactions_30days:
                print('=================================')
                print(transaction)
        else:
            self.transactions_30()
            self.print_transactions30()
    
    # Prints out transactions of Watcard for the past 30 days.
    # print_transactions30: None -> None
    def print_transactions_range(self, start, end):
        self.transactions_recent_range = self.transactions_range(start, end)
        #Prints out the transactions
        for transaction in self.transactions_recent_range:
            print('=================================')
            print(transaction)

    # Scrapes the transactions page, where type is either 30, 60, or range.
    #   If type is range, then please specify the start and end date in the
    #   form of 'MM/DD/YYYY'.
    # transactions_scrape: Str Str Str -> List of Transaction
    def transactions_scrape(self, type, start = '0', end = '0'):
        print("Loading... Please be patient, this may take up to 1 minute")
        # Initializes Chromedriver
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('log-level=3')
        options.add_argument("--headless")
        browser = webdriver.Chrome(options = options)
        browser.maximize_window()
        browser.get('https://watcard.uwaterloo.ca/OneWeb/Account/LogOn')\
        
        # Login
        username_input = browser.find_element(By.XPATH, '//*[@id="Account"]')
        password_input = browser.find_element(By.XPATH, '//*[@id="Password"]')
        username_input.send_keys(self.studentID)
        password_input.send_keys(self.password)
        login_button = browser.find_element(By.XPATH, '//*[@id="oneweb_main_content"]/div[2]/div[3]/form/div/button')
        login_button.click()

        # Goes to Transactions page
        browser.find_element(By.XPATH, '//*[@id="ow-navbar-collapse"]/ul/li[2]/a').click()
        browser.find_element(By.XPATH, '//*[@id="ow-navbar-collapse"]/ul/li[2]/ul/li[3]/a').click()
        # Past 30 days
        if type == "30":
            browser.find_element(By.XPATH, '//*[@id="oneweb_main_content"]/div[2]/div/div/form/fieldset[1]/ul/li[1]/span').click()
        # Past 60 days
        elif type == "60":
            browser.find_element(By.XPATH, '//*[@id="oneweb_main_content"]/div[2]/div/div/form/fieldset[1]/ul/li[2]/span').click()
        # Range
        else:
            browser.find_element(By.XPATH, '//*[@id="trans_start_date"]').clear()
            browser.find_element(By.XPATH, '//*[@id="trans_start_date"]').send_keys(start)
            browser.find_element(By.XPATH, '//*[@id="trans_end_date"]').clear()
            browser.find_element(By.XPATH, '//*[@id="trans_end_date"]').send_keys(end)
            browser.find_element(By.XPATH, '//*[@id="trans_search"]').click()

        # Attempts to access the table of values for 1 minute until it successfully loads
        transactions_table = None
        for i in range(60):
            try:
                transactions_table = browser.find_element(By.XPATH, '//*[@id="transaction_result"]/table')
                break
            except:
                time.sleep(1)
        
        data = transactions_table.find_element(By.TAG_NAME, 'tbody')
        transactions_unprocessed = data.find_elements(By.TAG_NAME, 'tr')
        transactions = []
        # Appends each Transaction to the list transactions
        for transaction in transactions_unprocessed:
            temp = transaction.find_element(By.CSS_SELECTOR, "td[data-title='Terminal:']").get_attribute('innerHTML').split(" : ")[1].strip()
            if "MUDIES" in temp:
                temp = "MUDIES"
            elif "LAUNDRY" in temp:
                temp = "LAUNDRY"
            transactions.append(Transaction(transaction.find_element(By.CSS_SELECTOR, "td[data-title='Date:']").get_attribute('innerHTML'),
                                            float(transaction.find_element(By.CSS_SELECTOR, "td[data-title='Amount:']").get_attribute('innerHTML')[2:]),
                                            temp))
        
        return transactions

    # Prints Watcard transactions for the past 60 days
    # transactions_60: None -> List of Transaction
    def transactions_60(self):
        self.transactions_60days = self.transactions_scrape("60")
        self.most_recent_lookup = self.transactions_60days
        return self.transactions_60days
        
    # Prints Watcard transactions for the past 30 days
    # transactions_30: None -> List of Transaction
    def transactions_30(self):
        self.transactions_30days = self.transactions_scrape("30")
        self.most_recent_lookup = self.transactions_30days
        return self.transactions_30days
    
    # Prints Watcard transactions from specified start date to end date
    # transactions_range: None -> List of Transaction
    def transactions_range(self, start, end):
        self.transactions_recent_range = self.transactions_scrape("range", start, end)
        self.most_recent_lookup = self.transactions_recent_range
        return self.transactions_recent_range
    
    # Scrapes and prints out the current balance of Watcard. Only balances
    #   that are not empty would be shown.
    # balance: None -> None
    def balance(self):
        # Initializes Chromedriver
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('log-level=3')
        options.add_argument("--headless")
        browser = webdriver.Chrome(options = options)
        browser.maximize_window()
        browser.get('https://watcard.uwaterloo.ca/OneWeb/Account/LogOn')\
        
        # Login
        username_input = browser.find_element(By.XPATH, '//*[@id="Account"]')
        password_input = browser.find_element(By.XPATH, '//*[@id="Password"]')
        username_input.send_keys(self.studentID)
        password_input.send_keys(self.password)
        login_button = browser.find_element(By.XPATH, '//*[@id="oneweb_main_content"]/div[2]/div[3]/form/div/button')
        login_button.click()

        # Goes to Balances page
        browser.find_element(By.XPATH, '//*[@id="ow-navbar-collapse"]/ul/li[2]/a').click()
        browser.find_element(By.XPATH, '//*[@id="ow-navbar-collapse"]/ul/li[2]/ul/li[1]/a').click()

        # Locates table of balances
        balances_table = browser.find_element(By.XPATH, '//*[@id="oneweb_main_content"]/div[2]/div[1]/div/table')
        data = balances_table.find_element(By.TAG_NAME, 'tbody')
        balances_unprocessed = data.find_elements(By.TAG_NAME, 'tr')
        balances = []
        
        # Appends non-empty balance to list balances
        for balance in balances_unprocessed:
            if (balance.find_element(By.CSS_SELECTOR, "td[data-title='Limit:']").get_attribute('innerHTML') != "$ 0.00") or (balance.find_element(By.CSS_SELECTOR, "td[data-title='Amount:']").get_attribute('innerHTML') != "$ 0.00"):
                balances.append(Balance(balance.find_element(By.CSS_SELECTOR, "td[data-title='Name:']").get_attribute('innerHTML'),
                                                balance.find_element(By.CSS_SELECTOR, "td[data-title='Limit:']").get_attribute('innerHTML'),
                                                balance.find_element(By.CSS_SELECTOR, "td[data-title='Amount:']").get_attribute('innerHTML')))
        self.balances = balances
        return balances

    def graph(self, transactions):
        frequency = {}
        for transaction in transactions:
            if transaction.location in frequency:
                temp = frequency[transaction.location]
                temp += -1 * transaction.amount
                frequency[transaction.location] = round(temp, 2)
            else:
                frequency[transaction.location] = round(-1 * transaction.amount, 2)
        locations = list(frequency.keys())
        amount = list(frequency.values())
        locations = [ location.replace(' ', '\n') for location in locations]
        plt.bar(locations, amount)
        plt.title('Money Spent on Different Locations')
        plt.xlabel('Location')
        plt.ylabel('Money Spent')
        plt.show()
        return frequency