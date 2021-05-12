# CADDIT

<img src="/CADDIT1.jpg"></img>

It's an online message board like **Reddit** made by **Flask** and **SQLAlchemy**.
- I use a database to store all the data.
- The passwords are hashed in this database.


## Content
- Registered members can submit content to the site under different categories and they can comment on other posts.
<img src="/CADDIT3.jpg"></img>
- It has different categories that users can post -like **subreddits**-
- Users can customize their profiles and add their social media accounts
<img src="/CADDIT2.jpg"></img>

## APIs
- GET /api/post  ---> returns the last 10 posts as JSON
- GET /api/category ---> returns category lists and their slugs as JSON
- GET /api/post/<id> --->  returns the post given by id and its comments
- GET /api/category/<category> ---> returns the posts of given category
- GET /api/user/<username> ---> returns the given user's public information



## Made by
<p align="left"> 
   <a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a><a href="https://flask.palletsprojects.com/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg" alt="flask" width="40" height="40"/> </a> <a href="https://getbootstrap.com" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bootstrap/bootstrap-plain-wordmark.svg" alt="bootstrap" width="40" height="40"/> </a></p>

## Check My Other Projects
- <a href="https://github.com/davutkulaksiz">GitHub</a>
- <a href="https://davutkulaksiz.github.io/">GitHub Pages</a>
