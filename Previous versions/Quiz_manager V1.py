import mysql.connector

# Connecting to the database
mydb = mysql.connector.connect(
  host="localhost",
  user="otheruser",
  password="swordfish",
  database="testing
)

#Autocommit is disabled by default when connecting through Connector/Python. 
#This can be enabled using the autocommit connection parameter.
mydb.autocommit = True

# My cursor allows me to execute sql commands.
mycursor = mydb.cursor()


#-----------------------------------------------------------------------------------------------------------------------#


# FUNCTIONS:

#Version of add_quiz that connects to db...
def add_quiz():
    
    #Try except block to prevent program from crashing in case of error
    #Note: Must find a way to print questions and options in a more user friendly way
    #Note2: Must add fuctionality to allow user to choose from answers and receive feedback
    try:
        #Set variable to let user add 3 questions
        num_of_questions = 3

        #Iterate through num_of_questions
        for i in range(num_of_questions):
            question = input("Type Question")     #Take question
            option1 = input("Give option a")      #User gives three possible answer
            option2 = input("Give option b")
            option3 = input("Give option c")
            answer = input("Which was the correct one?")

            #Writes to database table
            #Note1: must add functionality to allow user created tables with user chosen names
            #Note2: I used .execute function slightly differently to how you did in your other methods because this table has autoincrement ID
            mycursor.execute("INSERT INTO testing.quiz1(question, option1, option2, option3, answer) VALUES (%s, %s, %s, %s, %s)",
                                (question, option1, option2, option3, answer))
            
        print("Quiz Added")
        mycursor.execute("SELECT * FROM quiz1")
  
        # fetch all the matching rows 
        result = mycursor.fetchall()

        # loop through the rows
        for row in result:
            print(row)
            print("\n")
        
    except:
        print("Something went wrong")
        
        
#-----------------------------------------------------------------------------------------------------------------------#


# Function to add a new user(quiz taker)
def add_user():
  username = input("Please enter your username: ")
  password = input("Please enter your password: ")
  email = input ("Please enter your email address: ")
  add_to_table = "insert into user_info Values ('"+username+"','"+password+"','"+email+"')"
  mycursor.execute(add_to_table)


#-----------------------------------------------------------------------------------------------------------------------#


# Function to add a new quiz master(quiz maker)
def add_master():
  username = input("Please enter your username: ")
  password = input("Please enter your password: ")
  add_to_table = "insert into quiz_master_info Values ('"+username+"','"+password+"')"
  mycursor.execute(add_to_table)
    
    
#-----------------------------------------------------------------------------------------------------------------------#


# Function to check log in of user
def user_login():
  username = input('Enter username: ')
  password = input('Enter password: ')
  # Checking if the username or password is in the table (Checking if it is correct)
  statement = f"SELECT Username from user_info WHERE Username='{username}' AND Password = '{password}';"
  mycursor.execute(statement)
  if not mycursor.fetchone():  # An empty result evaluates to False.
    print("Incorrect username or password")
  else:
    # Else if it is correct / Login successful!
    print("Login Successful!")
    
    
#-----------------------------------------------------------------------------------------------------------------------#


# Function to check log in of master
def master_login():
  username = input('Enter username: ')
  password = input('Enter password: ')
  # Checking if the username or password is in the table (Checking if it is correct)
  statement = f"SELECT Username from quiz_master_info WHERE Username='{username}' AND Password = '{password}';"
  mycursor.execute(statement)
  if not mycursor.fetchone():  # An empty result evaluates to False.
    print("Incorrect username or password")
  else:
    # Else if it is correct / Login successful!
    print("Login Successful!")
    
    
#-----------------------------------------------------------------------------------------------------------------------#


# MENU SELECTION:

print("WELCOME!")

selection = input("Please enter one of the following options: \na - Add new user(Quiz taker) \nb - Add new quiz-master \nc - User log in \nd - Quiz master log in \nPlease enter your option now: ")

if selection == "a":
  add_user()

elif selection == "b":
  add_master()

elif selection == "c":
  user_login()

elif selection == "d":
  master_login()

else:
  print("Invalid selection, please try again!")