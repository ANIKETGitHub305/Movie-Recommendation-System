# Imported datetime module. It supplies classes to work with date and time
import datetime

# Defind the class by the user
class User:

    def __init__(self,user_id,pin):
        self.user_id = user_id
        self.pin = pin
        self.balance = 0
        self.transactions_history = []



    def get_transaction_history(self):
        return self.transactions_history



    def withdraw(self,amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.transactions_history.append((datetime.datetime.now(),"withdraw" , amount))
            return  True
        else:
            return False




    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions_history.append((datetime.datetime.now(),"Deposit", amount))
            return True
        else:
            return False


    def transfer(self,to_user,amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            to_user.balance += amount
            self.transactions_history.append((datetime.datetime.now(), "Transfer to user ID: " + to_user.user_id, amount))
            to_user.transactions_history.append((datetime.datetime.now(), "Transfer from user ID: " + self.user_id, amount))
            return True
        else:
            return False


# Defined the class by the user
class ATM:
    def __init__(self):
        self.users = {}


    def authenticate_user(self, user_id,pin):
        if user_id in self.users and self.users[user_id].pin == pin:
            return self.users[user_id]
        else:
            return None


    def add_user(self, user):
        self.users[user.user_id] = user


#Define the main function
def main():
    atm = ATM()
    # User ID and PIN
    Aniket = User("Aniket", "637073")
    Akmal = User("Akmal", "123456")
    Ashish = User("Ashish", "987764")
    Bishnu = User("Bishnu", "700564")
    Chirag = User("Chirag", "885962")


    atm.add_user(Aniket)
    atm.add_user(Akmal)
    atm.add_user(Ashish)
    atm.add_user(Bishnu)
    atm.add_user(Chirag)



    while True:
        print("Welcome to My ATM Interface")   #Display the main menu

        user_id = input(("Enter the User ID"))   #Get the User's ID

        pin = input(("Enter the pin"))     #Get the User's PIN

        user = atm.authenticate_user(user_id,pin)   #check if User ID and PIN are Correct


        if(user):
            print("Successfully Authenticated")
            while True:
                #Display all the choices
                print("1. Transaction History ")
                print("2. Withdraw ")
                print("3. Deposit ")
                print("4. Transfer ")
                print("5. Quit ")

                # Get the User's Choices
                choice = input(" Enter Your Choice: ")

                #check the User's Choice
                if choice == "1":
                    print("Transactions History:  ")
                    for transactions in user.get_transactions_history():
                        print(transactions)


                elif choice == "2":  #Withdrew Amount
                    amount = float(input("Enter the withdrawal Amount"))
                    if user.withdraw(amount):
                        print("Successfully Withdrew. Now Your Balance is:  ",user.balance)
                    else:
                        print("Invalid Amount or Insufficient Balance")

                elif choice == "3":   #Deposited Amount
                    amount = float(input("Enter the Deposit Amount:  "))
                    if user.deposit(amount):
                        print("Successfully Deposited. Now Your Balance is: " ,user.balance)
                    else:
                        print("Invalid Amount. Please Enter the Valid Amount ")


                elif choice == "4": #Recipient's User ID
                    recipient_id = input("Enter the Recipient's User ID: ")
                    recipient = atm.authenticate_user(recipient_id, "232323")
                    if recipient:
                        amount = float(input("Enter the Transfer Amount: "))
                        if user.transfer(recipient,amount):
                            print("Successfully Transferred")
                        else:
                            print("Invalid Amount or Insufficient Balance")
                    else:
                        print("Recipient not found")


                elif choice == "5": # Quit
                    print(" Thank You For Using The ATM! ")
                    exit()

                else:
                    print(" Invalid Choice. Please Select a Valid Option ")

        else:
            print(" Authentication Failed. Please Check Your User ID and PIN ")




if __name__ == "__main__":
    #call the main Function
    main()












