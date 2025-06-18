import streamlit as st
import pickle
import pandas as pd
import numpy as np
import lzma
import time
import random

# Load data
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

with lzma.open("similarity1.pkl.xz", "rb") as f:
    similarity = pickle.load(f)

similarity = np.array(similarity)

st.set_page_config(page_title="Movie Recommender", page_icon="🍿", layout="wide")

# 🌈 Theme selector
theme = st.selectbox("🎨 Choose a theme", ["🌞 Light", "🌙 Dark", "🎃 Halloween", "❄️ Winter", "💘 Valentine"])

# Theme styles
theme_styles = {
    "🌞 Light": {
        "bg": "linear-gradient(to right, #fefcea, #f1da36)",
        "text": "#1f1f1f",
        "bubble_bg": "#ffffff88",
        "emoji": "🌞",
        "font": "Quicksand",
        "font_size": "18px",
        "cursor": "url('https://github.com/merlynmartis/movie_cursor_images/blob/main/light.png?raw=true'), auto",
        "greeting": " Hey there, sunshine! Ready for some feel-good flicks?",
        "fallback": "sans-serif"
    },
    "🌙 Dark": {
        "bg": "linear-gradient(to right, #232526, #414345)",
        "text": "#f1f1f1",
        "bubble_bg": "#33333388",
        "emoji": "🌙",
        "font": "Rubik",
        "font_size": "17px",
        "cursor": "url('https://github.com/merlynmartis/movie_cursor_images/blob/main/dark.png?raw=true'), auto",
        "greeting": "🌌 Enter the night... and discover cinematic gems.",
        "fallback": "sans-serif"
    },
    "🎃 Halloween": {
        "bg": "linear-gradient(to right, #4b2c20, #ff7518)",
        "text": "#ffefd5",
        "bubble_bg": "#00000055",
        "emoji": "🎃",
        "font": "Creepster",
        "font_size": "20px",
        "cursor": "url('https://github.com/merlynmartis/movie_cursor_images/blob/main/halloween.png?raw=true'), auto",
        "greeting": " Welcome, mortal! Dare to watch something spooky?",
        "fallback": "cursive"
    },
    "❄️ Winter": {
        "bg": "linear-gradient(to right, #a1c4fd, #c2e9fb)",
        "text": "#001f3f",
        "bubble_bg": "#ffffff99",
        "emoji": "❄️",
        "font": "Montserrat",
        "font_size": "17px",
        "cursor": "url('https://github.com/merlynmartis/movie_cursor_images/blob/main/winter.png?raw=true'), auto",
        "greeting": " Welcome to the cozy side of cinema!",
        "fallback": "sans-serif"
    },
    "💘 Valentine": {
        "bg": "linear-gradient(to right, #ff9a9e, #fad0c4)",
        "text": "#800040",
        "bubble_bg": "#fff0f5bb",
        "emoji": "💘",
        "font": "Dancing Script",
        "font_size": "19px",
        "cursor": "url('https://github.com/merlynmartis/movie_cursor_images/blob/main/valentine.png?raw=true'), auto",
        "greeting": " Ready to fall in love with a movie?",
        "fallback": "cursive"
    }
}

style = theme_styles[theme]

# 🎈 Floating emojis per theme
animations = {
    "🎃 Halloween": "fall"
}

animation_name = animations.get(theme, "")
custom_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family={style['font'].replace(" ", "+")}&display=swap');

* {{
    font-family: '{style['font']}', sans-serif !important;
}}

html, body, .stApp {{
    font-family: '{style['font']}', sans-serif !important;
    font-size: {style['font_size']};
    background: {style['bg']};
    color: {style['text']};
    cursor: {style['cursor']};
}}

.chat-bubble {{
    background: {style['bubble_bg']};
    padding: 15px 20px;
    margin: 10px 0;
    border-radius: 20px;
    font-size: 1.1em;
    width: fit-content;
    max-width: 90%;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}

.user-bubble {{
    align-self: flex-end;
    font-weight: bold;
    color: {style['text']};
    border: 2px solid #ffffff33;
    margin-left: auto;
}}

.bot-bubble {{
    color: {style['text']};
    border: 1px solid #ffffff44;
    margin-right: auto;
}}

.recommend-box {{
    display: inline-block;
    background: #ffffff33;
    color: {style['text']};
    padding: 12px 18px;
    border-radius: 15px;
    margin: 10px 10px 10px 0;
    font-weight: 600;
    box-shadow: 2px 4px 12px rgba(0,0,0,0.1);
}}

.recommend-box:hover {{
    transform: scale(1.05);
    cursor: pointer;
    background-color: #ffffff55;
}}

.message-container {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    animation: fadeIn 0.8s ease-in-out;
}}

@keyframes fadeIn {{
    from {{opacity: 0; transform: translateY(10px);}}
    to {{opacity: 1; transform: translateY(0);}}
}}

@keyframes dropConfetti {{
    0% {{ transform: translateY(0); }}
    100% {{ transform: translateY(100vh); }}
}}

@keyframes floatStars {{
    0% {{ transform: translateY(0); }}
    100% {{ transform: translateY(100vh); }}
}}

@keyframes fall {{
    0% {{ transform: translateY(0) rotate(0deg); }}
    100% {{ transform: translateY(100vh) rotate(360deg); }}
}}

@keyframes snow {{
    0% {{ transform: translateY(0); }}
    100% {{ transform: translateY(100vh); }}
}}

@keyframes floatHeart {{
    0% {{ transform: translateY(0) scale(1); }}
    50% {{ transform: translateY(50vh) scale(1.2); }}
    100% {{ transform: translateY(100vh) scale(1); }}
}}

.emoji-float {{
    position: fixed;
    top: -40px;
    font-size: 28px;
    animation: {animation_name} 7s linear infinite;
    pointer-events: none;
    z-index: 9999;
}}
</style>
"""


st.markdown(custom_css, unsafe_allow_html=True)

# 🎉 Add floating emojis
emoji_map = {
    "🌞 Light": "🎉",
    "🌙 Dark": "🌟",
    "🎃 Halloween": "🦇",
    "❄️ Winter": "❄️",
    "💘 Valentine": "💖"
}
emoji = emoji_map.get(theme)

if emoji:
    floats = ""
    for i in range(15):
        left = random.randint(0, 95)
        delay = random.uniform(0, 5)
        floats += f"<div class='emoji-float' style='left:{left}vw; animation-delay:{delay:.2f}s'>{emoji}</div>"
    st.markdown(f"<div>{floats}</div>", unsafe_allow_html=True)

# 🏷️ Title & Greeting
st.markdown(f"<h1 style='text-align:center;'>{style['emoji']} Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align:center; font-weight:400;'>{style['greeting']}</h3>", unsafe_allow_html=True)

# 🎭 Movie Selection
movie_list = movies['title'].values
selected_movie = st.selectbox("🎭 Pick a movie you like:", movie_list)

# 🔍 Recommendation Logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movie_indices]

# 💬 Chat-style Recommendations
if st.button("💬 Recommend Some Movies!"):
    recommendations = recommend(selected_movie)

    with st.container():
        st.markdown(f"<div class='message-container'><div class='chat-bubble user-bubble'>🎬 I really liked <strong>{selected_movie}</strong>. Got any cool suggestions?</div></div>", unsafe_allow_html=True)
        time.sleep(1)

        st.markdown(f"<div class='message-container'><div class='chat-bubble bot-bubble'>🤖 Ohh, nice pick! Give me a sec... thinking... 🎞️</div></div>", unsafe_allow_html=True)
        time.sleep(1.2)

        st.markdown(f"<div class='message-container'><div class='chat-bubble bot-bubble'>✨ Alright! Based on <strong>{selected_movie}</strong>, you might love these:</div></div>", unsafe_allow_html=True)

        box_html = "<div style='margin-top:10px;'>"
        for movie in recommendations:
            box_html += f"<div class='recommend-box'>🎥 {movie}</div>"
        box_html += "</div>"
        st.markdown(box_html, unsafe_allow_html=True)

        time.sleep(0.5)
        st.markdown(f"<div class='message-container'><div class='chat-bubble bot-bubble'>🍿 Want more recs? Just pick another movie! I’ve got plenty. 😎</div></div>", unsafe_allow_html=True)

# 🤖 Mini Chatbot
st.markdown("### 🤖 Ask the Movie Bot Something")
user_query = st.text_input("💬 Type your question here...")

def mini_chatbot_response(query):
    query = query.lower()
    if "scary" in query or "horror" in query:
        return "👻 If you're brave enough, check out *Hereditary*, *The Conjuring*, or *Get Out*! 🎃"
    elif "under 90" in query or "short" in query:
        return "⏱️ Sure! *Toy Story*, *Run Lola Run*, and *My Neighbor Totoro* are awesome and short!"
    elif "comedy" in query or "funny" in query:
        return "You might love *Superbad*, *The Grand Budapest Hotel*, or *Bridesmaids*!"
    elif "sad" in query or "cry" in query:
        return "😭 Bring tissues for *The Pursuit of Happyness*, *Atonement*, or *Hachi*."
    elif "feel good" in query:
        return "😊 Try *Amélie*, *Paddington 2*, or *The Secret Life of Walter Mitty* – all warm and fuzzy!"
    elif "animated" in query:
        return "🎨 *Coco*, *Zootopia*, and *Spider-Man: Into the Spider-Verse* are top-tier animated picks!"
    elif "action" in query:
        return "💥 Action fans might enjoy *Mad Max: Fury Road*, *John Wick*, or *Gladiator*!"
    elif "romantic" in query or "romance" in query:
        return "❤️ Here are some romantic movies *The Notebook*, *You've Got Mail,*, or *Love Actually*!"
    elif "thriller" in query:
        return "💥 Here are some thriller movies *Shutter Island*, *Gone Girl,*, or *Memento*!"
    elif query.strip() == "":
        return None
    else:
        return "🤔 Hmm, I’m still learning. Try asking for a genre or mood like 'scary', 'animated', or 'short movies'!"

response = mini_chatbot_response(user_query)

if response:
    time.sleep(0.5)
    st.markdown(f"<div class='message-container'><div class='chat-bubble user-bubble'>{user_query}</div></div>", unsafe_allow_html=True)
    time.sleep(0.8)
    st.markdown(f"<div class='message-container'><div class='chat-bubble bot-bubble'>{response}</div></div>", unsafe_allow_html=True)
