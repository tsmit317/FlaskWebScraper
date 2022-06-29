# [Ski NC](https://skinc.herokuapp.com/)
Ski NC is a simple web app which displays the current conditions and slope status for North Carolina’s five major ski resorts.

<img width="1456" alt="Screen Shot 2022-06-29 at 14 35 40" src="https://user-images.githubusercontent.com/13583303/176534560-127e3a90-43f3-407b-9ab9-d4c1b9b68856.png">



### How it works

Built with the lightweight Flask web framework, this web app utilizes Python’s Beautiful Soup library to web scrape condition and slope data from NC’s five major ski resort websites. 
The app runs a BackgroundScheduler via the APScheduler library to update condition and slope data every hour. 
The frontend is designed using the Bootstrap framework and the app is currently hosted on the Heroku cloud platform. 

### Motivation

My initial goal was to learn more about web frameworks, specifically Flask or Django. 
I thought displaying all NC ski conditions on one page rather than having to check each website individually would be different, and I was curious to see what it would look like. 
I ended up choosing Flask over Django due to the website's intended simplicity.

### Current Issues

This web app is currently using SQLite. SQLite is not intended as a production grade database. 
Instead Heroku provides production grade PostgreSQL databases as a service. 
Additionally, SQLite writes to a disk and since Heroku uses an Ephemeral filesystem, anything you write to disk won't be persisted between instances of the app. 
Basically, the contents of the database are cleared periodically. You might notice the “Last Updated” date is wildly incorrect. 
A hard reset (clear your browser cache) should fix this: Ctrl + Shift + R

### Tech/frameworks used

- [Flask](https://flask.palletsprojects.com/en/2.1.x/) 
- [Bootstrap](https://getbootstrap.com/)

