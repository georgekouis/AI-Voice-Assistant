from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import nltk

nltk.download('omw-1.4')

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate',150) #Taxutita fonis tou AI

order_pizza = {'Pepperoni Pizza', 'Italian Pizza', 'Barbeque Pizza'}


def pizza_flavor():
    global recognizer

    speaker.say("Do you want to see what pizzas we have?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("Please choose a pizza")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                eidos_pizzas = recognizer.recognize_google(audio)
                eidos_pizzas = eidos_pizzas.lower()

            with open(eidos_pizzas, 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"I wrote down the pizza {eidos_pizzas}")    
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I didn't understand you! Please try again!")
            speaker.runAndWait()


def extra_ingredients():

    global recognizer

    speaker.say("Do you want something extra?")
    speaker.runAndWait()

    done = False 

    while not done:
        try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()    

                order_pizza.append(item)
                done = True

                speaker.say(f"We will add at your {item} your extra ingredients!") 
                speaker.runAndWait()

        except speech_recognition.UnboundLocalError:
                recognizer = speech_recognition.Recognizer()
                speaker.say("I didn't understand you.")  
                speaker.runAndWait() 

def show_pizza():

    speaker.say("The pizza that you picked is the following.")
    for item in order_pizza:
        speaker.say(item)
    speaker.runAndWait()

def hello():
    speaker.say("Hello, how can I help you today?")
    speaker.runAndWait() 

def quit():
    speaker.say("Bye")
    speaker.runAndWait()  
    sys.exit(0)


mappings = {
    "greeting": hello, 
    "order_pizza": pizza_flavor,
    "extra_ingredients": extra_ingredients,
    "show_pizza": show_pizza,
    "quit": exit
}                                          
    

assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

while True:

    try:
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

        assistant.request(message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()       