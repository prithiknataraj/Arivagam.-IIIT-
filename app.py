#  _________________________Importing the necessry packages_________________________
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo  import MongoClient
import wolframalpha
from youtubesearchpython import VideosSearch
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import wikipedia
import openai
# from flask_socketio import SocketIO, join_room, leave_room, send, emit
# from googletrans import Translator, LANGUAGES

# _________________________Connecting flask_________________________
app= Flask(__name__)
app.secret_key= "password"

# _________________________Connecting OpenAI_________________________
openai.api_key = "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"

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
                     'age':age, 'subtitle':subtitle,
                     'id':id,'preflang1':preflang1, 'gender':gender, 
                     'preflang2':preflang2,'confpassword':confpassword}
        db.users.insert_one(user_data)

        session['user'] = username
  
        return redirect(url_for('home'))

    return render_template('SignUp.html')

# Home Page.
@app.route('/home', methods=['GET','POST'])
def home():
    text = request.data.decode('utf-8')
    if text:
        user = db.users.find_one({'username': 'yukthi@gmail.com'})
        if text == 'button1':
            lilink = user.get('li1')
        elif text == 'button2':
            lilink = user.get('li2')
        elif text == 'button3':
            lilink = user.get('li3')
        elif text == 'button4':
            lilink = user.get('li4')
        elif text == 'button5':
            lilink = user.get('li5')
        elif text == 'button6':
            lilink = user.get('li6')
        elif text == 'button7':
            lilink = user.get('li7')
        elif text == 'button8':
            lilink = user.get('li8')
        elif text == 'button9':
            lilink = user.get('li9')
        elif text == 'button10':
            lilink = user.get('li10')
        elif text == 'button11':
            lilink = user.get('li11')
        elif text == 'button12':
            lilink = user.get('li12')
        elif text == 'button13':
            lilink = user.get('li13')
        elif text == 'button14':
            lilink = user.get('li14')
        elif text == 'button15':
            lilink = user.get('li15')
        user = db.users.find_one({'username': session['user']})
        if user:
            db.users.update_one({'username':session['user']},{'$set':{'courslist':lilink}})
    user = db.users.find_one({'username': session['user']})
    if user:
        age=user.get('age') 
    if request.method == 'POST':
        to_search = request.form['ytsearch']
        playsearch = request.form['ytplay']
        if playsearch:
            return redirect(url_for('Video'))
        videosSearch = VideosSearch(to_search, limit=7)
        results = videosSearch.result()
        video_links = []
        for result in results['result']:
            video_links.append(result['link'])
        link = video_links[0]
        sep_l = link.split('=')
        id = sep_l[-1]
        try:
            transcript = YouTubeTranscriptApi.get_transcript(id)
        except:
            try:
                link = video_links[1]
                sep_l = link.split('=')
                id = sep_l[-1]
                transcript = YouTubeTranscriptApi.get_transcript(id)
            except:
                link = video_links[2]
                sep_l = link.split('=')
                id = sep_l[-1]
                transcript = YouTubeTranscriptApi.get_transcript(id)
        script = ""
        for text in transcript:
            t = text["text"]
            if t != '[Music]':
                script += t + " "

        subtitle = script

        if subtitle:
            user = db.users.find_one({'username': session['user']})
            if user:
                db.users.update_one({'username':session['user']},{'$set':{'subtitle':subtitle}})
                db.users.update_one({'username':session['user']},{'$set':{'id':id}})
                db.users.update_one({'username':session['user']},{'$set':{'video_links':video_links}})
            return redirect(url_for('extract'))
    return render_template('Home.html',age=age)

# Video Page.
@app.route('/Video',methods=['GET','POST'])
def Video():
    return render_template('Video.html')

# ProfileEdit Page.
@app.route('/ProfileEdit',methods=['GET', 'POST'])
def ProfileEdit():
    if request.method=='POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['email']
        password = request.form['password']
        confpassword = request.form['confpassword']
        age = request.form['age']
        gender = request.form['gender']
        preflang1 = request.form['preflang1']
        preflang2 = request.form['preflang2']
        user = db.users.find_one({'username': session['user']})
        if user:
            db.users.update_many({'username':session['user']},{'$set':{'username': username, 'password': password,
                     'firstname': firstname, 'lastname': lastname,
                     'age':age,
                     'preflang1':preflang1, 'gender':gender, 
                     'preflang2':preflang2,'confpassword':confpassword}})
  
        return redirect(url_for('home'))
    user = db.users.find_one({'username': session['user']})
    if user:
        username = user.get('username')
        password = user.get('password')
        firstname = user.get('firstname')
        lastname = user.get('lastname')
        age = user.get('age')
        gender = user.get('gender')
        preflang1 = user.get('preflang1')
        preflang2 = user.get('preflang2')
        confpassword = user.get('confpassword')
    return render_template('ProfileEdit.html',username = username,password=password,firstname=firstname,lastname=lastname,age=age,gender=gender,preflang1=preflang1,preflang2=preflang2,confpassword=confpassword)

# Courses Page.
@app.route('/Courses',methods=['GET','POST'])
def Courses():
    user = db.users.find_one({'username': session['user']})
    if user:
        courlist = user.get('courslist')
    transcript = YouTubeTranscriptApi.get_transcript(courlist[0])
    script = ""
    for text in transcript:
        t = text["text"]
        if t != '[Music]':
            script += t + " "

    subtitle = script
    
    id1=courlist[0]
    id2=courlist[1]
    id3=courlist[2]

    if request.method=='POST':
        target_language = request.form['django']
        url = "https://nlp-translation.p.rapidapi.com/v1/translate"
        querystring = {"text":subtitle,"to":target_language,"from":"en"}

        headers = {
            "X-RapidAPI-Key": "43cc727829msh5644c8389123bf7p18e60cjsnc980a33f130a",
            "X-RapidAPI-Host": "nlp-translation.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        ask = response.json()["translated_text"][target_language]
        return render_template('Courses.html',subtitle=ask,id1=id1,id2=id2,id3=id3)

        
    return render_template('Courses.html',subtitle=subtitle,id1=id1,id2=id2,id3=id3)

# Chat ChatBot Page.
@app.route('/ChatBot',methods=['GET','POST'])
def ChatBot():
    if request.method=='POST':
        user_input = request.form['dbt']
        bot_response = chat(user_input)
        return jsonify({'output': bot_response})
    else:
        return render_template('ChatBot.html')
    
# Group Chat Page.
# @app.route('/GroupChat')
# def GroupChat():
#     return render_template('GroupChat.html')

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')

# @socketio.on('message')
# def handle_message(data):
#     room = data['room']
#     message = data['message']
#     source_language = user_languages[room]
#     user_name = user_names[request.sid]
    
#     for client_room, target_language in user_languages.items():
#         if client_room != room:  # Exclude the source user's room
#             translated_message = translate_message(message, source_language, target_language)
#             emit('user_message', {'user': user_name, 'message': translated_message}, room=client_room)

# @socketio.on('create')
# def handle_create(data):
#     room = data['room']
#     user_languages[room] = data['language']
#     user_names[request.sid] = data['user']
#     join_room(room)
#     emit('system_message', {'message': f'You have created and joined room {room}.'})
#     emit('system_message', {'message': 'Translation is enabled in this room.'}, room=room)

# @socketio.on('join')
# def handle_join(data):
#     room = data['room']
#     user_languages[room] = data['language']
#     user_names[request.sid] = data['user']
#     join_room(room)
#     emit('system_message', {'message': f'You have joined room {room}.'})
#     emit('system_message', {'message': 'Translation is enabled in this room.'}, room=room)

# @socketio.on('leave')
# def handle_leave(data):
#     room = data['room']
#     user_name = user_names[request.sid]
#     leave_room(room)
#     emit('system_message', {'message': f'{user_name} has left the room.'}, room=room)
#     del user_names[request.sid] 
#     emit('update_users', {'users': list(user_names.values())}, room=room)  
    
# Meeting In Page.
@app.route('/MeetingIn')
def MeetingIn():
    return render_template('MeetingIn.html')

# Meeting Page.
@app.route('/Meeting')
def Meeting():
    return render_template('Meeting.html')

# Meeting Home Page.
@app.route('/MeetingHome',methods=['GET', 'POST'])
def MeetingHome():
    if request.method=='POST':
        roomID = request.form['roomID']
        return redirect("/vdocall?roomID="+roomID)
    return render_template('MeetingHome.html')

# ________________________________________________Functions________________________________________________
# ChatBot Function.

def chat(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

if __name__== "__main__":
    app.run(debug= True)
