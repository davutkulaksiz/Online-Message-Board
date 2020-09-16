from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "ataçalgandeniziremgökçemuratmustafaözgürdavut"

# Database object
db = SQLAlchemy(app)
# Marshmallow Object for API
ma = Marshmallow(app)


# This will represent user objects on database
class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    post = db.relationship('Post', backref='poster')
    facebook = db.Column(db.String(50))
    twitter = db.Column(db.String(50))

    def __init__(self, name, email, password, post, facebook, twitter):
        self.name = name
        self.email = email
        self.password = password
        self.posts = post
        self.facebook = facebook
        self.twitter = twitter


# This will represent post objects on database
class Post(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    # name_of_poster = db.Column(db.String(100))
    category = db.Column(db.String(50))
    post = db.Column(db.String(240))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comment = db.relationship('Comment', backref='mainpost')

    def __init__(self, category, post, poster, comment):
        self.category = category
        self.post = post
        self.poster = poster
        self.comment = comment


# This will represent comment objects on database
class Comment(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    comment = db.Column(db.String(240))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    commenter = db.Column(db.String(100))

    def __init__(self, comment, commenter, mainpost):
        self.comment = comment
        self.commenter = commenter
        self.mainpost = mainpost


# This will be used for Post JSON Data
class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post

# This will be used for User JSON Data
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


# This will return the last 10 posts
@app.route("/api/post", methods=["GET"])
def get_post():
    # This is the number of posts
    length = Post.query.count()
    # offset will be used to get a slice of posts
    offset = length - 10
    # this will give last 10 posts
    posts = reversed(Post.query.order_by(Post._id).offset(offset).all())

    post_schema = PostSchema(many=True)
    output = post_schema.dump(posts)
    return jsonify({"post": output})

# This will return the post by given id
@app.route("/api/post/<post_id>", methods=["GET"])
def get_post_by_id(post_id):
    # To get the post by given id
    post = Post.query.filter_by(_id=post_id).first_or_404(description="There is no data for <Post{}>".format(post_id))
    post_schema = PostSchema()
    output = post_schema.dump(post)
    return jsonify({"post": output})

# The category list as JSON
@app.route("/api/category", methods=["GET"])
def get_category():
    categories = {
        "Cats": {
            "slug": "/cats",
        },
        "Other Animals": {
            "slug": "/otheranimals",
        },
        "Gaming": {
            "slug": "/gaming",
        },
        "Politics": {
            "slug": "/politics",
        },
        "NSFW": {
            "slug": "/nsfw",
        }
    }
    return jsonify({"categories": categories})

# This will return the posts under given category
@app.route("/api/category/<category>", methods=["GET"])
def get_category_by_name(category):
    # Get posts under specific category
    posts = Post.query.filter_by(category=category).with_entities(Post._id, Post.post)
    post_schema = PostSchema(many=True)
    output = post_schema.dump(posts)
    return jsonify({category: output})

# This will return the given user's public info
@app.route("/api/user/<user>", methods=["GET"])
def get_user(user):
    # Get user's public data
    user_info = User.query.filter_by(name=user).with_entities(User._id, User.name, User.facebook, User.twitter)\
        .first_or_404(description="There is no data for user {}".format(user))
    user_schema = UserSchema()
    output = user_schema.dump(user_info)
    return jsonify({"user:": output})


# Home Page
@app.route("/", methods=["GET", "POST"])
def index():
    if "user" in session:
        return render_template("index.html", user=session["user"], values=reversed(Post.query.all()))
    else:
        return render_template("index.html", values=reversed(Post.query.all()))


# THIS IS FOR EXPERIMENT
@app.route("/base", methods=["GET", "POST"])
def base():
    # This if/else statement will change the buttons on the right side of the site
    if "user" in session:
        return render_template("base.html", user=session["user"])
    # If there isn't logged in user, there will be LOG IN/SIGN UP buttons
    else:
        return render_template("base.html")


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    # Checking if a user logged in
    if "user" in session:
        return redirect(url_for("profile", user=session["user"]))
    # If there is no user
    else:
        # Getting input from user by POST method
        if request.method == "POST":
            # User Data
            username = request.form["username"]
            # Checking if the user exists in the database
            found_user = User.query.filter_by(name=username).first()
            if found_user:
                password = request.form["password"]
                # Checking if password matches with hashed one on database
                found_password = found_user.password
                password_check = sha256_crypt.verify(password, found_password)
                if password_check:
                    # Session starts
                    session["user"] = username
                    # Redirection to Dynamic User Page
                    return redirect(url_for("profile", user=username))
                else:
                    flash("Incorrect username or password", "info")
                    return render_template("login.html")
            else:
                flash("Incorrect username or password", "info")
                return render_template("login.html")
        else:
            return render_template("login.html")


# Logout Page
@app.route("/logout", methods=["GET", "POST"])
def logout():
    # Clearing session data to disable logs
    session.pop("user", None)
    # Error check
    if "user" in session:
        print("Oh, no we have a mouse infestation here!. There are some problems with logging out system.")
    return render_template("logout.html")


# Signup Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Checking if a user logged in
    if "user" in session:
        return redirect(url_for("user", usr=session["user"]))
    else:
        # Getting input from user by POST method
        if request.method == "POST":
            # User Data
            email = request.form["email"]
            username = request.form["username"]
            password = request.form["password"]
            # Hashed Password will be added to database
            hashed_password = sha256_crypt.encrypt(password)

            # Checking if the user exists in the database
            found_user = User.query.filter_by(name=username).first()
            if found_user:
                flash("You have already signed up!")
                return render_template("signup.html")
            else:
                # User object creation
                usr = User(username, email, hashed_password, post="", facebook="", twitter="")
                # Adding the user to database
                db.session.add(usr)
                db.session.commit()
                flash("You can now log in")
                return redirect(url_for("login"))
        return render_template("signup.html")


# Profile Page
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" in session:
        if request.method == "POST" and "twitter" in request.form:
            twitter = request.form["twitter"]
            # Find the user
            found_user = User.query.filter_by(name=session["user"]).first()
            # Assigning Twitter account
            found_user.twitter = twitter
            db.session.commit()

        if request.method == "POST" and "facebook" in request.form:
            facebook = request.form["facebook"]
            # Find the user
            found_user = User.query.filter_by(name=session["user"]).first()
            # Assigning Twitter account
            found_user.facebook = facebook
            db.session.commit()

        return render_template("profile.html", user=session["user"])
    else:
        return redirect(url_for("login"))


# Dynamic User Page
@app.route("/profiles/<username>", methods=["GET", "POST"])
def userProfiles(username):
    # Checking if the user exists in the database
    found_user = User.query.filter_by(name=username).first()
    if found_user:
        # Facebook
        facebook = found_user.facebook
        # Twitter
        twitter = found_user.twitter
        return render_template("userProfiles.html", usr=username, twitter=twitter, facebook=facebook)
    else:
        return redirect(url_for("index"))

# Dynamic Category Page
@app.route("/categories/<category>", methods=["GET", "POST"])
def categoryPages(category):
    # Checking if the category exists
    accepted_strings = {"cats", "gaming", "politics", "otheranimals", "politics", "nsfw"}
    if category in accepted_strings:
        if request.method == "POST" and "post" in request.form:
            # Post Data
            body = request.form["post"]
            if not body:
                flash(u"Posts can not be empty", "error")
            else:
                username = session["user"]
                Users = User.query.filter_by(name=username).first()

                # Post object creation
                post = Post(category, body, poster=Users, comment=[])

                # Adding the post to database
                db.session.add(post)
                db.session.commit()
        if request.method == "POST" and "comment" in request.form:
            # Comment Data
            text = request.form["comment"]
            if not text:
                print("Comments can not be empty")
            else:
                # Username of the commenter
                commenter = session["user"]
                # Post
                Posts = Post.query.filter_by(post=request.form["actualPost"]).first()
                # Comment object creation
                comment = Comment(text, mainpost=Posts, commenter=commenter)

                # Adding the comment to database
                db.session.add(comment)
                db.session.commit()

        return render_template("category.html", values=Post.query.filter_by(category=category),
                               User=User, categoryName=category)
    else:
        return redirect(url_for("index"))

# To see all the users in database
@app.route("/view", methods=["GET", "POST"])
def view():
    return render_template("view.html", values=User.query.all())




if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
