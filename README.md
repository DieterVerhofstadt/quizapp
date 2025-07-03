This project has the main goal of building an app that I can use myself, specifically when driving, as a way to rehearse trivia questions. What I want is
- an automatic queue of randomized questions
- read out loud
- with some time in between so I can think of the answer
- then getting the answer read out loud

Key features are:
- the randomization (else I will remember the sequence of answers)
- the automatic queue (else I have to manipulate my device while driving)
I built the application as a "vibe coding" experiment, following instructions by ChatGPT. I have a fair understanding of the end result but I have a hard time debugging or improving.

Structure:
- The source file is "vragenENG.csv" which contains all questions and answers with "vraag,antwoord" as the key value pair.
- The main program is (currently) quiz_spoken.py
- Two auxiliary files are config.toml and requirements.txt
- there are other files with questions in Dutch or different approaches to the main program

Problems:
- the first version of the app does not queue the questions but puts clickable mp3s into the browser; after some investigation, it turned out that streamlit.clout doesn't support an automatic queue of generated audio; I changed the program to produce 1 mp3 of a randomized order of the questions
- the local program I have, quizvoorgelezenENG, does the queuing but on my laptop it doesn't activate Dutch text-to-speech

Nice to haves:
- having a Dutch version
- having my own voice reading them
- have it published to a wide audience
- have an app per trivia topic, or activate a topic in the app
- users can feed their own questions
- you can start and stop the app with speech yourself
