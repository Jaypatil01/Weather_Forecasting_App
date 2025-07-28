# Weather_Forecasting_App
A fun little weather app made with Python! You can speak the city name, see animated results, hear the weather, and it even logs your searches to a text file.

# Voice-Based Weather App

This is a Python-based weather application with a simple graphical interface. Users can type or speak the name of a city to get real-time weather information, which is both displayed with a typing animation and read aloud using a female voice. Each search is saved to a log file for future reference.

## Features

- Voice input for city names using a microphone
- Text-to-speech weather summary using pyttsx3
- Typing animation for displaying results like subtitles
- Logs each query with a timestamp to `weather_log.txt`
- Simple and clean Tkinter GUI

## Requirements

- Python 3.x  
- Required Python libraries:
  - `requests`
  - `tkinter` (standard with most Python installations)
  - `pyttsx3`
  - `speech_recognition`

To install the required libraries, run:

```bash
pip install requests pyttsx3 SpeechRecognition
