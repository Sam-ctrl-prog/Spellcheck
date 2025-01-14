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
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    if file.filename.endswith('.txt'):
        text = file.read().decode('utf-8')
    elif file.filename.endswith('.docx'):
        from docx import Document
        doc = Document(file)
        text = ' '.join([p.text for p in doc.paragraphs])
    else:
        return "Unsupported file type", 400
    
    spell = SpellChecker()
    words = text.split()
    corrected = [spell.correction(word) for word in words]
    corrected_text = ' '.join(corrected)
    
    return render_template('result.html', original=text, corrected=corrected_text)

if __name__ == '__main__':
    app.run(debug=True)
