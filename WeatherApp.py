from tkinter import *
import requests
import re

API_KEY = '&units=imperial&appid=e7faebfe494a131c02e0b1fbbadd1b19'
URL = 'http://api.openweathermap.org/data/2.5/weather?'
icon_image = ''
weather_display = False

def getWeather():
    search_type = check_entry()
    user_entry = location_entry.get()
    if search_type == 'zip=':
        error_frame.pack_forget()
        response = requests.get(URL+search_type+user_entry+API_KEY)
        display_response(response)
    elif search_type == 'q=':
        error_frame.pack_forget()
        response = requests.get(URL+search_type+user_entry+API_KEY)
        display_response(response)
    else:
        display_error("Please enter a valid location.")

def display_response(response):

    if response.status_code == 404:
        display_error("Please enter a valid location.")
    elif response.status_code == 200:
        response = response.json()
        weather_frame = Frame(root, bg="#4db8ff")
        description = response['weather'][0]['description']
        temp = response['main']['temp']
        humidity = response['main']['humidity']
        icon_id = response['weather'][0]['icon']

        icon = PhotoImage(file='{}.png'.format(icon_id))
        global icon_image
        icon_image = icon
        global weather_display

        if not weather_display:
            temp_label.config(fg="white", text="Temperature: {}".format(round(temp)), bg="#4db8ff", font=("Serif", 24))
            humidity_label.config(fg="white", text="Humidity: {}".format(round(humidity)), bg="#4db8ff", font=("Serif", 24))
            description_label.config(text=description.capitalize(), fg="white", bg="#4db8ff", font=("Serif", 24))
            icon_label.config(image=icon, bg="#4db8ff")
            temp_label.pack()
            humidity_label.pack()
            description_label.pack()
            icon_label.pack()
            weather_frame.pack()
            weather_display = True
        else:
            temp_label.config(text="Temperature: {}".format(round(temp)))
            humidity_label.config(text="Humidity: {}".format(round(humidity)))
            description_label.config(text=description.capitalize())
            icon_label.config(image=icon)

    else:
        display_error("An unknown error has ocurred. Please try again later.")


def display_error(error):
    error_label.config(text=error)
    error_frame.pack(fill=X)

def check_entry():
    user_entry = location_entry.get()
    if re.match("\d{5}", user_entry) != None and len(user_entry)==5:
        return 'zip='
    elif re.match("\D", user_entry) != None:
        return 'q='
    else:
        return None

root = Tk()

root.config(bg="#4db8ff")
location_frame = Frame(root, bg="#4db8ff")
weather_frame = Frame(root, bg="#4db8ff")
error_frame = Frame(root, bg="red")

greeting_label = Label(root, text="Enter a city or zip code", fg="white", bg="#4db8ff", font=("Serif", 24))
location_entry = Entry(location_frame)
submit_button = Button(location_frame, text="Submit", fg="white", bg="#003d66", command=getWeather)
error_label = Label(error_frame, fg="white", bg="red")

temp_label = Label()
humidity_label = Label()
description_label = Label()
icon_label = Label()

error_label.pack()
greeting_label.pack()
location_frame.pack()
location_entry.grid(row=0, column=0, padx=10, ipadx=50)
submit_button.grid(row=0, column=1)
weather_frame.pack()

root.title("The Weather App")
root.geometry("600x400")
root.mainloop()
