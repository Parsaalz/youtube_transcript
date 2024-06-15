from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pytube import YouTube
from django.conf import settings
import os
import assemblyai as aai
import openai as oai
@csrf_exempt
def blog_page(request):
    if request.method=="POST":
        yt_link=request.POST.get('youtubelink')
        print(yt_link)
        title=get_title(yt_link)
        transcription=get_transcription(yt_link)
        if not transcription:
            return JsonResponse({"error":"failed to get transcript"},status=500)
        blog_content=generate_blog(transcription)
        print(blog_content)
        if not blog_content:
            return JsonResponse({"error":"failed to generate"},status=500)
    return render(request,'base.html')


def get_title(link):
    print(1)
    print(link)
    yt=YouTube(link)
    title=yt.title
    print(title)
    return title

def get_audio(link):
    print(2)
    yt=YouTube(link)
    print(2.1)
    video=yt.streams.filter(only_audio=True).first()
    print(2.2)
    audio=video.download(output_path=settings.MEDIA_ROOT)
    print(2.3)
    base,ext=os.path.splitext(audio)
    print(2.4)
    new_file=base+'.mp3'
    print(2.5)
    os.rename(audio,new_file)
    return new_file

def get_transcription(link):
    print(3)
    audio_file=get_audio(link)
    # aai.settings.api_key = ""
    transcriber=aai.transcriber()
    transcript=transcriber.transcribe(audio_file)
    return transcript.text

def generate_blog(transcription):
    print(4)
    # oai.api_key=""

    prompt=f"{transcription}\n\nArticle:"

    response = oai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
    )
    generated_content=response.choices[0].text.strip()
    return generated_content