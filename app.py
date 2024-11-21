from flask import Flask, render_template, request
import pyttsx3
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', message=None, greeting=None, name=None, class_section=None, roll_number=None)


@app.route('/speak_details', methods=['POST'])
def speak_details():
    name = request.form['name']
    class_section = request.form['class_section']
    roll_number = request.form['roll_number']

    # Check if all required fields are filled
    if not name or not class_section or not roll_number:
        return render_template('index.html', message="Please fill all fields.", greeting=None)

    # Get current date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    details = f"Name: {name}, Class & Section: {class_section}, Roll Number: {roll_number}, Date and Time: {current_time}"

    # Initialize pyttsx3 engine to speak the details
    engine = pyttsx3.init()
    engine.say(f"Your details are: {details}")
    engine.runAndWait()
    engine.stop()

    message = f"Details spoken: {details}"

    return render_template('index.html', message=message, greeting=f"Hello, {name}! Welcome to your dashboard.",
                           name=name, class_section=class_section, roll_number=roll_number)


@app.route('/edit', methods=['POST'])
def edit():
    name = request.form['name']
    class_section = request.form['class_section']
    roll_number = request.form['roll_number']
    return render_template('index.html', name=name, class_section=class_section, roll_number=roll_number)


if __name__ == '__main__':
    app.run(debug=True)
