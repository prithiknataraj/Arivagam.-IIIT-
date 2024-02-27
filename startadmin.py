from flask import Flask,session,render_template,request,redirect,g,url_for
from pymongo import MongoClient
from youtubesearchpython import VideosSearch
from youtube_transcript_api import YouTubeTranscriptApi
import wolframalpha
from translate import Translator

app=Flask(__name__)

client=MongoClient()
client=MongoClient("mongodb://localhost:27017/")

db=client['Arivagam-IIIT']
app.secret_key = 'password'
users=db['users']

lilink1 = ['pQxDwez0NVU','e_04ZrNroTo','020g-0hhCAU']
lilink2 = ['B3Fv2X8EKfE','JcNTptn8twU','SUt8q0EKbms']
lilink3 = ['GD6YOvKt_xw','lTioAWQ2KRE','HkUIN8Uo9hE']
lilink4 = ['zWO-bTi6u8M','WzmIi9oWfQI','xEF8shaU_34']
lilink5 = ['AgINA9_IFiI','iONDebHX9qk','0ARKQqTtnlQ']
lilink6 = ['n8Nx5iGKVFE','IwW0GJWKH98','TMubSggUOVE']
lilink7 = ['5Q0FlxcEEIw','PVoTRu3p6ug','NybHckSEQBI']
lilink8 = ['oxg0K1BuPoo','s-Xpa5UZAZs','Lbv6WbjIQW0']
lilink9 = ['cPjRaw8CVr8','DjlgfPeHnek','yg8irmc_fiU']
lilink10 = ['RSQjxL5WRNM','b093aqAZiPU','TTepNRy0wj8']
lilink11 = ['T9lt6MZKLck','mhd9FXYdf4s','V5ArB_GFGYQ']
lilink12 = ['rz4Dd1I_fX0','3NhBzKP03gY','bKKJkxqIg94']
lilink13 = ['CWAi_2oLhYg','nu_pCVPKzTk','jBzwzrDvZ18']
lilink14 = ['sVxBVvlnJsM','CBYHwZcbD-s','MLqHDsBOC4c']
lilink15 = ['tSodBEAJz9Y','qiQR5rTSshw','fErDcUtd8fA']
lilink16 = ['bFv_mLwBvHc','Vj_13bdU4dU','0LIV0miyxR8']
lilink17 = ['bFv_mLwBvHc','QaqYJjNH0AU','VtbYvVDItvg']
lilink18 = ['bFv_mLwBvHc','sLqdPipf1UM','f_nVhrOgpYw']
lilink19 = ['yHsl3zqayF8','xCtskrNlq1M','-CpZAH6elIc']
lilink20 = ['Dpo6H_xYwgg','JzO-DoJNZCE','17MelulklBY']
lilink21 = ['1W17IfnBFDc','dj0W4CrLtgI','kO_eRnhPtZM']

# yHsl3zqayF8
user = db.users.find_one({'username': 'yukthi@gmail.com'})
if user:
    db.users.update_many({'username':'yukthi@gmail.com'},{'$set':{'li1':lilink1,'li2':lilink2,'li3':lilink3,'li4':lilink4,'li5':lilink5,'li6':lilink6,
                                                               'li7':lilink7,'li8':lilink8,'li9':lilink9,'li10':lilink10,'li11':lilink11,'li12':lilink12,
                                                               'li13':lilink13,'li14':lilink14,'li15':lilink15,'li16':lilink16,'li17':lilink17,'li18':lilink18,
                                                               'li19':lilink19,'li20':lilink20,'li21':lilink21}})