This project has the main goal of building an app that I can use myself, specifically when driving, as a way to rehearse trivia questions.
The source file is "vragenENG.csv" which contains all questions and answers with "vraag,antwoord" as the key value pair.
The main program is (currently) quiz_spoken.py which intends to
- randomly pick a question from the csv
- convert the text into speech, and read the question out loud
- wait 5 seconds
- and then read the answer out loud
- moving to the next random question after 2 more seconds
This will allow me to think of the answer and then have it checked by hearing the answer.
Key features are:
- the randomization (else I will remember the sequence of answers)
- the automatic queue (else I have to manipulate my device while driving)
I built the application as a "vibe coding" experiment, following instructions by ChatGPT. I have a fair understanding of the end result but I have a hard time debugging or improving.

Problems:
- the current version of the app does not queue the questions but puts clickable mp3s into the browser
- the local program I have, quizvoorgelezenENG, does the queuing but on my laptop it doesn't activate Dutch text-to-speech
