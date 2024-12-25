import pyttsx3

def play_sound(current_piece, next_piece):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Change index to select different voices
    engine.setProperty('rate', 100)  # Speed of speech
    engine.setProperty('volume', 11)  # Volume from 0.0 to 1.0
    sentence = f"Move {current_piece} to {next_piece}"
    engine.say(sentence)
    engine.runAndWait()
    
play_sound("A fifteen", "B fourteen")