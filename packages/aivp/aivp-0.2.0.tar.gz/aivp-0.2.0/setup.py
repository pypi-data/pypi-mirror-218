from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aivp',
    version='0.2.0',
    description='AI and Voice Processing Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['aivp'],
    install_requires=[
        'SpeechRecognition',
        'gTTS',
        'playsound',
        'characterai'
    ],
    author='Caleb Costa',
    url='https://github.com/removeableox/aivp',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
