
from flask import Flask, render_template, request, redirect
import smtplib
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

# TODO if necessary
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'

# initialize the database
db = SQLAlchemy(app)


# create db model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False) # 25 characters max, nullable=False for blank name not possible
    last_name = db.Column(db.String(25), nullable=False)
    new_email = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    # TODO if necessary
    # create a function to return a string when we add sth
    def __repr__(self):
        return '<Name %r>' % self.id
        # % = primary key in the code above


# TODO if necessary
subscribers = []


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/blog')
def blog():
    return render_template("blog.html")


@app.route('/subscribe')
def subscribe():

    # TODO push data to database here or in form()?

    return render_template("subscribe.html")

# @app.route('/friends', methods=['POST', 'GET'])
# def friends():
#     if request.method == "POST":
#         friend_name = request.form['name']
#         new_friend = Friends(name=friend_name)
#
#         # push to database
#         try:
#             db.session.add(new_friend)
#             db.session.commit()
#             return redirect('/friends')
#
#         except:
#             return "There was an error adding your friend..."
#
#     else:
#         friends = Friends.query.order_by(Friends.date_created)
#         return render_template("friends.html", friends=friends)


@app.route('/programs')
def programs():
    return render_template("programs.html")


@app.route('/topics')
def topics():
    return render_template("topics.html")


@app.route('/intro')
def intro():
    return render_template("intro.html")


@app.route('/this_page')
def this_page():
    return render_template("this_page.html")


@app.route('/form', methods=['POST', 'GET'])
def form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")


    if request.method == "POST":
        first_name_db = Friends(first_name=first_name)
        last_name_db = Friends(last_name=last_name)
        email_db = Friends(new_email=email)

        # TODO fix the line
        # when = Friends.date_created()

        # push to database
        try:
            db.session.add(first_name_db)
            db.session.add(last_name_db)
            db.session.add(email_db)
            # db.session.add(when)
            db.session.commit()
            return redirect('/form')

        except:
            return "There was an error adding the Friend..."

# TODO if muted lines necessary...
    # else:
    #     return render_template("form.html", subscribers=subscribers, first_name=first_name, last_name=last_name, email=email)

    message = "You have been subscribed to my email newsletter!"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    password = os.environ.get("cameel_gm_pass")
    server.login("cameelcode@gmail.com", password)
    server.sendmail("cameelcode@gmail.com", email, message)

    if not first_name or not last_name or not email:
        error_statement = "All form fields required..."
        return render_template("subscribe.html",
                               error_statement=error_statement,
                               first_name=first_name,
                               last_name=last_name,
                               email=email)
    subscribers.append(f"{first_name} {last_name} || {email}")
    return render_template("form.html", subscribers=subscribers, first_name=first_name, last_name=last_name, email=email)










if __name__ == '__main__':
    app.run()
