from flask import Flask, Response, request, render_template
from transformers import pipeline, AutoModelWithLMHead, AutoTokenizer

model = AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-en-zh")
tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-zh")
translation = pipeline("translation_en_to_zh", model=model, tokenizer=tokenizer)

app = Flask(__name__)


@app.route('/')
def r():
    return render_template('translation.html')
    
@app.route('/en2zh', methods=['POST'])
def en2zh():
# 英文翻译成中文
# AutoModelForSeq2SeqLM.from_pretrained
    text = request.form.get("sentence")
    translated_text = translation(text, max_length=40)[0]['translation_text']
    return translated_text
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)