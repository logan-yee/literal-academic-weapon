import pyttsx3

def speak(text, rate=120, volume=1.0):
    """Convert text to speech with adjustable rate and volume."""
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)  # Adjust speed
    engine.setProperty("volume", volume)  # Adjust volume (0.0 to 1.0)

    # Set the voice (optional)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)  # Use first available voice

    # Queue the message
    engine.say(text)

    # Process and execute the speech
    engine.runAndWait()
