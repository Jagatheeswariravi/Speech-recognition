import requests
import wave
import json
from senti import get_audio_url,get_video_infos
from api import api_key,pod_api_key
import sys
import time
from listennotes import podcast_api
import pprint


## commomn 

base_url = "https://api.assemblyai.com/v2"

pod_endpoint =  'https://listen-api.listennotes.com/api/v2'

headers = {"authorization": api_key}

pod_headers = {"authorization": pod_api_key}


def get_epi_audio_url(episode_id):
    client = podcast_api.Client(api_key=pod_api_key)
    response = client.fetch_episode_by_id(
     id=episode_id,
    show_transcript=1,
    )
    data=response.json()

    audio_url = data["audio"]
    thumbnail = data["thumbnail"]
    title = data["title"]

    return audio_url,thumbnail,title

## transcribe



def transcribe(audio_url,auto_chapters):

    data = {"audio_url": audio_url,
            "auto_chapters":  auto_chapters}

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

def save_transcript(episode_id):

    audio_url,thumbnail,title=get_epi_audio_url(episode_id)
    
    transcript_id=transcribe(audio_url,auto_chapters=True)

    transcription_result=polling(transcript_id)

    pprint.pprint(transcription_result)

    filename = episode_id +".txt"

    with open(filename,"w") as f:
        f.write(transcription_result["text"])
    
    chapter_filename = episode_id +".json"

    with open(chapter_filename, 'w') as f:
        chapters = transcription_result['chapters']

        ep_data = {'chapters': chapters}
        ep_data['audio_url']=audio_url
        ep_data['thumbnail']=thumbnail
        ep_data['episode_title']=title
           

        json.dump(ep_data, f, indent=4)
        print('Transcript saved')
        return True




def save_video_sentiments(url):
    video_info = get_video_infos(url)
    audio_url= get_audio_url(video_info)
    title = video_info["title"]
    title = title.strip().replace(" ","_")
    
    save_transcript(audio_url,title,sentiment_analysis=True)



if __name__ == "__main__":
    save_video_sentiments("https://www.youtube.com/watch?v=vNxyOhyPGEs&t=169s")

    


