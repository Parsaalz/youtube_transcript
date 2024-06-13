from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pytube import YouTube
from django.conf import settings
import os
import assemblyai as aai
def blog_page(request):
    return render(request,'base.html')
@csrf_exempt
def generate_blog(request):
    if request.method=="POST":
        try:
            data=json.loads(request.body)
            yt_link=data["link"]
            return JsonResponse({"content":yt_link})
        except(KeyError,json.JSONDecodeError):
            return JsonResponse({"error":"invalid data sent"},status=400)
        title=get_title(yt_link)
        transcription=get_transcription(yt_link)
        if not transcription:
            return JsonResponse({"error":"failed to get transcript"},status=500)
    else:
        return JsonResponse({"eror":"invalid request method"},status=405)

def get_title(link):
    yt=YouTube(link)
    title=yt.title
    return title

def get_audio(link):
    yt=YouTube(link)
    video=yt.streams.filter(only_audio=True).first()
    audio=video.download(output_path=settings.MEDIA_ROOT)
    base,ext=os.path.splitext(audio)
    new_file=base+'.mp3'
    os.rename(audio,new_file)
    return new_file

def get_transcription(link):
    audio_file=get_audio(link)
    aai.settings.api_key = "06b8d0f97d84421b81fde120af29d6bd"
    transcriber=aai.transcriber()
    transcript=transcriber.transcribe(audio_file)
    return transcript.text