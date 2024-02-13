#  _________________________Importing the necessry packages_________________________
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo  import MongoClient
import wolframalpha

# _________________________Connecting flask_________________________
app= Flask(__name__)
app.secret_key= "password"

# _________________________Connecting MongoDB_________________________
client= MongoClient("mongodb://localhost:27017/")
db= client["Arivagam-IIIT"]
users= db["users"]
chat= db["chat_messages"]

# _________________________Connecting Wolframalpha_________________________
client= wolframalpha.Client('6WAEP9-R9GHYET35U')

# _________________________Connecting HTML_________________________
# Landing Page
@app.route("/")
def LandingPage():
    return render_template("LandingPage.html")

# Login Page
@app.route('/Login', methods=['GET','POST'])
def Login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'yukthi@gmail.com':
            return redirect(url_for('admin'))

        user = db.users.find_one(
            {'username': username, 'password': password})

        if user:
            session['user'] = username
            dis = user.get('disability')
            if dis == 'dyslexia':
                return redirect(url_for('dyshome'))
            elif dis == 'deaf':
                return redirect(url_for('hearhome'))
            return redirect(url_for('home'))
        else:
            correction = "Invalid username or password"
            return render_template('Login.html',correction=correction)

    return render_template('Login.html')

# Sign-Up Page
@app.route('/SignUp', methods=['GET','POST'])
def SignUp():

    if request.method=='POST':

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['email']
        password = request.form['password']
        confpassword = request.form['confpassword']
        age = request.form['age']
        gender = request.form['gender']
        disability = request.form['disability']
        preflang1 = request.form['preflang1']
        preflang2 = request.form['preflang2']
        hist1=[]
        hist2=[]
        hist3=[]
        subtitle=""
        id=""

        if db.users.find_one({'username': username}):
            correction = "Mail-ID alraedy taken"
            return render_template('SignUp.html',correction=correction)
        elif password != confpassword:
            correction = "Passwords are not similar"
            return render_template('SignUp.html',correction=correction)

        user_data = {'username': username, 'password': password,
                     'firstname': firstname, 'lastname': lastname,
                     'history1':hist1,'history2':hist2, 'history3':hist3,
                     'age':age, 'disability':disability, 'subtitle':subtitle,
                     'id':id,'preflang1':preflang1, 'gender':gender, 
                     'preflang2':preflang2,'confpassword':confpassword,"elite":"no"}
        db.users.insert_one(user_data)

        session['user'] = username
        if disability == 'dyslexia':
            return redirect(url_for('dyshome'))
        elif disability == 'deaf':
            return redirect(url_for('hearhome'))
  
        return redirect(url_for('home'))

    return render_template('SignUp.html')

if __name__== "__main__":
    app.run(debug= True)