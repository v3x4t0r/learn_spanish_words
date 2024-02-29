# Spanish Learning Game

## Overview
This Spanish Learning Game is designed to help users learn and master the 500 most common Spanish words through a flashcard-style quiz application. Built with Python and the Kivy framework, it offers an interactive way to strengthen your vocabulary skills.

## Features
- **Flashcard Quiz**: Presents words to translate from Spanish to English, testing your knowledge and helping you learn.
- **Adaptive Difficulty**: Words are selected based on their difficulty level, which adjusts based on your answer history.
- **Review Mode**: Toggle a review mode to focus on words you've struggled with, allowing for targeted learning.
- **Progress Tracking**: Tracks your correct and incorrect answers, adjusting the selection of words accordingly.
- **Mastery System**: Words answered correctly a certain number of times are considered mastered and excluded from future selection.

## Planned features
- **Stars System**: Awards stars for every set of 30 correct answers, resetting upon receiving a wrong answer, to motivate learning.
- **Changing Mastery Criteria**: Adjust `CORRECT_ANSWERS_REQUIRED_FOR_MASTERY` in the script to change how many times a word must be answered correctly before it's considered mastered.

## Requirements
- Python 3.6 or later
- Kivy
- Pandas
- NumPy

## Installation
Ensure you have Python installed, then install Kivy and Pandas using pip:

```bash
pip install kivy pandas numpy
```

## How to Use

- The application will automatically load a Spanish word for you to translate.
- Click on one of the two buttons to choose your answer.
- The application will provide immediate feedback on your choice.
- Use the "Toggle Review Mode" button to focus on words you find difficult.
- Your progress is visually represented through the accumulation of stars, which are awarded for correct answers and reset after a wrong answer.
- Mastered words (answered correctly 4 times in a row) will be excluded from future selections.

## Data Persistence

Your progress (correct and incorrect answers) is saved automatically, allowing you to pick up where you left off in future sessions.

## Customizing the Application

- **Modifying the Word List**: Update `words_with_translations.csv` with new words or translations as desired. The list consists of 500 of 5000 total words. See "word list generation" for more info.

## Contributing

Feel free to fork the repository and submit pull requests to contribute to the development of this learning tool.


## Word List Generation

The word list used in this Spanish Learning Game is generated based on a unique approach focused on the practicality and relevance of learning. The concept emphasizes the importance of common words in accelerating language learning progress. The methodology behind generating this list involves analyzing thousands of subtitles from movies and TV shows across various Spanish-speaking countries, including Spain, Mexico, Argentina, Colombia, and Chile. This corpus reflects the actual usage of Spanish, identifying words with high contextual diversity - those appearing across a wide range of media.

The aim was to isolate the most common words that constitute the backbone of spoken Spanish. Research indicates that with just the 1,000 most common words, one can cover 79% of spoken Spanish, and with 5,000 words, nearly 90% coverage is achievable. This effort culminated in the creation of a comprehensive word list that forms the foundation of the "SpanishInput" course. This course is distinguished by its focus on teaching the most common Spanish words through comprehensible input, ensuring efficient learning without the distraction of less relevant vocabulary.

### Credit

The word list and the educational methodology are the creations of [SpanishInput](https://youtube.com/SpanishInput), a resource dedicated to teaching Spanish effectively by concentrating on the most frequently used words in the language. The project's innovator has made available a free PDF and Excel file of the word list, reflecting the dedication to spreading knowledge and assisting learners in achieving fluency in Spanish through practical means.

For more information and access to the first lessons of the SpanishInput course, visit the [SpanishInput YouTube channel](https://youtube.com/SpanishInput).



## License

[MIT License](LICENSE)

Enjoy enhancing your Spanish vocabulary with our learning game!

