from googletrans import Translator
translator = Translator()

intext = input('English text: ')
print('結果')
print(translator.translate(intext, src='en', dest='ja').text)
