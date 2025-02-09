# literal-academic-weapon

## Inspiration

Procrastination is a big problem, especially for post-secondary students. We wanted to use AI to help keep students on track, with the model notifying you whenever you're slacking off. 

## What it does

The LLM can detect whenever your screen is displaying something unrelated to your assignments, and will notify you that you're procrastinating. It will also break down your session stats, showing you how much you worked, and conversely how much you procrastinated.

## How we built it

We built the back-end using Python. We utilized a multi-agent system to differentiate related work from procrastination, and had an LLM generate an optimized study schedule for the user. 
- Using Pillow to capture images of the users screen
- InternVL implemented with pytorch to generate image to text outputs
- Ollamas Llama3 model executed with Langchain to classify the text outputs and format it to json
- Mistral model with Ollama and Lanchain to generate an optimized study schedule based on user habits
- pytts3 for a text-to-speech notification
- plyer for a system notification
- FastAPI to link the back end to the front end
- React.js for front end web pages 

## Challenges we ran into

One particularly challenging part of the assignment was to train the model to be accurate enough to output results, without taking so long to train that it'd be infeasible. That was a fine line that we had to negotiate, but our AI model is working at an optimum balance.

## Accomplishments that we're proud of

We're really proud of being able to implement machine learning into our code, as well as tying that to a robust front-end.

## What we learned

We learned much about utilizing machine learning in our code, which will be crucial in the years to come, as AI models grow in relevance and popularity.

## What's next for Literal Academic Weapon

A lot of maintenance and extension; the implementation thus far is pretty barebones. However, in the future, we as a team hope to make it a more generalized and accessible tool, possibly hooking it up to Canvas LMS and scraping assignment info from there to better train the Ollama model.
