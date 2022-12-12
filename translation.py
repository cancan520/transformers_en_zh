# @Time    : 2021/5/27 15:28
# @Author  :

from transformers import pipeline, AutoModelWithLMHead, AutoTokenizer

# 英文翻译成中文
# AutoModelForSeq2SeqLM.from_pretrained
model = AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-en-zh")
tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-zh")
translation = pipeline("translation_en_to_zh", model=model, tokenizer=tokenizer)

text = "Student accommodation centres, resorts"
translated_text = translation(text, max_length=40)[0]['translation_text']
print(translated_text)
# 中文翻译成英文
model = AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
translation = pipeline("translation_zh_to_en", model=model, tokenizer=tokenizer)

text = "早上好，今天我们一起去打羽毛球吧。"
translated_text = translation(text, max_length=40)[0]['translation_text']
print(translated_text)