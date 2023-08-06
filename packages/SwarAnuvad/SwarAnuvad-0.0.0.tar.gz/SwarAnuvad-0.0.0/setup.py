from setuptools import setup

setup(
    name='SwarAnuvad',
    version='',
    description='Speech translation assistant',
    author='Tejas Sonavane',
    long_description='''The code uses speech recognition to capture user input through a microphone. It then recognizes the speech using Google's Speech-to-Text API. 
    The user is prompted to specify a language, and their subsequent speech is translated into multiple languages. The translations are displayed in the console.
    The speech translation assistant allows users to communicate in different languages by converting their spoken input into written text and providing translations in various supported languages.
    
    https://github.com/Tejass0/SwarAnuvad


# Make sure you have upgraded version of pip
Windows
```
py -m pip install --upgrade pip
```

Linux/MAC OS
```
python3 -m pip install --upgrade pip
```


# Requirements
Python 3.9+


# Installation
Install using pip...
```
pip install SwarAnuvad
pip3 install SwarAnuvad
```

# Example
```
from SwarAnuvad import SwarAnuvad

s = SwarAnuvad()
pop = s.lantrans()
print(pop, "++++")
```

# Output
```
['GREEK: Πώς είσαι', 'ESPERANTO: kiel vi fartas', 'ENGLISH: how are you', 'AFRIKAANS: Hoe gaan dit', 'SWAHILI: habari yako', 'CATALAN: Com estàs', 'ITALIAN: Come stai', 'HEBREW: מה שלומך', 'SWEDISH: Hur mår du', 'CZECH: jak se máte', 'WELSH: Sut wyt ti', 'ARABIC: كيف حالك', 'URDU: آپ کیسے ہو', 'IRISH: Conas tá tú', 'BASQUE: zelan zaude', 'ESTONIAN: kuidas sul läheb', 'AZERBAIJANI: necəsən', 'INDONESIAN: Apa kabarmu', 'SPANISH: Cómo estás', 'RUSSIAN: Как вы', 'GALICIAN: como estás', 'DUTCH: Hoe is het', 'PORTUGUESE: como vai', 'LATIN: quid agis', 'TURKISH: Nasılsın', 'FILIPINO: Kamusta ka', 'LATVIAN: kā tev iet', 'LITHUANIAN: kaip laikaisi', 'THAI: คุณเป็นอย่างไร', 'VIETNAMESE: Bạn khỏe không', 'ROMANIAN: ce mai faci', 'ICELANDIC: hvernig hefurðu það', 'POLISH: Jak się masz', 'TAMIL: எப்படி இருக்கிறீர்கள்', 'YIDDISH: וואס מאכסטו', 'BELARUSIAN: як ты', 'FRENCH: comment allez-vous', 'BULGARIAN: Как си', 'UKRAINIAN: як справи', 'CROATIAN: kako si', 'BENGALI: আপনি কেমন আছেন', 'SLOVENIAN: Kako si', 'HAITIAN CREOLE: koman ou ye', 'DANISH: Hvordan har du det', 'PERSIAN: چطور هستید', 'HINDI: आप कैसे हैं', 'FINNISH: mitä kuuluu', 'HUNGARIAN: hogy vagy', 'JAPANESE: 元気ですか', 'GEORGIAN: როგორ ხარ', 'TELUGU: మీరు ఎలా ఉన్నారు', 'CHINESE TRADITIONAL: 你好嗎', 'ALBANIAN: si jeni', 'NORWEGIAN: hvordan har du det', 'KOREAN: 어떻게 지내세요', 'KANNADA: ನೀವು ಹೇಗಿದ್ದೀರಿ', 'MACEDONIAN: како си', 'CHINESE SIMPLIFIED: 你好吗', 'SLOVAK: ako sa máš', 'MALTESE: kif int', 'MARATHI: तू कसा आहेस', 'GERMAN: Wie geht es dir', 'MALAY: apa khabar', 'SERBIAN: како си'] ++++
```

# Please wait at-least 20 seconds to see the output.
# Currently, this package is on upgrade.
# ''',
    packages=['SwarAnuvad'],
    long_description_content_type="text/markdown",
    keywords=['voice translate', 'voice to text translate', 'multiple language voice translate', 'translate', 'text to voice translate'],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License", 
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=[
        'pyttsx3',
        'SpeechRecognition',
        'translate',
        'PyAudio',
        'googletrans'
    ],
)
