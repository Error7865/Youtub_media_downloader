
#global variable 'stream' 70 'download' 53 'cont'  89, thumb "url of mp3 file"


from . import you
from flask import render_template, flash, redirect, url_for, send_file, request
from ..forms import You, Download
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
import os
from moviepy.editor import AudioFileClip

import requests
from mutagen.id3 import ID3, APIC

def list_video_res(videos):         #It return a dictionary of all resulation of progressive videos(like 144p, 360p, 720p)
    res={}                  #dict will store all video resolution like 720: 13
    for item in videos:
        item=str(item)
        key=int(str(item.split('res="')[1]).split('p"')[0])       #It will return the integer vlaue of resolution like 144, 360 etc
        itag=int(str(item.split('itag="')[1]).split('" mi')[0])        #It will return all the values of itag
        sub={key : itag}
        res.update(sub)
    return res


def list_audio(audios):         #It will return list of audio like 48,320 etc
    aud={}                  #list will store all audio
    for item in audios:
        item=str(item)
        key=int(str(item.split('abr="')[1]).split('kbps"')[0])       #It will return the integer vlaue of resolution like 144, 360 etc
        itag=int(str(item.split('itag="')[1]).split('" mi')[0])        #It will return all the values of itag
        sub={key : itag}
        aud.update(sub)
        
    return aud                                          #It will return the integer value of audio abr : itag value

def dict_type(media):           #It return dict int(res or abr): type
    typ={}
    for item in media:
        item=str(item)
        key=int(str(item.split('itag="')[1]).split('" mi')[0])        #It will return all the values of itag
        value=str(str(item.split('mime_type="')[1]).split('" ')[0])  #this is value of typ dict
        sub={key : value}
        typ.update(sub)
    return typ



# def generate_url()

@you.route('/', methods=['POST', 'GET'])
def home():
    fom=You()
    down=Download()     #download form
    global download
    download=False
    # print('Download at first ', download)

    itag=None
    itag=request.args.get('link')
    print('itag: ', itag)
    

    if fom.validate_on_submit():
        link=fom.link.data
        # print(link)
        delete()            #it will delete if any file presen Download file
        try:
            yt=YouTube(link)        #creating link object
            yt.register_on_complete_callback(on_complete)               #register after download function

        except :
            flash("Please check link again.")
            return redirect(url_for('you.home'))
        
        global stream
        stream=yt.streams       #all streams

        global thumb
        thumb=yt.thumbnail_url
        title=yt.title      #title of youtube video
        author=yt.author    #author of youtube video

        info={'title': title, 'author': author}         #for show video title and author

        videos=stream.filter(progressive=True)          #List of all progressive streams
        audios=stream.filter(only_audio=True)           #List of all audio strems
        
        res=list_video_res(videos)                      #dict of all videos resolution
        re_typ=dict_type(videos)
        aus=list_audio(audios)                          #dict of all audios abr : itag 
        au_typ=dict_type(audios)
        return render_template('you.html', fo=fom, video=res, audio=aus, down=down, info=info, v_type=re_typ, a_type=au_typ)

    # if down.validate_on_submit():
    #     itag=down.itag.data
    #     print('itag: ', itag)
    #     global cont         #It will requird for next to covert mp4 to mp3
    #     cont=stream.get_by_itag(itag) 
    #     print('cont: ', cont)  
    #     loc=os.getcwd()+'\\app\\test'
    #     cont.download(loc)

    if itag is not None:
        print('itag value: ', itag)
        global cont
        cont=stream.get_by_itag(itag)
        print('cont inside itag: ', cont)
        loc=os.getcwd()+'\\app\\test\\'
        cont.download(loc)
        
    if download:
        check_audio(str(cont))
        file=os.listdir('app/test')[0]  #update
        name=os.getcwd()+'\\app\\test\\'+file   #url update
        # print('Its execute')
        return send_file(name, as_attachment=True)
    else:
        print('Thats not execute ', download)

    return render_template('you.html', fo=fom, video=[], audio=[], info={})

# @you.route('/<link>')
# def  sub_home(link):
#     print('Inside sub_home',link)
#     return redirect(url_for('you.home'))


def delete():            #This function check any file presenton download file or not if present then it delete that
    files=os.listdir('app/test')
    if files !=[]:
        for i in files:
            os.remove('app/test/'+i)
    

def on_complete(stream, file_path):         #operation after download media
    global download
    download=True       #set True means in server download completed
    print('file ad',file_path)
    # print(stream)
    print('file downloade', download)
    

    return None

def down_img(url, audio):          #It will download thumbnail of video
    if thumb is not None:
        r=requests.get(url).content
        with open(os.getcwd()+'\\app\\thumbnail\\img.jpg', 'wb') as img:         #img.jpg is a static name
            img.write(r)
        add_cover(audio)
    else: 
        pass

def add_cover(audio):        #This func add thumbnail as cover to the mp3 file
    url=os.getcwd()+'\\app\\thumbnail'      #this is thumbnail url
    if os.listdir(url)!=[]:
        img=open(url+'\\img.jpg', 'rb')         #img is a static name for each thumbnail
        audio=ID3(os.getcwd()+'\\app\\test\\'+audio)
        audio.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=img.read()))
        audio.save()
        img.close()
        os.remove(url+'\\img.jpg')


def check_audio(sub):       #This will check file audio of not
    print('Inside check_audio')
    h=sub.find('abr=')
    print('sub= ', sub)
    print('h= ', h)
    if h>0:
        to_mp3()
    else:
        print('Not execute to_mp3 ')



def to_mp3():       #it convert the function to mp3
    print('Inside to_mp3')
    file=os.listdir(os.getcwd()+'\\app\\test\\')[0]
    sound=AudioFileClip(os.getcwd()+'\\app\\test\\'+file)
    sub_file=file.split('.')[0]
    sound.write_audiofile(os.getcwd()+'\\app\\test\\'+sub_file+'.mp3')
    os.remove(os.getcwd()+'\\app\\test\\'+file)         #it remove .mp4 file not .mp3 file
    down_img(thumb, audio=sub_file+'.mp3')
    