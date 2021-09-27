import mysql.connector

# Connecting to the database
mydb = mysql.connector.connect(
  host="localhost",
  user="otheruser",
  password="swordfish",
  database="testing"
)

#Autocommit is disabled by default when connecting through Connector/Python. 
#This can be enabled using the autocommit connection parameter.
mydb.autocommit = True

# My cursor allows me to execute sql commands.
mycursor = mydb.cursor()


#-----------------------------------------------------------------------------------------------------------------------#


# FUNCTIONS FOR QUIZZES:


#Function to be reused for every new quiz option added but change table name
def take_quiz1():
    
    #I could probably have just used SELECT * here but it was working and I didn't want to mess with it :)
    mycursor.execute("SELECT ID, question, option1, option2, option3, answer FROM quiz1")
    result = mycursor.fetchall()
    
    #Declare variable to track correct answers
    correct=0
    
    for row in result:                                         #Loop through the rows
        print("{}: {}".format(row[0], row[1]))                 #Prints number and question
        print("a)", row[2])                                    #Prints option a
        print("b)", row[3])
        print("c)", row[4])
        answer = input("Enter 'a', 'b', or 'c':")              #Ask for user input
        if answer == row[5]:                                   #Check if input matches correct answer stored in database
            correct+=1                                         #If so, add to correct tally
        print("\n")

    print("Total Score: {}/3".format(correct))                 #Display score to user
    
    
    
#Repeat the exact same process but change table name
def take_quiz2():
    
    mycursor.execute("SELECT ID, question, option1, option2, option3, answer FROM quiz2") #Note table name is now quiz2
    result = mycursor.fetchall()
    
    correct=0
    
    for row in result:
        print("{}: {}".format(row[0], row[1]))
        print("a)", row[2])
        print("b)", row[3])
        print("c)", row[4])
        answer = input("Enter 'a', 'b', or 'c':")
        if answer == row[5]:
            correct+=1
        print("\n")

    print("Total Score: {}/3".format(correct))
    
    
def take_quiz3():
    
    mycursor.execute("SELECT ID, question, option1, option2, option3, answer FROM quiz3")
    result = mycursor.fetchall()
    
    correct=0
    
    for row in result:
        print("{}: {}".format(row[0], row[1]))
        print("a)", row[2])
        print("b)", row[3])
        print("c)", row[4])
        answer = input("Enter 'a', 'b', or 'c':")
        if answer == row[5]:
            correct+=1
        print("\n")

    print("Total Score: {}/3".format(correct))
    


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
        
        
        #Notify user of successful quiz addition
        #Call notify() method to let devs know to add new menu option
        print("Quiz Added")
        notify()
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


import smtplib

#Function to notify support engineers to load newly created quiz
#Resource: https://www.youtube.com/watch?v=Y_tnWTjTfzY
def notify():
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)                        #Connect to gmail server
    server.login("wezquizdevs@gmail.com", "uslmrvunjrhlvkob")               #Login to sender email address
    server.sendmail("wezquizdevs@gmail.com",                                
                    "Wesleyweber18@gmail.com", #Sends to your own email to test funtion                                     
                    "New Quiz Notification. Please add menu option")

    server.quit()
    print ("Quiz Added. The quiz offering will be updated within 48hrs")
        
        
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


#Resource: https://stackoverflow.com/questions/3556305/how-to-retrieve-table-names-in-a-mysql-database-with-python-and-mysqldb
#Function to allow user to choose from quiz database
def choose_quiz():
    
    #Quiz choice menu continously runs with while loop until user hits 0 to go back
    while True:
        
        
        #execute 'SHOW TABLES' (but data is not returned)
        mycursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'quizzes'")   
        
        #Variable to show option number next to quiz names
        x=1
    
        #Iterates through, and prints table names in quizzes database
        for (table_name,) in mycursor:
                print(x,table_name)
                x+=1
        
        #Try except block to account for erroneous user input and prevent crash
        try:
            quiz_choice = int(input("Choose a quiz (enter 0  to go back): "))     

            if quiz_choice == 1:        #Each quiz has its own dedicated method that gets called based on user input
                take_quiz1()
            elif quiz_choice == 2:
                take_quiz2()
            elif quiz_choice == 3:
                take_quiz3()
            elif quiz_choice == 0:
                break
        
        #Prompt user to make correct input if they make a mistake in choosing quiz
        except:
            print("Please choose a quiz by typing a number and hitting enter")
            for (table_name,) in mycursor:
                print(x,table_name)
                x+=1
            continue
            
            
#----------------------------------------------------------------------------------------------------------------------#


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