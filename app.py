import openai
import pyttsx3
from flask import Flask, render_template, request

openai.api_key = "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"

# Initialize Flask app
app = Flask(__name__)

def text_to_speech(text, gender):
    voice_dict = {'Male': 0, 'Female': 1}
    code = voice_dict[gender]

    engine = pyttsx3.init()

    # Setting up voice rate
    engine.setProperty('rate', 150)

    # Setting up volume level  between 0 and 1
    engine.setProperty('volume', 0.8)

    # Change voices: 0 for male and 1 for female
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[code].id)

    engine.say(text)
    engine.runAndWait()

# Define home page route
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        text = request.form.get("text")
        gender = 'Male'
        text_to_speech(text, gender)
    return render_template("index.html")

@app.route("/summary", methods=['GET', 'POST'])
def summarize():
    text = request.form.get("text")
    summary = generate_summary(text)
    return render_template("summary.html", summary=summary, text = text)

def generate_summary(text):
    prompt = (f"Summarize the following text for a person with dyslexia:\n{text}\n\nSummary:")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    summary = response.choices[0].text.strip()
    return summary

@app.route("/simplify", methods=['GET', 'POST'])
def simplify():
    text = request.form.get("text")
    simplification = generate_simplification(text)
    return render_template("simplify.html", simplification=simplification, text=text)

def generate_simplification(text):
    prompt = (f"Simplify the writing in the given text without summarizing\n{text}\n\nSummary:")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    simplification = response.choices[0].text.strip()
    return simplification

@app.route("/bullets", methods=["GET", "POST"])
def bullets():
        # Retrieve user input from form
    text = request.form["text"]

        # Set up OpenAI API parameters
    prompt = f"Condense the following text into 6 or less bullet points:\n{text}\n\n*"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    bullets = response.choices[0].text

    print(bullets)
    bullets_array =[]
    bullets_arr1 = bullets.split("*")
    for bullet in bullets_arr1:
        bullets_array.append(bullet.strip()) 
    print(bullets_array)

    return render_template("bullets.html", bullets=bullets_array, text=text)

def generate_headings(text):
    # set GPT-3 parameters
    model_engine = "text-davinci-003"
    prompt = (f"Split the text into paragraphs and give each paragraph a heading\n{text}\nText with Headings:")
    max_tokens = 2000
    
    # generate summary with GPT-3
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        n = 1,
        stop=None,
        temperature=0.5,
    )
    headings = response.choices[0].text.strip()
    return headings

@app.route('/headings', methods=['GET', 'POST'])
def headings_text():
    text = request.form.get("text")
    headings = generate_headings(text)
    heading_array = []
    for text in headings.split("\n\n"):
        heading = text.split(":")[0]
        para = text.split(":")[1]
        heading_array.append({"headings": heading.strip(), "para": para.strip()})
    print(heading_array)
    return render_template("headings.html", headings=heading_array, text=text)

# Define flashcards page route
@app.route("/flashcards", methods=['GET', 'POST'])
def flashcards():
    text = request.form["text"]
    print(text)

    # Use OpenAI API to generate flashcards
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Break down the given piece of text into flashcards in a question-answer form\n\n{text}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    flashcards = response.choices[0].text.strip()

 #   print(flashcards)
    # Convert flashcards to a list of objects
    cards = []
    for card in flashcards.split("\n\n"):
        if "Q: " in card and "A: " in card:
            question = card.split("Q: ")[1]
            question = card.split("A: ")[0]
            answer = card.split("A: ")[1]
            cards.append({"question": question.strip(), "answer": answer.strip()})

    # Render flashcards page with data
    return render_template("flashcards.html", data=cards)

if __name__ == "__main__":
    app.run(debug=True)

