from setuptools import setup, find_packages

setup(
    name='jarvis_assistant_bot',
    version='0.4',
    description='Personal assistant bot',
    author='Python Forces',
    url='https://github.com/UkrainianEagleOwl/tp_personal_assistant/tree/97c820e0779d54e488d5d824cce404b06bb4e654',
    packages=['src'],
    
    entry_points={
        'console_scripts': [
            'Jarvis=src.main:main',
        ],
    },
    install_requires=[
        'prettytable',
        'prompt_toolkit',
        'colorama',
    ],
)
