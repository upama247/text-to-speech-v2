from flask import Flask, render_template, request
from gtts import gTTS
from datetime import datetime
import os
import io
import base64

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

    # Initialize gTTS to speak the details
    tts = gTTS(f"Your details are: {details}", lang='en')

    # Save the speech to a byte buffer
    audio_buffer = io.BytesIO()
    tts.save(audio_buffer)
    audio_buffer.seek(0)

    # Convert the audio to base64 to be sent to the browser
    audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')

    message = f"Details spoken: {details}"

    return render_template('index.html', message=message, greeting=f"Hello, {name}! Welcome to your dashboard.",
                           name=name, class_section=class_section, roll_number=roll_number, audio_base64=audio_base64)


@app.route('/edit', methods=['POST'])
def edit():
    name = request.form['name']
    class_section = request.form['class_section']
    roll_number = request.form['roll_number']
    return render_template('index.html', name=name, class_section=class_section, roll_number=roll_number)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
