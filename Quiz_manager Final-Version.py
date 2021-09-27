import mysql.connector
# SO i can view the scores correctly
# Type this into your terminal to download pandas so it works :  py -3 -m pip install pandas (Hit enter and it will download)
import pandas as pd

# This will create the database if it doesnt exist and do nothing if it does!
con = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root"
)
test_cursor =con.cursor()
try: 
  test_cursor.execute("CREATE DATABASE Credentials")
except Exception as ex:
    # Rollback is very important
    con.rollback()

# Connecting to the testing database
mydb1 = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="Credentials"
)

#Autocommit is disabled by default when connecting through Connector/Python. 
#This can be enabled using the autocommit connection parameter.
mydb1.autocommit = True

# My cursor allows me to execute sql commands for testing database.
user_cursor = mydb1.cursor()

# This will create the database if it doesnt exist and do nothing if it does!
try: 
  test_cursor.execute("CREATE DATABASE Quizzes")
except Exception as ex:
    # Rollback is very important
    con.rollback()

# Connecting to the quizzes database
mydb2 = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="quizzes"
)

#Autocommit is disabled by default when connecting through Connector/Python. 
#This can be enabled using the autocommit connection parameter.
mydb2.autocommit = True

# My cursor allows me to execute sql commands for quizzes database.
quiz_cursor = mydb2 .cursor()


# FUNCTIONS:

# Version of add_quiz that connects to db.
# The default number of questions will be 3, you can change this easily by changing the number in the parameter. 
def add_quiz():
    
    #Try except block to prevent program from crashing in case of error
    try:

        # Asking user for a quiz name.
        quiz_name = input("Please enter the quiz name: ")

        #Allow user to determine number of questions as per reviewer instructions
        num_of_questions = int(input("How many questions should your quiz have?: \n"))

        # Allow the quiz master to add any restrictions according to age or gender (or both)
        age_restriction = input("Please enter an age restriction (If none please enter 0): ")
        
        # Replacing any spaces with a underscore as you cant use spaces in SQL to make table names.
        quiz_name = quiz_name.replace(" ","_")

        # Creating the new table in quizzes for the new quiz.
        quiz_cursor.execute("CREATE TABLE "+quiz_name+"(\
                            question varchar(255),\
                            option1 varchar(255),\
                            option2 varchar(255),\
                            option3 varchar(255),\
                            answer varchar(255),\
                            age_requirement varchar(255));")

        #Iterate through num_of_questions
        for i in range(num_of_questions):
            question = input("Type Question: ")     #Take question
            option1 = input("Give option a: ")      #User gives three possible answer
            option2 = input("Give option b: ")
            option3 = input("Give option c: ")
            answer = input("Which was the correct one: a/b/c")


            #Writes to database table
            #The questions and answers will be added to the table now.
            quiz_cursor.execute("INSERT INTO quizzes."+quiz_name+"(question, option1, option2, option3, answer,age_requirement) VALUES (%s, %s, %s, %s, %s, %s)",
                                (question, option1, option2, option3, answer,age_restriction))
            
        print("Quiz Added")
        quiz_cursor.execute("SELECT * FROM "+quiz_name)
  
        # fetch all the matching rows 
        result = quiz_cursor.fetchall()

        # loop through the rows
        print("These are the questions you added to "+quiz_name+" below: Question/ option1/ option2/ option3/ correct answer/Age restriction\n")
        for row in result:
            print(row)
            print("\n")
        
    except:
        print("Something went wrong")

#This function will let the user access and complete a selected quiz.
def take_quiz(quiz_name, user):

  # This will create the table if it doesnt exist and do nothing if it does!
  try:
    quiz_cursor.execute("CREATE TABLE SCORES (\
    QuizName varchar(255),\
    User varchar(255),\
    Attempts int(10),\
    Score int(10),\
    TotalQuestions int(10));")
  except Exception as ex:
    # Rollback is very important
    print()

  #I could probably have just used SELECT * here but it was working and I didn't want to mess with it :)
  # This will now select the correct quiz and ask the questions, then give a score!
  print("\nWelcome to the", quiz_name, "quiz!",sep = " ")
  quiz_cursor.execute("SELECT question, option1, option2, option3, answer FROM "+quiz_name)
  result = quiz_cursor.fetchall()
    
  #Declare variable to track correct answers
  correct=0
  #This is to number each question.
  question_num = 0
  for row in result:
    question_num +=1                                         #Loop through the rows
    print("\n{}: {}".format(question_num, row[0]))                 #Prints number and question
    print("a)", row[1])                                    #Prints option a then b then c
    print("b)", row[2])
    print("c)", row[3])
    answer = input("Enter 'a', 'b', or 'c': ")              #Ask for user input
    if answer == row[4]:                                   #Check if input matches correct answer stored in database
      correct+=1                                         #If so, add to correct tally   

  # Checking how many attempts the user made at the quiz.
  quiz_cursor.execute("Select * from SCORES WHERE QuizName='"+quiz_name+"' AND User = '"+user+"';")
  attemptsInfo = [item[0] for item in quiz_cursor.fetchall()]
  attemptsNo = len(attemptsInfo)+1

  # Adding all the info to the SCORES table.
  quiz_cursor.execute("insert into SCORES Values ('"+quiz_name+"','"+user+"','"+str(attemptsNo)+"','"+str(correct)+"','"+str(question_num)+"')")
  print(attemptsInfo)

  # Quiz done.
  print("\nQuiz Complete!")
  print("Total Score: ",correct,"/", question_num,)   #Display score to user
  percentage = round((correct/question_num)*100, 1)   #Calculate percentage and allow only 1 decimal place
  print("As a percentage: {}".format(percentage))     #Display percentage to user
        
  if percentage > 75:
        print ("That is a good score!")              #Display message to user based on performance
  elif percentage > 50:
        print("That is ok but you can do better")
  else:
        print("Maybe try an easier quiz?")                
    
# Function to add a new user(quiz taker)
def add_user():

  # This will create the table if it doesnt exist and do nothing if it does!
  try:
    user_cursor.execute("CREATE TABLE user_info (\
    Username varchar(255),\
    Password varchar(255),\
    Age varchar(255),\
    Email varchar(255));")
  except Exception as ex:
    print()

  username = input("Please enter your username: ")
  password = input("Please enter your password: ")
  age = input("Please enter your age: ")
  email = input ("Please enter your email address: ")
  add_to_table = "insert into user_info Values ('"+username+"','"+password+"','"+age+"','"+email+"')"
  user_cursor.execute(add_to_table)
  print("New user ({}) added!\n".format(username))

# Function to add a new quiz master(quiz maker)
def add_master():

  # This will create the table if it doesnt exist and do nothing if it does!
  try:
    user_cursor.execute("CREATE TABLE quiz_master_info (\
    Username varchar(255),\
    Password varchar(255));")
  except Exception as ex:
    print()

  username = input("Please enter your username: ")
  password = input("Please enter your password: ")
  add_to_table = "insert into quiz_master_info Values ('"+username+"','"+password+"')"
  user_cursor.execute(add_to_table)
  print("New quiz master ({}) added!\n".format(username))

# Function to check log in of user
def user_login():
  access = False
  username = input('Enter username: ')
  password = input('Enter password: ')
  # Checking if the username or password is in the table (Checking if it is correct)
  statement = f"SELECT Username from user_info WHERE Username='{username}' AND Password = '{password}';"
  user_cursor.execute(statement)
  if not user_cursor.fetchone():  # An empty result evaluates to False.
    print("Incorrect username or password")
  else:
    # Else if it is correct / Login successful!
    access = True
    print("Login Successful!")
  return access, username

# Function to check log in of master
def master_login():
  username = input('Enter username: ')
  password = input('Enter password: ')
  # Checking if the username or password is in the table (Checking if it is correct)
  statement = f"SELECT Username from quiz_master_info WHERE Username='{username}' AND Password = '{password}';"
  user_cursor.execute(statement)
  if not user_cursor.fetchone():  # An empty result evaluates to False.
    print("Incorrect username or password")
  else:
    # Else if it is correct / Login successful!
    print("Login Successful!")
    
    #Once log in successful, give option to go back or create new quiz
    master_choice = input("""Please enter one of the following options:\n 
a - Add new quiz \n\
b - View scores
c - Exit \n\
Please enter your option now: """)
    if master_choice[0].lower() == "a":      #If they choose a, call add_quiz()
        add_quiz()
    elif master_choice[0].lower() == "b":
        view_scores = quiz_cursor.execute("Select * from Scores")
        view_scores = quiz_cursor.fetchall()
        view_scores = pd.DataFrame(view_scores,columns=["Quizname","Username","Attempts","Score","Total-Questions"])
        print()
        print(view_scores)
        print()
    elif master_choice[0].lower == "c":      #'pass' goes back to main menu with no message
        pass
    else:
        print("\nOops, invalid entry. Returning to main menu\n")  #Back to main menu with message to user
        

# MENU SELECTION:

print("WELCOME TO WEZQUIZ!")

while True:
    # Asking new user what they want to do.
    selection = input("Please enter one of the following options: \n\
    a - User Sign up(Quiz taker) \n\
    b - Quiz-master Sign up \n\
    c - User log in \n\
    d - Quiz master log in \n\
    e - Quit \n\
    Please enter your option now: ")

    if selection == "a":
      add_user()

    elif selection == "b":
      add_master()

    elif selection == "c":

      # The function user_login will return a list, this gives each instance a variable name
      access, user = user_login()
      if access == True:
        busy = False
        # This will give the user the option to take multiple quizes or press e to exit.
        while(busy == False):
          user_option = input("Would you like to take a quiz or exit:\n\
    t - take quiz\n\
    e - Exit\n\
    Please enter your option now: ")

          # This will display all the quiz names so the user can select one and then take the quiz.
          if user_option == "t":
            quiz_cursor.execute("Show tables")
            print("\nThese are the quizzes available: ")
            table_names = [item[0] for item in quiz_cursor.fetchall()]
            # This will exclude the scores table so users cannot select it.
            toprint = [x for x in table_names if x != "scores"]
            print(*toprint, sep = "\n")
            selection = input("Please enter only the name of the quiz: ")
            # Checking if the user meets the age requirements to take the quiz.
            quiz_cursor.execute("SELECT age_requirement FROM "+selection)
            restriction = quiz_cursor.fetchall()[0][0]
            user_cursor.execute("SELECT Age FROM user_info WHERE Username='"+user+"'")
            user_age = user_cursor.fetchall()[0][0]
            if int(user_age) < int(restriction):
                print("You do not meet the age requirement to take this quiz! You must be "+restriction+" or above to take this quiz.")
            # If the user is the appropriate age it will allow them to take the quiz.
            else:
                take_quiz(selection, user)
  
          else: busy = True
            


    elif selection == "d":
      master_login()
    
    elif selection == "e":
        print("\nThank you! Goodbye:)")
        break

    else:
      print("Invalid selection, please try again!")