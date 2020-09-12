# Online-Message-Board
 It's an online message board like Reddit made by Flask and SQLAlchemy.
 
 Registered members can submit content to the site under different categories and they can comment on other posts.
 I use databases to store all the data and the passwords are hashed.

You can use the API to get public data using these:

- GET /api/post  ---> returns the last 10 posts as JSON
- GET /api/category ---> returns category lists and their slugs as JSON
- GET /api/post/<id> --->  returns the post given by id and its comments
- GET /api/category/<category> ---> returns the posts of given category
- GET /api/user/<username> ---> returns the given user's public information
