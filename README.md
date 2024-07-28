# RL Trainer
### Video Demo:  https://youtu.be/CC_aOxuGdls
### Description:
This is RL Trainer, a web application designed to assist Rocket League players in enhancing their gameplay. Built with Flask, RL Trainer leverages the powerful analytical capabilities of Ballchasing.com to automatically analyze your Rocket League replays. By simply uploading your replay files, RL Trainer provides you with a page of your playstyle and offers personalized suggestions on the mechanics you need to improve.

#### How it works:
Start by signing up by creating a username and then entering a password, and of course confirming it to make sure you dont forget your password. Next you will be redirected to the home page where you can upload your rocket league replay file which can be saved after you have finished a game. Keep in mind that 1v1 (or even 2v1) is not supported and will return an error. Ballchasing.com also has an upload limit to prevent the website from crashing and other types of errors such as overload, for this reason sometimes you might encounter this type of error, where the solution would be to just try again later, but sometimes even when the website has not reached the limit, ballchasing.com has a problem where they cant analyze the replay properly and return stats that are incomplete, if that happens to you simply try uploading your replay file again.

You will then be shown the players that has played in the game and finished the game without forfeiting/leaving the game, and you will have to select one of them to view their playstyle. After the backend has processed the results, you will be shown one of four different playstyles:
1. Ball Chaser - Someone who recklessly tries to hit the ball, without giving much importance to other factors such as, teammates, rotation or position.
2. Anchor - Someone who patiently waits for in his defensive half, waiting for a good opportunity to counter.
3. Passer - Someone who gives a lot of importance to his teammates, making space and trying to get on the end of passes.
4. All Rounder - A player who equally gives importance to all aspects of Rocket League's mechanics and skills.

On each playstyles' page it includes many things which you can use to your advantage, it includes two (or more) lists of mechanics (or skills) that you can use to improve your game, and rank up in Rocket League. It also includes 2 videos from YouTube, which are considered the best for the specific playstyle the user has. And finally, it also includes a small tip which will definitely improve yourself.

After you have seen your playstyle, checked what the webpage includes, You can navigate to the home page to analyze a different replay and if you wish to see your playstyle of the previous replay, you can click on the 'My Playstyle' link on the navbar.

#### Files:
* There are a few folders that were generated automatically when I started my Flask application since I'm using a local environment. Those including:
 - __pycache__ - This includes all the cache of the website so that it doesn't need to additionaly download extra data and take longer to load
 - .venv - This includes other stuff that are just essential for programming such as, libraries, scripts, etc.

* For my app I am using bootstrap and I wanted to customize the colors, so I have bootstrap locally installed in this folder. There are also a few .json files. Files/folders that exist because of bootstrap include node_modules, css, sass, package-lock.json and package.json

* In the static folder there are only 3 files:
 - main.min.css (css file)
 - logo.png (favicon img)
 - rocket_league.png (just a random image of RL)

* The templates folder has 11 different html files, which can be categorized into 4 types:
 - Login Pages - login and register
 - Normal Pages - index, layout and chooseplayer
 - Error Pages - noplaystyle and apology
 - Playstyle Pages - allrounder, ballchaser, passer and anchor

* In app.py, there are several defs that are written in this file, which is the main backend for my application, RL Trainer:
 - register - This is where you would make a new account in RL Trainer
 - login - This is where you would login to RL Trainer with your account
 - logout - This has all the functionality that makes the logout button work
 - index - The home page, where you can upload your replay
 - playstyle - This redirects you to the /playstyle route where you can choose your player, and view the playstyle
 - myplaystyle - This is similar to the one before, it displays your playstyle when you have clicked the 'My Playstyle' button in the navbar. If you have not analyzed a replay yet it doesn't show anything

* There are also some other files, such as:
 - trainer.db - Contains the users and the users' playstyles
 - ideas.txt - Everything that I wanted to add and other things which I needed to write down is here
 - helpers.py - This python file contains two functions: apology and login_required, which were used as libraries for app.py. And yes this is from cs50's pset 9
 - README.md - This file you're reading


This is everything about RL Trainer
