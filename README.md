# QuizManager
Final iteration of the quiz project as per the requirements of the HyperionDev careers program

## Project Details

### Description:
For this project we were instructed to create a quiz program, that enables users to log in as either quiz masters or quiz takers (users). The quiz masters are able to create ,add new quizzes to the program and add a age restriction, while the users are able to take the quizzes to test their knowledge.

### Functionality:
This program an updated version of the QuizManager project also saved in this repository. The quiz masters now have the ability to set the number of questions they would like for a given quiz (as opposed to the previous predetermined number of three questions per quiz). Users who take the quiz are also now given a little more feedback on their performace (as opposed to just a score out of 3 as before). The quiz master is also able to add an age restriction.

MySQL databases: This program works by connecting to two local database schemas. One called Credentials, which houses all the user data, and one called quizzes, which is where all the quizzes and quiz questions are stored. If the abovementioned databases do not already exist locally, they are automatically created for the user by the program as it runs.

add-quiz: The add_quiz function is called after a user successfully logs in as a master and selects the option to add a quiz from the masters’ menu. The user is allowed to choose the name for the quiz they create as well as the number of questions within it, and the quiz is saved as such in the quizzes database. The creator of the quiz is prompted to give a quiz name, quiz age restriction and write down a question, followed by three possible answers and is then asked which letter corresponds to the correct answer (a, b, or c). This process is reiterated for as many times as there are questions in the quiz. After the successful addition of the quiz to the database, the master who created it is notified of their success. In the case of a failure to add a quiz for any reason, a try except block will also provide a notification and return the user to the menu.

take-quiz: The take_quiz function is called when a user successfully logs in as a user and selects the option to take a quiz from the user menu. They are then prompted to enter the name of the quiz based on a list of possible options which is displayed to the user by printing the names of all the tables within the quizzes database. After the user enters a valid name, the program then iterates through all the questions stored in the corresponding quiz and takes in user input as their responses to the quiz questions. After completing the quiz, the user is shown their score and given brief feedback on their performance and returned to the menu to navigate the program as they wish.

add_user: The add_user function asks the user to enter a name, password and email address which is then stored into a MySQL table called user_info. When a user wants to log in, the program checks their username and password against the list within the database to see if they are valid details.

add_master: This works exactly the same as the add user function, only the data is saved to the quiz_master_info table.

user login and master login: As mentioned above, when a user wants to log in as a user to take a quiz or a master to create one, they are prompted to make the relevant selection from the starting menu, after which they are asked to input valid log in detail. If the log in info is validated by what is stored in the appropriate database, their log in will be successful and they will be presented with further options within the user menu or master menu.

### Usefulness:
This project could be used as an efficient program for an edtech company to help educate students in any field. It could also be used by schools as a way to help studetns prep of exams. It is simple and straightforward to use and the code itself is clean and well commented on, making it easy to understand.

### Contributors:
This was team project completed by Wesley Weber and Jarryd Robson.

### Project Status:
This will hopefully be the final version of this program, assuming the Hyperion code reviewers are happy, and will mark the completion of the Hyperion careers program for it's creators.

