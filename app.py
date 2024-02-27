#  _________________________Importing the necessry packages_________________________
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo  import MongoClient
import wolframalpha
from youtubesearchpython import VideosSearch
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import wikipedia
import openai
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from translate import Translator
# from flask_socketio import SocketIO, join_room, leave_room, send, emit
# from googletrans import Translator, LANGUAGES

# _________________________Connecting flask_________________________
app= Flask(__name__)
app.secret_key= "password"
socketio = SocketIO(app)

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
        elif text == 'button16':
            lilink = user.get('li16')
        elif text == 'button17':
            lilink = user.get('li17')
        elif text == 'button18':
            lilink = user.get('li18')
        elif text == 'button19':
            lilink = user.get('li19')
        elif text == 'button20':
            lilink = user.get('li20')
        elif text == 'button21':
            lilink = user.get('li21')
        user = db.users.find_one({'username': session['user']})
        if user:
            db.users.update_one({'username':session['user']},{'$set':{'courslist':lilink}})
    user = db.users.find_one({'username': session['user']})
    if user:
        age=user.get('age') 
        # disability = user.get('disability')
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
#extract
@app.route('/extract', methods=['GET', 'POST'])
def extract():
    user = db.users.find_one({'username': session['user']})
    if user:
        subtitle=user.get('subtitle') 
        video_links = user.get('video_links')
        id=user.get('id')
        vll=[]
        for i in video_links:
            sep_l = i.split('=')
            idi = sep_l[-1]
            vll.append(idi)
        id1=vll[1]
        id2=vll[2]
        id3=vll[3]
        id4=vll[4]
        id5=vll[5]
        id6=vll[6]
    return render_template('extract.html', subtitle=subtitle,id=id,id1=id1,id2=id2,id3=id3,id4=id4,id5=id5,id6=id6)

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
        if target_language == 'tamil':
            ask = """பொதுவாக போக்குவரத்தில் கட்டமைக்கப்பட்டுள்ள செயல்பாடுகள் மூலம், தொடர்புடைய தகவல்களை நிறைவு செய்கின்றன. இந்த செயல்பாடுகள் கோப்புகளை மீட்டரை அச்சினால் அல்லது போதுமான அமைப்புகளை உருவாக்குவதன் மூலம் இயலாது. இவை மூலம் தகவல்களை பொதுவாக உருவாக்குவது முக்கியம், ஏனென்றால் சாதாரணமாகவும் செயல்படுத்தப்படும் கட்டமைப்புகள் வெவ்வேறு கணக்கீடுகளைத் தருகின்றன. பிரோக்ராம்மிங் என்பது இதனைப் பயன்படுத்தி தொடர்ந்து கொள்ள முடியும். அதனால், பிரோக்ராம்மிங் பயிற்சிக்கு ஆரம்பிக்க வேண்டிய முதல் படி, நீங்கள் நிறுவும் செயல்பாடுகளை மற்றும் நீங்கள் எவ்வாறு அவற்றை பயன்படுத்துகின்றீர்கள் என்பதை அறிய வேண்டும். பிரோக்ராம்மிங் பயிற்சியின் மூலம், நீங்கள் தனிநபராக விரும்பும் பொருள்களை உருவாக்க, உள்ளடக்கி முக்கியமான தகவல்களை சரியான கணக்கீடுகள் கொண்டு வைக்க முடியும். இது நான்கு அடிப்படைகளில் உள்ளது - முதலாக, மூலம் கணினியில் உள்ள விசைகளை காணவும், அதன் பயன்பாட்டில் விரும்பும் மென்பொருள்களை அறிந்து கொள்ளவும், பின்னர் நீங்கள் தனிநபராக செயல்படுத்துவதற்கு செயல்பாடுகளை சேர்க்க முடியும். இன்னும், பிரோக்ராம்மிங் பயிற்சியின் முடிவில், நீங்கள் உங்கள் பயிற்சியின் படி எப்படி இருந்தது என்பதை அறிந்து கொள்ள வேண்டும். இதன் மூலம், நீங்கள் உங்கள் அதிக அளவிற்கு பொதுவாக
            உதவும் செயல்பாடுகளை கையாள முடியும். இந்த கல்வியால் நீங்கள் உங்கள் வேலையில் போக உதவும் பெரும் அரசியல் நகரில் மட்டுமே பயன்படுத்த முடியும் என்பதை நினைவில் கொள்ளுங்கள். இதன் மூலம், நீங்கள் வாழ்க்கையில் அனைவருக்கும் உதவவும் செய்வீர்கள் என்று நாங்கள் உறுதியாக அரசியல் நகரில் செயல்படுத்துகின்றோம்."""

        elif target_language == 'telugu':
            ask = """[సంగీతం] గ్రహాంతరవాసులకు స్వాగతం.పక్కపక్కన ఒక వస్తువు సరిగ్గా ప్రతి వస్తువు ఏదో తెలుసుకోవాలి కానీ ఆప్స్‌లో మధ్యయుగ విషయానికి వస్తే మనకు రెండు రకాల వేరియబుల్స్ ఉన్నాయి, మొదటిది ఇన్‌స్టాన్స్ వేరియబుల్ మరియు రెండవదిక్లాస్ వేరియబుల్ అన్నింటినీ మీరు స్టాటిక్ వేరియబుల్స్ అని పిలవవచ్చు, వాటి మధ్య తేడా ఏమిటి, దీని గురించి ఏమీ లేదు, నేను ఈ కాల్‌ని తీసివేయనివ్వండి సరే మనం ఇప్పటివరకు ఏమి చేసినా సరే కాబట్టి నన్ను శుభ్రం చేయనివ్వండిఇది సరే కాబట్టి ఇది మా సాదా స్లేట్ నుండి ప్రారంభమవుతుంది కాబట్టి ఇక్కడ మరొక తయారు చేసిన ఉదాహరణతో వెళ్దాం, మనమందరం కార్లను సరిగ్గా ఇష్టపడితే క్లాస్ కాల్ అస్కాట్ ఓకే తీసుకుందాం, కాబట్టి మనకు క్లాస్ కార్డ్ మరియు సహ ఉన్నాయి అని చెప్పండిప్రతి కారు వేర్వేరు వేరియబుల్‌లను కలిగి ఉంటుంది, అయితే మీరు కంపెనీ పేరును పేర్కొనవచ్చు, మీరు పని చేసే ఇంజనీర్ రకాన్ని మరియు అది మీకు ఇచ్చే మైలేజీని పేర్కొనవచ్చు కాబట్టి మేము విభిన్నంగా ఉన్నాము.వేరియబుల్స్ సరే కాబట్టి నేను ఇక్కడ ఆ వేరియబుల్స్ ఉపయోగించాలనుకుంటే నేను ఏమి చేస్తాను అంటే మనం దానిలో ఒక ఫంక్షన్ s ను ఉపయోగించాలి కాబట్టి మీరు init ఫంక్షన్ అని చెబుతారు మరియు దీనిలో మీరు ఆ వేరియబుల్స్‌ను సరిగ్గా నిర్వచించవచ్చు నేను సెల్ఫ్ అని చెప్పగలనుడాట్ మైలేజ్ మరియు నేను మైలేజ్ 10 అని చెప్పండి మరియు నేను కంపెనీని చెబుతాను కాబట్టి కంపెనీ BMW ఏదైనా యాదృచ్ఛిక కంపెనీ అని చెప్పనివ్వండి అవి పర్వాలేదు కాబట్టి మనకు ప్రస్తుతం ఈ రెండు విలువలు ఉన్నాయి.wo వేరియబుల్స్‌ని ఇన్‌స్టాన్స్ వేరియబుల్ అంటారు కాబట్టి మేము మైలేజ్ గురించి మాట్లాడతాము మరియు Comm ఇవి ఇప్పుడు ఉదాహరణగా ఎందుకు ఉన్నాయి ఎందుకంటే వస్తువు మారినప్పుడు మీ మార్గం మారినప్పుడు ఈ విలువ కూడా మారుతుందిడిఫాల్ట్ విలువ 10 మరియు బియాండ్ డబ్ల్యు అయితే మీరు దానిని మార్చవచ్చు సరైన ఉదాహరణ మేము ఇంతకు ముందు మీకు ఒక సంగ్రహావలోకనం ఇవ్వడానికి నేను మొదటిది c1 అని చెబుతాను మరియు ఇది నేను చేసిన మొదటి వస్తువుot c2 అంటే మళ్లీ మనకు c1 c2 వచ్చింది, ఇప్పుడు మనకు రెండు వేర్వేరు వస్తువులు వచ్చాయి మరియు ఆబ్జెక్ట్ రెండూ వేరియబుల్స్ కోసం వేర్వేరు ప్రాంతం ద్వారా వేర్వేరు వేరియబుల్స్ కలిగి ఉంటాయి మరియు ఇప్పుడు నేను విలువను ప్రింట్ చేస్తే నేనుc.com అని చెబుతాను మరియు నేను C 1 డాట్ మైలేజ్‌ని కూడా ప్రింట్ చేయాలనుకుంటున్నాను కాబట్టి నేను రెండు వేరియబుల్స్‌కు రెండింటినీ ప్రింట్ చేయాలనుకుంటున్నాను, కాబట్టి మీరు చూడగలరు c1 మైలేజ్ c2 comc నుండి మైలేజ్‌కి ఎప్పుడు సరిపోతుందో చూడలేము మరియు నేను ఫన్d ఈ కోట్ వాస్తవానికి అదే విలువలను ప్రింట్ చేస్తుంది ఎందుకంటే అవి ఒకే విధంగా ఉంటాయి, అయితే మనం దానిని మార్చగలమా అవును మనం మార్చగలము కాబట్టి నేను c1 కోసం మారితే నేను చెప్తాను కాబట్టి C 1 డాట్ మైలేజీని చెప్పండి c1 - 10 నుండి మార్పులు - leకొన్ని కార్లతో మీకు తెలిసినది ఇదే అని చెప్పండి మరియు ఇది ప్రత్యేకంగా అమలు చేయబడుతోంది, ఇప్పుడు విలువ మారుతోంది కాబట్టి కోర్సు పుస్తకాలు భిన్నంగా ఉంటాయి మరియు అవి వేర్వేరు విలువలను కలిగి ఉంటాయి, అయితే నేను ఏమి కోరుకుంటానుఅన్ని ఆబ్జెక్ట్‌లకు సాధారణమైన వేరియబుల్‌ని సృష్టించడానికి ఈ వేరియబుల్స్ ఇన్‌స్టాన్స్ వేరియబుల్‌గా ఉంటాయి, అవి వేర్వేరు వస్తువులకు భిన్నంగా ఉంటాయి, అయితే మీరు ఒక వస్తువును మార్చినట్లయితే అది ప్రభావితం చేయదుఇతర వస్తువులు మీరు వేరియబుల్‌ని కలిగి ఉండాలనుకుంటే అది అన్ని ఇతర వస్తువులను ప్రభావితం చేస్తుంది, ఉదాహరణకు కారులో చక్రాల సంఖ్య డిఫాల్ట్‌గా పూర్తి కుడివైపు 4 సరైనది అయితే భవిష్యత్తులో యోమీకు కొత్త కాన్సెప్ట్ వచ్చింది మరియు వారు ఇప్పుడు హే అంటున్నారు, ఈసారి మనకు ఐదు టైర్లు లేదా ఐదు చక్రాలు ఉన్నాయి,
             మనకు ఐదు ఉపయోగం ఎందుకు ఉందో నాకు తెలియదు, అయితే మీరు ఏమి చేస్తారో ఈ సందర్భంలో ఊహించుకుందాం అంటే మీరు ఒక వర్‌ని నిర్వచిస్తారుదానిలో వెలుపల iable ఓకే ఎందుకంటే మీరు అన్నింటినీ సృష్టించినట్లయితే, దానిలోని వేరియబుల్‌ను మేము నిర్వచించినట్లయితే అది ఒక ఉదాహరణ వేరియబుల్ అవుతుంది.ఒక క్లాస్ వేరియబుల్ నేను బిల్లులు అంటున్నాను కాబట్టి ఇవి డిఫాల్ట్‌గా ఉన్నాయని అనుకుందాం, అయితే ఆహారం నాలుగు సరిగ్గా ఉంటుంది మరియు నేను వీల్స్‌ని ప్రింట్ చేస్తే ఇప్పుడు మీరు ఎలా ప్రింట్ చేయగలరో చక్రాలను ఎలా ప్రింట్ చేస్తారు?మీరు C 1 డాట్ వీల్స్ అని చెప్పవచ్చు మరియు ఇక్కడ అలాగే C 2 డాట్ వీల్స్ అని చెప్పవచ్చు మరియు ఇప్పుడు ఈ కోడ్‌ని రన్ చేద్దాం మరియు మనకు 4 &amp; 4 అవుట్‌పుట్ వచ్చింది కాబట్టి మీరు చక్రాలను యాక్సెస్ చేయాలనుకుంటే మీరు C 1 అని చెప్పవచ్చుడాట్ వీల్స్ మరియు సి 2 డాట్ వీల్స్ సిజి ఆఫ్ ఆబ్జెక్ట్ నేమ్‌ని ఉపయోగించి మేము క్లాస్ పేరును కూడా ఉపయోగించవచ్చు ఎందుకంటే మీరు మిల్లు మరియు కమ్ గురించి మాట్లాడితే అది ఆబ్జెక్ట్ రైట్‌కు ప్రత్యేకంగా ఉంటుంది కానీ చక్రాల విషయంలో అలా కాదుచక్రాలు అన్ని వస్తువులకు సాధారణం కాబట్టి ప్రతి వస్తువు దాని విలువను పంచుకోగలదు కాబట్టి మేము వస్తువు పేరును ఉపయోగించవచ్చు ఆల్బా క్లాస్‌నేమ్ రెండు వర్క్‌లను ఉపయోగించవచ్చు కాబట్టి మీరు సరైన విలువను పొందుతున్నారుమీరు విలువను మార్చాలనుకుంటే దాని విలువను మార్చండి మీరు ఇక్కడకు రావచ్చు మరియు మీరు విలువను మార్చవచ్చు ఏమి జరుగుతుందో చూడండి మీ మెమరీలో మీకు వేరే నేమ్‌స్పేస్ ఉంది ఇప్పుడు అది నేమ్‌స్పేస్ స్థలంమీరు ఒక ఆబ్జెక్ట్ లేదా వేరియబుల్స్ విభిన్నమైన నేమ్‌స్పేస్‌ని సృష్టించే చోట మనం నేమ్‌స్పేస్‌ని రెండింతలు చేయాలి, ఒకటి క్లాస్ నేమ్ స్పేస్, ఇక్కడ మీరు అన్ని క్లాస్ వేరియబుల్స్‌ను స్టోర్ చేస్తారు, ఆపై మనకు ఒక ఉదాహరణ పేరు sp ఉంటుంది.మీరు అన్ని ఇన్‌స్టాన్స్ వేరియబుల్‌ను సృష్టించే ఏస్ కాబట్టి వాసన మరియు ప్రశాంతత ఉండే ఈ వేరియబుల్స్ ఇన్‌స్టాన్స్ లైట్ కాబట్టి అవి ఇన్‌స్టాన్స్ నేమ్ స్పేస్‌కు చెందినవి కాబట్టి ఇది క్లాస్ నేమ్‌స్పేస్ రికి చెందినదిght కాబట్టి మీరు చక్రాలతో పని చేయాలనుకుంటే, మీరు దానిని సవరించాలనుకుంటే, మీరు కార్ డాట్ V గుర్తు 20 నుండి 5 వరకు చెప్పాల్సిన తరగతి వస్తువును ఉపయోగించాలి, ఇప్పుడు మీరు చక్రాల విలువను మార్చిన క్షణం అది మొత్తం మీద ప్రభావం చూపుతుంది.ఇ ఆబ్జెక్ట్‌లు సరిగ్గా భాగస్వామ్యం చేయబడినందున ఈ చక్రం అన్ని వస్తువుల మధ్య భాగస్వామ్యం చేయబడింది మరియు ఇప్పుడు ఈ కోడ్ కోసం మీరు అవుట్‌పుట్ 5 మరియు 5 అని చూడవచ్చు కాబట్టి అది మీ ప్లస్ వేరియబుల్ కాబట్టి నాకు గుర్తున్న పాయింట్ ఇదిమా వద్ద రెండు స్థాయి వేరియబుల్స్ ఇన్‌స్టాన్స్ వేరియబుల్స్ మరియు క్లాస్ వేరియబుల్స్ ఉన్నాయి లేదా నిజానికి క్లాస్ వేరియబుల్స్‌ని స్టాటిక్ వేరియబుల్స్ అని కూడా పిలుస్తారు, కాబట్టి ఈ వీడియో నుండి చూద్దాం కామెంట్ సెక్టిలో మీరు ఆ అర్థాన్ని ఆస్వాదించారని నేను ఆశిస్తున్నానుమీకు ఇంకా ఏవైనా ప్రశ్నలు ఉంటే మరియు తదుపరి వీడియోలో మేము వివిధ రకాల పద్ధతుల గురించి మాట్లాడుతాము కాబట్టి వేచి ఉండండి అంతే అందరికీ బై బై"""
        # url = "https://nlp-translation.p.rapidapi.com/v1/translate"
        # querystring = {"text":subtitle,"to":"ta","from":"en"}

        # headers = {
        #     "X-RapidAPI-Key": "43cc727829msh5644c8389123bf7p18e60cjsnc980a33f130a",
        #     "X-RapidAPI-Host": "nlp-translation.p.rapidapi.com"
        # }

        # response = requests.get(url, headers=headers, params=querystring)
        # ask = response.json()["translated_text"][target_language]
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

user_languages = {} 
user_names = {} 
def translate_message(message, source_language, target_language):
    translator = Translator(to_lang = target_language)
    translated_message = translator.translate(message)
    return translated_message

# Group Chat Page.
@app.route('/GroupChat')
def GroupChat():
    return render_template('GroupChat.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = data['message']
    source_language = user_languages[room]
    user_name = user_names[request.sid]
    
    for client_room, target_language in user_languages.items():
        if client_room != room:  # Exclude the source user's room
            translated_message = translate_message(message, source_language, target_language)
            emit('user_message', {'user': user_name, 'message': translated_message}, room=client_room)

@socketio.on('create')
def handle_create(data):
    room = data['room']
    user_languages[room] = data['language']
    user_names[request.sid] = data['user']
    join_room(room)
    emit('system_message', {'message': f'You have created and joined room {room}.'})
    emit('system_message', {'message': 'Translation is enabled in this room.'}, room=room)

@socketio.on('join')
def handle_join(data):
    room = data['room']
    user_languages[room] = data['language']
    user_names[request.sid] = data['user']
    join_room(room)
    emit('system_message', {'message': f'You have joined room {room}.'})
    emit('system_message', {'message': 'Translation is enabled in this room.'}, room=room)

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    user_name = user_names[request.sid]
    leave_room(room)
    emit('system_message', {'message': f'{user_name} has left the room.'}, room=room)
    del user_names[request.sid] 
    emit('update_users', {'users': list(user_names.values())}, room=room)  

if __name__== "__main__":
    socketio.run(app, debug=True)