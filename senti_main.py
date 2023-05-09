import requests
import wave
import json
from senti import get_audio_url,get_video_infos
from api import api_key
import sys
import time

## commomn 

base_url = "https://api.assemblyai.com/v2"

#file_name = sys.argv[1]

headers = {"authorization": api_key}

## upload
def upload(file_name):

    with open(file_name , "rb") as f:
        response = requests.post(base_url + "/upload",
                            headers=headers,
                            data=f)

    upload_url = response.json()["upload_url"]
    
    print("url",upload_url)

    return upload_url





## transcribe



def transcribe(audio_url,sentiment_analysis):

    data = {"audio_url": audio_url,
            "sentiment_analysis": sentiment_analysis }

    url = base_url + "/transcript"
    response = requests.post(url, json=data, headers=headers)

    transcript_id = response.json()["id"]

    print(transcript_id)

    return transcript_id

## polling

def polling(transcript_id):

    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

    while True:
        transcription_result = requests.get(polling_endpoint, headers=headers).json()

        if transcription_result['status'] == 'completed':
            print("done")
            break

        elif transcription_result['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")
            print("error")
        
        print("transcripting")
        time.sleep(60)
        
        
        
    return transcription_result

## Saving script

def save_transcript(audio_url,title,sentiment_analysis=False):

    #upload_url=upload(file_name)

    transcript_id=transcribe(audio_url,sentiment_analysis)

    transcription_result=polling(transcript_id)

    filename = title+".txt"

    with open(filename,"w") as f:
        f.write(transcription_result["text"])
    if sentiment_analysis:
        filename = title+".json"
        with open(filename,"w") as f:
             sentiments = transcription_result["sentiment_ananlysis_results"]
             json.dump(sentiments,filename,indent=4)

            
    print("saved")





def save_video_sentiments(url):
    video_info = get_video_infos(url)
    audio_url= get_audio_url(video_info)
    title = video_info["title"]
    title = title.strip().replace(" ","_")
    
    save_transcript(audio_url,title,sentiment_analysis=True)



if __name__ == "__main__":
    save_video_sentiments("https://www.youtube.com/watch?v=vNxyOhyPGEs&t=169s")

    


