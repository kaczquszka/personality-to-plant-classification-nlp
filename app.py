import streamlit as st
import torch
import wikipediaapi
import wikipedia
from transformers import pipeline
import pandas as pd
import pickle
import re
import random
import time

if 'sentiment' not in st.session_state:
    st.session_state.sentiment = {
    'Growth':None,
    'Soil':None,
    'Sunlight':None,
    'Watering':None,
    'Fertilization Type':None
}

if 'page' not in st.session_state:
    st.session_state.page = None

if 'step' not in st.session_state:
    st.session_state.step = 1

if 'info' not in st.session_state:
    st.session_state.info = {
    'Growth':None,
    'Soil':None,
    'Sunlight':None,
    'Watering':None,
    'Fertilization Type':None
}
    
if 'plant' not in st.session_state:
    st.session_state.plant = None     

if 'question_number' not in st.session_state:
    st.session_state.question_number = {
    'Growth':None,
    'Soil':None,
    'Sunlight':None,
    'Watering':None,
    'Fertilization Type':None
}  

Questions = {
    "Growth": [
        "Would you consider yourself a fast learner? Why?",
        "How eager are you to learn new technologies?",
        "Do you have difficulties acquiring new knowledge? If so, why?",
        "How would you feel in a situation where you have to learn a new skill in a short time?"
    ],
    "Soil": [
        "Is it easy for you to make new friends?",
        "How do you feel in situations where you have to talk to new people?",
        "How do you feel when you have to make a phone call to a person you haven't talked to yet?",
        "How would you describe your attitude toward laws and regulations? Do you always follow them, no matter what?",
        "Do you consider yourself the life of the party?"
    ],
    "Sunlight": [
        "How do you feel about hot summer days?",
        "Would you be happy spending a month in the tropics?",
        "Do you prefer hot weather over cold weather?",
        "How do you feel during summer when it comes to temperatures?"
    ],
    "Watering": [
        "How do you feel about water sports?",
        "Do sea cruises sound like a fun activity to you?",
        "How do you feel about swimming in the warm Mediterranean Sea?",
        "Do you enjoy swimming in pools or any natural bodies of water?",
        "When you are on vacation, do you use pools or go swimming if possible?"
    ],
    "Fertilization Type": [
        "Do you consider your diet healthy and good for you?",
        "How do you feel about bio products?",
        "Do you take care of your health?",
        "Can you imagine your life without any fast-food meals?"
    ]
}


def rerun_quiz():
    st.session_state.step=1 


def calculate_result(res_dict):
  copy = res_dict.copy() #zeby nie nadpisywac
  multiplier = {
      'neutral': 0,
      'negative': -1,
      'positive': 1
  }
  sentiment_value =[]
  key_sentiment_dict = list(st.session_state.sentiment.keys())
  x = 0
  for results in copy:
    for key in results:
      results[key] = results[key] * multiplier[key]
    sentiment_value.append(sum(results.values()))
    st.session_state.sentiment[key_sentiment_dict[x]] = sum(results.values())
    x = x+1


  
  return sentiment_value
@st.cache_resource
def load_pipeline():
    return pipeline("text-classification", model="kaczquszka/fine-tuned-on-2000-answers-distilbert-base-uncased", top_k=3)

def getPrediction():
    pipe = load_pipeline()
    # ... rest of your code
def getPrediction():
    pipe = load_pipeline()
    result = pipe([item for item in st.session_state.info.values()])
    res_dict = [{item['label']: item['score'] for item in item_list} for item_list in result]
    results = calculate_result(res_dict)
    with open('content/knn_classifier.svn', 'rb') as f:
        classifier = pickle.load(f)
    return(classifier.predict([results])[0])
    
def findPage():

    query = st.session_state.plant + ' plant'
    page_name = wikipedia.search(query,1)
    wiki = wikipediaapi.Wikipedia('plant-character-classification 1.0', language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
    return wiki.page(page_name[0])


def printResults(image_title,image_url):
    left, mid ,right = st.columns([1,3,1])
    with mid:
        st.image(image_title,image_url)
    st.markdown("#### :violet[Why such result? :thinking:]")
    st.markdown("The questions you answered were mapped to specific traits of plants. " \
    "\n\nYour answers were then anaylized using fine tuned distilBert model on sentiment analysis. " \
    "\n\nThen, based on results obtained from the model, a simple k nearest neighbours classification was used to assign the most suitable plant to your character")
    st.divider()
    st.markdown('#### :violet[Still not satisfied? See for yourself then..]')
    df = pd.read_csv('datasets/plants_unique.csv', encoding = "latin1")
    # st.write(df[df['Plant Name']==st.session_state.plant].iloc[:,:6]) 
    results = pd.DataFrame(columns=['Category','Question','Your Answer', 'Sentiment assigned', 'Obtained trait'])

    for category in df.columns[1:]:
        results.loc[len(results)]=[category,f'{Questions[category][st.session_state.question_number[category]]}', f'{st.session_state.info[category]}',f'{st.session_state.sentiment[category]:.4f}',f'{df[df['Plant Name']==st.session_state.plant][category].values[0]}']
    
    st.dataframe(results, hide_index=True)
    st.divider()
    
def getPhotoAndSummary():
    plants_links = pd.read_csv("datasets/plants_links.csv")
    wiki = wikipediaapi.Wikipedia('plant-character-classification 1.0', language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
    print(st.session_state.plant)
    st.session_state.page = wiki.page( plants_links.loc[plants_links['Names']==st.session_state.plant, 'Page Title'].values[0])

    html_text = st.session_state.page.summary
    source_text = st.session_state.page.fullurl
    image_url = plants_links.loc[plants_links['Names']==st.session_state.plant, 'Links'].values[0]
    media_type = image_url.rsplit(".",1)[-1].lower()
    title = re.sub('\s','_', st.session_state.plant)
    image_title= f"content/{title}.{media_type}"
    return html_text,source_text, image_title, image_url


def init_quesions():
    for name in st.session_state.question_number:
        n = random.randint(0,(len(Questions[name])-1))
        st.session_state.question_number[name] = n


if st.session_state.step == 1:
    st.title('What is your inner plant? 🪴🍄')
    st.markdown('Answer the questions and find out!')
    st.divider()

    form_placeholder = st.empty()
    with form_placeholder.form("quiz_answers"):
        
        if st.session_state.question_number['Growth'] == None:
            init_quesions()
        for name in st.session_state.info.keys():
            st.session_state.info[name] = st.text_input(Questions[name][st.session_state.question_number[name]])
            print(st.session_state.info[name])
        submit_button = st.form_submit_button(label ="Submit")

    if submit_button:
        if not all(st.session_state.info.values()):
            st.warning('fill all of the fileds, please :)')
        else:
            st.session_state.step=2
            form_placeholder.empty()
            st.rerun()        
        
elif st.session_state.step == 2:  
    # left, mid ,right = st.columns([1,3,1])
    # with mid:
    #     st.image('content/loading.gif')
    #     st.write("https://www.pinterest.com/ideas/loading-gif/948421891026/")
    st.session_state.plant = getPrediction()
    st.session_state.page = findPage()
    st.session_state.step = 3
    # time.sleep(3)
    st.rerun()

elif st.session_state.step == 3: 
    html_text,source_text ,image_title,image_url = getPhotoAndSummary()
    if(st.session_state.page.exists()):
        st.markdown(f"# Your inner plant is :rainbow[{st.session_state.plant}]!")
        st.divider()
        printResults(image_title,image_url)
        st.markdown(f'#### :violet[Learn more about :rainbow[{st.session_state.plant}]!]')
        st.html(html_text)
        st.write('Source: ', source_text)
    st.button('rerun', on_click=rerun_quiz)


