
import requests
import wave
from api import api_key
import sys

## commomn 

base_url = "https://api.assemblyai.com/v2"

file_name = sys.argv[1]

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



def transcribe(upload_url):

    data = {"audio_url": upload_url }

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
        
    return transcription_result

## Saving script

upload_url=upload(file_name)

transcript_id=transcribe(upload_url)

transcription_result=polling(transcript_id)



with open("result.txt","w") as f:
  f.write(transcription_result["text"])

print("saved")
