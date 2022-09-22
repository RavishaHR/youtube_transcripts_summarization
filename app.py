from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
import json
from urllib.parse import parse_qs, urlparse
from transformers import pipeline
from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


app = Flask(__name__)
CORS(app)

@app.route('/')
def index_page():
    return "Hello world"

@app.route('/time', methods=['GET'])
def get_time():
    return str(datetime.now())

@app.route('/hello')
def welcome_message():
    name = request.args.get('name', '')
    return f'Welcome {name}'


###################################################################################

@app.route('/api/summarize', methods=['GET'])
def get_transcripts():
    #Example:https://www.youtube.com/watch?v=Mus_vwhTCq0
    yt_url = request.args.get('youtube_url', '')
    yt_id = get_youtube_id(yt_url)[2:]
    transcripts = handle_transcript(yt_id) #change

   
    #Summarize
    summary = do_NLP(transcripts) #change
    #print(summary)

    #Return with HTTP Status OK and handle HTTP exceptions
    #return ("ugh")
    return str(summary) 



def handle_transcript(youtubeid):
    list_of_dictionaries = YouTubeTranscriptApi.get_transcript(youtubeid)
    sentence = []
    for transcript in list_of_dictionaries:
        #print(transcript['text'])
        sentence.append(transcript['text'])
    return ' '.join(map(str,sentence))


def get_youtube_id(url):
    q = urlparse(url).query
    return q


#Function for NLP
#accept YouTube transcript as an input parameter and return summarized transcript as output
def do_NLP(transcripts):

    
    # using pipeline API for summarization task
    #summarization = pipeline("summarization")
    #summary_text = summarization(transcripts)[0]['summary_text']



    # # initialize the model architecture and weights
    # model = T5ForConditionalGeneration.from_pretrained("t5-base")
    # # initialize the model tokenizer
    # tokenizer = T5Tokenizer.from_pretrained("t5-base")
    # inputs = tokenizer.encode("summarize: " + transcripts, return_tensors="pt", max_length=512, truncation=True)
    # # generate the summarization output
    # outputs = model.generate(
    #     inputs, 
    #     max_length=150, 
    #     min_length=40, 
    #     length_penalty=2.0, 
    #     num_beams=4, 
    #     early_stopping=True)

    # # just for debugging
    # print(outputs)
    # summary_text = tokenizer.decode(outputs[0])
    # print(summary_text)



    model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
    tokenizer = AutoTokenizer.from_pretrained("t5-base")
    inputs = tokenizer("summarize: " + transcripts, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(
        inputs["input_ids"], max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True
    )
    summary_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(summary_text)


    return summary_text


if __name__ == '__main__':
    app.run(debug=True)


