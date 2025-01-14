from flask import Flask, request, jsonify, render_template
from spellchecker import SpellChecker

app = Flask(__name__)
spell = SpellChecker()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_spelling():
    sentence = request.json.get('sentence', '')
    tokens = sentence.split()
    corrected = {word: spell.correction(word) for word in tokens if word in spell.unknown(tokens)}
    return jsonify(corrected)

if __name__ == '__main__':
    app.run(debug=True)
