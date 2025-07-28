import requests
import tkinter as tk
import pyttsx3
import speech_recognition as sr
import threading
from datetime import datetime
import os

def get_weather():
    city = city_entry.get()
    api_key = "35b99b622b8f22ce01d723b5f4390fd4"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        name = data['name']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        pressure = data['main']['pressure']

        voice_text = f"Temperature in {name} is {int(temp)} degrees. Humidity is {int(humidity)} percent."
        display_text = (
            f"City: {name}\n"
            f"Temperature: {temp} °C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind} m/s\n"
            f"Pressure: {pressure} hPa"
        )

        threading.Thread(target=speak, args=(voice_text,)).start()
        animate_text(display_text)
        save_to_log(name, temp, humidity, wind, pressure)
    else:
        animate_text("City not found. Please try again.")

def animate_text(text):
    result_label.config(text="")
    def update(i=0):
        if i < len(text):
            current = result_label.cget("text")
            result_label.config(text=current + text[i])
            r.after(18, lambda: update(i + 1))
    update()

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.id.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 190)
    engine.say(text)
    engine.runAndWait()

def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        result_label.config(text="Listening...")
        r.update()
        try:
            audio = recognizer.listen(source, timeout=5)
            city = recognizer.recognize_google(audio)
            city_entry.delete(0, tk.END)
            city_entry.insert(0, city)
            get_weather()
        except:
            animate_text("Sorry, could not recognize speech.")

# Save log file in same folder as this script
def save_to_log(city, temp, humidity, wind, pressure):
    try:
        log_path = os.path.join(os.path.dirname(__file__), "weather_log.txt")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"{now} | {city} | Temp: {temp}°C | Humidity: {humidity}% | Wind: {wind} m/s | Pressure: {pressure} hPa\n"
        with open(log_path, "a", encoding="utf-8") as file:
            file.write(log_line)
        print("Logged:", log_line.strip())
    except Exception as e:
        print("Error writing to file:", e)

def clear_entry(event):
    if city_entry.get() == "Enter city name":
        city_entry.delete(0, tk.END)

def restore_entry(event):
    if city_entry.get() == "":
        city_entry.insert(0, "Enter city name")

# ------------------ GUI ------------------
r = tk.Tk()
r.title("Weather App")
r.geometry("400x500")
r.configure(bg="#e3f2fd")
r.resizable(False, False)

tk.Label(r, text="Weather Forecast", font=("Segoe UI", 20, "bold"), bg="#e3f2fd", fg="#468acf").pack(pady=15)

frame = tk.Frame(r, bg="#e3f2fd")
frame.pack(pady=10)

city_entry = tk.Entry(frame, font=("Segoe UI", 14), width=22, fg="#555", justify="center")
city_entry.insert(0, "Enter city name")
city_entry.bind("<FocusIn>", clear_entry)
city_entry.bind("<FocusOut>", restore_entry)
city_entry.grid(row=0, column=0, padx=(10, 5))

mic_button = tk.Button(frame, text="🎤", font=("Segoe UI", 14), command=recognize_voice,
                       bg="#e3f2fd", bd=0, activebackground="#bbdefb")
mic_button.grid(row=0, column=1)

tk.Button(r, text="Get Weather", font=("Segoe UI", 12, "bold"),
          bg="#468acf", fg="white", activebackground="#1565c0",
          padx=10, pady=5, bd=0, command=get_weather).pack(pady=10)

result_label = tk.Label(r, text="", font=("Segoe UI", 13), bg="#e3f2fd", justify="left", wraplength=360)
result_label.pack(pady=20)

r.bind('<Return>', lambda event: get_weather())

r.mainloop()
