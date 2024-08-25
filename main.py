import speech_recognition as sr
import pyttsx3
import webbrowser
import musicLib
import requests
import nltk
from nltk.chat.util import Chat, reflections
from youtubesearchpython import VideosSearch
from googlesearch import search

recognizer = sr.Recognizer()
engine = pyttsx3.init()
microphone = sr.Microphone()
newsAPI = "6ff2882ba17d42229e809add5c68a6de"
nltk.download('punkt', quiet=True)

patterns = [
    (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
    (r'how are you', ['I am doing well, thank you!', 'I am fine, how about you?']),
    (r'what is your name', ['My name is Alfred, your AI assistant.']),
    (r'bye|goodbye', ['Goodbye!', 'See you later!', 'Bye!']),
    (r'(.*)', ['I am not sure how to respond to that.', 'Can you please rephrase that?', 'Interesting, tell me more.']),
     (r'what is the capital of (.*)', ['The capital of %1 is... Actually, I don\'t have access to that information. You might want to look it up online.']),
    (r'who is (.*)', ['I\'m afraid I don\'t have information about specific people. You might want to search for %1 online.']),
    (r'what is (.*)', ['%1 is an interesting topic. Unfortunately, I don\'t have detailed information about that. You might want to research it further.']),
]

chatbot = Chat(patterns, reflections)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def ask_ai(prompt):
    return chatbot.respond(prompt)

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/feed/")
    elif "open youtube" in c.lower(): 
        webbrowser.open("https://www.youtube.com/")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com/")
    elif c.lower().startswith("play"):
        query = c.lower().split(" ", 1)[1]
        videosSearch = VideosSearch(query, limit=1)
        video_result = videosSearch.result()
        video_link = video_result['result'][0]['link']
        webbrowser.open(video_link)
        speak(f"Playing {query} on YouTube.")
    elif c.lower().startswith("search"):
        try:
            query = c.lower().split(" ", 1)[1]
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            speak(f"Searching {query} on Google.")
            webbrowser.open(search_url)
        except IndexError:
            speak("Please provide a search query after 'search'.")

    elif "today's news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsAPI}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])
    else:
        response = ask_ai(c)
        speak(response)

if __name__ == "__main__":
    speak("initializing Alfred...")
    
    while True: 
        print("Listening...")
        try:
            with microphone as source:
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)

            if word.lower() == "alfred":
                speak("Yes sir!")
                with microphone as source:
                    print("Alfred Activated!")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
                            
        except Exception as e:
            print(f"Error: {e}")