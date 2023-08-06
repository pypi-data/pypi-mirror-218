from setuptools import setup

setup(
    name='sWaraNuvad',
    version='2.4',
    description='Speech translation assistant',
    author='Tejas Sonavane',
    long_description='''The code uses speech recognition to capture user input through a microphone. It then recognizes the speech using Google's Speech-to-Text API. 
    The user is prompted to specify a language, and their subsequent speech is translated into multiple languages. The translations are displayed in the console.
    The speech translation assistant allows users to communicate in different languages by converting their spoken input into written text and providing translations in various supported languages.''',
    packages=['sWaraNuvad'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
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
