# Bloom Quiz
#### Video Demo:  <URL https://www.youtube.com/watch?v=MHDgeOUYp1U>
#### Description:
Bloom Quiz is a website with quiz creation and taking capabilities. Starting out, you must register, you can't log in without knowing any account details. The registration has a password confirmation to
make sure that you remember your password and didn't make a typo. The registration details are stored in a sql database, then when you attempt to log in it checks your provided login details with all details
from the sql database. Once you login, you can logout or change your password. When you log in, you are greeted with the home page. It simply is a table of your stats which will initially be empty. I created 3
preloaded quizzes which each user will have access to: CS50, Math, and Grammar. The quizzes are each 5 questions with radio buttons to select answers and have their own html files and functions. Each one's
specific function is mostly the same, they insert into the stats table in SQL the amount of questions, the amount of correct answers, the user id, topic, and the percentage of correct answers. After completing
the quiz, you are shown the results template, which is a table that shows the topic of the quiz, the amount of questions, the amount of correct answers, and the percentage of correct answers. After clicking the
return to homepage button on the results screen, you are returned to home with the stats table now having the new results.
    The most involved part of the website is the ability to create your own quizzes and then
    take them. When clicking of the create a quiz button, you are sent to the first of two parts of the creation form. On this part, you enter the quiz name and the difficulty which you want it to be (from 1-5).
When you click the confirm button, it uses javascript to hide the first part of the form and the confirm button and shows the previously hidden second part of the form with the submit button. You then enter the
text and answer choices for your 4 desired questions and for each one select from a drop down menu the answer choice which is correct. After that, you click the submit button and have your quiz sent through POST
to the create function where it takes your values and inserts them into the quizzes and questions SQL tables. The quizzes table simply has the names, ids, and difficulties of each quiz while the questions table
has each row correspond to one question, each row having an id which corresponds to the quiz's id, the question text, all of the answer choices, and the correct answer choice. You are then redirected to the home
page with a flash message telling you that you successfully created the quiz (along the way if you don't enter information somewhere or do something else that would break the system you get an apology error
message). Now, you can go to the 'Your quizzes' page.
    When you go to the 'your quizzes' page, there is a table with the names of each quiz you made (with a hyperlink) and the difficulty level of each quiz. When you click the hyperlink to take the quiz you want,
open_quiz is called and it sends you to a custom url which is based on the id of the quiz you clicked on (/quiz/quiz_id). After submitting the quiz, open_quiz is called via POST and it retrieves your answers,
retrieves the correct answers from the database, and compares the values of the two. After that, it updates the 'corrects' variable and inserts all of the necessary data into the stats database and finally
renders the results screen with the necessary data.
    I envision this website as an interesting way to study, you can create mock quizzes based on a real quiz you have to take in school for instance. I hope in the future to turn it into an online system with
different people able to create quizzes for each other and take each other's quizzes. This was my CS50 final project.
