import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set the speech rate (optional)
engine.setProperty("rate", 150)  # Adjust speed (default is ~200 words per minute)

# Set the voice (optional)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # Use first available voice

# Queue the message
engine.say("You have been caught procrastinating, please look at the schedule your AI assistant to make you a literal academic weapon.")

# Process and execute the speech
engine.runAndWait()
