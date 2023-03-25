import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
from config import TOKEN
import fake_useragent

bot = telebot.TeleBot(TOKEN)

user = fake_useragent.UserAgent().random

@bot.message_handler(commands=['start'])
def start(message):
    chatid = message.chat.id
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    weather_today = types.KeyboardButton('Погода сьогодні')
    weather_tomorrow = types.KeyboardButton('Погода завтра')

    markup.add(weather_today, weather_tomorrow)

    bot.send_message(chatid, f'Я надаю інформацію про погоду у Львові. Обери кнопку', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def text(message):
    chatid = message.chat.id
    
    if message.text == 'Погода сьогодні':
        url = 'https://www.accuweather.com/uk/ua/lviv/324561/current-weather/324561'

        headers = {
            'User-Agent': user
        }

        response = requests.get(url, headers=headers)

        bs = BeautifulSoup(response.text, 'html.parser')

        status = bs.find('div', class_ = 'phrase').text
        temp = bs.find('div', class_ = 'display-temp').text
        temp_day = bs.find_all('div', class_ = 'temperature')[0].text
        temp_night = bs.find_all('div', class_ = 'temperature')[1].text
        wind_direction = bs.find_all('div', class_ = 'detail-item spaced-content')[1].text
        wind_speed = bs.find_all('div', class_ = 'detail-item spaced-content')[2].text
        humidity = bs.find_all('div', class_ = 'detail-item spaced-content')[3].text
        pressure = bs.find_all('div', class_ = 'detail-item spaced-content')[5].text
        chance_of_rain = bs.find_all('p', class_ = 'panel-item')[2].text
        sunrise = bs.find_all('span', class_ = 'text-value')[0].text
        sunset = bs.find_all('span', class_ = 'text-value')[1].text


        bot.send_message(chatid,
                         str(temp.strip()) + ' ' + str(status.lower()) + '\n' +
                         'Вдень: ' + str(temp_day.strip().lower().replace('макс', '')) + '/' + 'Вночі: ' + str(temp_night.strip().lower().replace('мін', '')) + '\n' +
                         'Напрямок вітру: ' + str(wind_direction.replace('Вітер', '').strip()) + '\n' +
                         'Пориви вітру: ' + str(wind_speed.replace('Пориви вітру', '').strip()) + '\n' +
                         'Вологість: ' + str(humidity.replace('Вологість', '').strip()) + '\n' +
                         'Тиск: ' + str(pressure.replace('Тиск', '').strip().replace('↔', '').replace('↑', '')) + '\n' +
                         'Ймовірність опадів: ' + str(chance_of_rain.replace('Імовірність опадів', '').strip()) + '\n' +
                         str(sunrise.strip()) + ' схід сонця' + '\n' +
                         str(sunset.strip()) + ' захід сонця'
                        )
    
    elif message.text == 'Погода завтра':
        url = 'https://www.accuweather.com/uk/ua/lviv/324561/daily-weather-forecast/324561?day=2'

        headers = {
            'User-Agent': user
        }

        response = requests.get(url, headers=headers)

        bs = BeautifulSoup(response.text, 'html.parser')

        status1 = bs.find('div', class_ = 'phrase').text
        temp1 = bs.find('div', class_ = 'temperature').text
        temp_nignt1 = bs.find_all('div', class_ = 'temperature')[1].text
        wind_direction1 = bs.find_all('p', class_ = 'panel-item')[1].text
        wind_speed1 = bs.find_all('p', class_ = 'panel-item')[2].text
        chance_of_rain1 = bs.find_all('p', class_ = 'panel-item')[3].text
        sunrise1 = bs.find_all('span', class_ = 'text-value')[0].text
        sunset1 = bs.find_all('span', class_ = 'text-value')[1].text


        bot.send_message(chatid, 
                         str(temp1.strip().replace('Макс', '')) + ' ' + str(status1.lower().strip()) + '\n' +
                         'Вдень: ' + str(temp1.strip().replace('Макс', '')) + '/' + 'Вночі: ' + str(temp_nignt1.strip().replace('Мін', '')) + '\n' +
                         'Напрямок вітру: ' + str(wind_direction1.replace('Вітер', '').strip()) + '\n' +
                         'Пориви вітру: ' + str(wind_speed1.replace('Пориви вітру', '').strip()) + '\n' +
                         'Ймовірність опадів: ' + str(chance_of_rain1.replace('Імовірність опадів', '').strip()) + '\n' +
                         str(sunrise1.strip()) + ' схід сонця' + '\n' +
                         str(sunset1.strip()) + ' захід сонця'
                        )
    
    else:
        bot.send_message(chatid, 'Я не розумію тебе')

bot.polling(none_stop=True)