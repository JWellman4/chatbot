import random
from datetime import datetime, timedelta
import streamlit as st
import yfinance as yf
import requests

st.set_page_config(
    layout='wide',
    page_title='Wellman ChatBot App',
    page_icon='🤖',
)

api_key = '79b962a1124522a8d5a249642ae69e69'
state_code = "Enter State Code:"

def get_current_day():
    return datetime.now().strftime("%A, %b %d, %Y")

def get_current_time():
    return datetime.now().strftime("%#I:%M %p")

def tomorrows_day():
    return (datetime.now() + timedelta(days=1)).strftime("%A, %b %d, %Y")

def get_num_days():
    return int(st.number_input("Enter the number of days from today:", min_value=1, step=1))

def get_future_date(num_days):
    current_date = datetime.now()
    future_date = current_date + timedelta(days=num_days)
    return future_date.strftime("%A, %b %d, %Y")

def get_stock():
    return st.text_input("Enter the ticker symbol:")

def get_stock_value(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    stock_data = stock.history(period="1d")
    if len(stock_data) == 0:
        return " Invalid stock symbol"
    current_value = stock_data["Close"].iloc[-1]
    formatted_value = "${:,.2f}".format(current_value)
    return formatted_value

def get_weather_location():
    return st.text_input("Enter City, State Code/Country Code:", value='Raleigh, NC')

def get_weather_value(weather_location):
    loc_data = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={weather_location}, {state_code}&appid={api_key}')
    if loc_data.status_code != 200:
        return "Error: Unable to retrieve weather data."

    location_info = loc_data.json()
    if len(location_info) == 0:
        return "Error: Location not found."

    lat = location_info[0]['lat']
    lon = location_info[0]['lon']
    weather_data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={api_key}')
    if weather_data.status_code != 200:
        return "Error: Unable to retrieve weather data."

    temp = round(weather_data.json()['main']['temp'])
    desc = weather_data.json()['weather'][0]['description']
    return f"The weather in {weather_location} is {temp}°F with {desc}."

# Define responses
responses = {
    "hi": ["Hello!", "Hi there!", "Hey!"],
    "what day is it?": ["Today is " + get_current_day()],
    "what is tomorrow's date?": ["Tomorrow is " + tomorrows_day()],   
    "what time is it now?": ["The time is " + get_current_time()],
    "what is the stock value?": ["Enter the ticker symbol"],
    "tell me the weather": ["Enter the location"],
    "where are you going this weekend?": ["Robot Land in Seoul, South Korea", "Robot Restaurant in Toyko, Japan"],
    "how are you": ["I'm doing well, thank you!", "I'm great, thanks for asking!", "I'm fine, how about you?"],
    "bye": ["Goodbye!", "See you later!", "Bye! Have a great day!"],
    "tell me the future date?": ["Enter the number of days"],
    "tell me a joke": ["Why was the robot so bad at soccer? Because it kept rebooting the ball.", "What’s a robot’s favorite type of music? Heavy metal.",\
                       "How do robots eat guacamole? With micro-chips.", "Why was the robot feeling cold? It left its Windows open."]
}

def chat(user_input):
    if user_input == 'bye':
        return random.choice(responses["bye"])
    elif user_input == 'tell me the future date?':
        num_days = get_num_days()
        return "Future date is " + get_future_date(num_days)
    elif user_input.lower() == 'what is the stock value?': 
        stock_symbol = get_stock()
        return "The latest closing stock value of " + str(stock_symbol) + " is " + str(get_stock_value(stock_symbol)) 
    elif user_input.lower() == 'tell me the weather':
        weather_location = get_weather_location()
        return get_weather_value(weather_location)
    elif user_input in responses:
        return random.choice(responses[user_input])
    else:
        return "I'm sorry, I don't understand that."


col1, col2 = st.columns(2, gap='large')
with col1: 
    st.title('Wellman Chatbot')
    st.write('Hi! I\'m DUB Bot. You can start chatting with me. Type "bye" to end the conversation.')
    user_input = st.text_input("You:")
    if user_input:
        bot_response = chat(user_input.lower())
        st.write('🤖 DUB Bot:', bot_response)

with col2: 
    st.image('C:/Users/jonat/OneDrive/Desktop/chatbot-removebg-preview.png', width=400)