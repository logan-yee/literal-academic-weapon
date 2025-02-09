import pyttsx3

def speak(text, rate=120, volume=1.0):
    """Convert text to speech with adjustable rate and volume."""
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)  # Adjust speed
    engine.setProperty("volume", volume)  # Adjust volume (0.0 to 1.0)

    # Set the voice (optional)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)  # Use first available voice

    engine.say(text)
    engine.runAndWait()

# Call again with different settings
speak("You have been caught procrastinating, please look at the schedule your AI assistant to make you a literal academic weapon.", rate=120, volume=1.25)

