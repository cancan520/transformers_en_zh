from flask import Flask, Response, request, render_template
from transformers import pipeline, AutoModelWithLMHead, AutoTokenizer

model = AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-en-zh")
tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-zh")
translation = pipeline("translation_en_to_zh", model=model, tokenizer=tokenizer)

model2 = AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
tokenizer2 = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
translation2 = pipeline("translation_zh_to_en", model=model2, tokenizer=tokenizer2)

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

@app.route('/zh2en', methods=['POST'])
def zh2en():
    # 中文翻译成英文
    text2 = request.form.get("sentence")
    translated_text2 = translation2(text2, max_length=40)[0]['translation_text']
    return translated_text2

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)