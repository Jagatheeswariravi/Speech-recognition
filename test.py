from podcast import save_transcript
import streamlit as st
import glob
import json

st.title("Welcome to podcast summary")
episode_id = st.sidebar.text_input("Please enter the episode id")
button = st.sidebar.button("Download Episode summary", on_click=save_transcript, args=(episode_id,))


st.sidebar.button("Get summary")



def get_clean_time(start_ms):
    seconds = int((start_ms / 1000) % 60)
    minutes = int((start_ms / (1000 * 60)) % 60)
    hours = int((start_ms / (1000 * 60 * 60)) % 24)
    if hours > 0:
        start_t = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        start_t = f'{minutes:02d}:{seconds:02d}'
        
    return start_t

if button:
    filename = episode_id + '.json'
    print(filename)
    with open(filename, 'r') as f:
        data = json.load(f)

    chapters = data['chapters']
    title = data['episode_title']
    thumbnail = data['thumbnail']
    
    audio = data['audio_url']

    st.header(f"{title}")
    st.image(thumbnail, width=200)
   
    for chp in chapters:
        with st.expander(chp['gist'] + ' - ' + get_clean_time(chp['start'])):
            chp['summary']
    







