import numpy as np
import pandas as pd
import logging
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the DataFrame
words_df = pd.read_csv('words_with_translations.csv')

# Ensure 'correct', 'incorrect', and 'correct_streak' columns exist
for col in ['correct', 'incorrect', 'correct_streak']:
    if col not in words_df.columns:
        words_df[col] = 0

# Calculate difficulty
words_df['difficulty'] = words_df['incorrect'] - words_df['correct'] + 1
words_df['difficulty'] = words_df['difficulty'].apply(lambda x: max(x, 0.01))  # Avoid negative values

logging.info("Difficulty levels initialized.")

class MistakesView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.spacing = 5
        
    def update_mistakes(self):
        mistakes = words_df.sort_values(by='incorrect', ascending=False).head(10)
        self.clear_widgets()
        for _, row in mistakes.iterrows():
            btn = Button(text=f"{row['spanish_word']}: {row['incorrect']} mistakes")
            btn.bind(on_press=lambda instance, word=row['spanish_word'], translation=row['english_translation']: self.show_translation(word, translation))
            self.add_widget(btn)
    
    def show_translation(self, word, translation, *args):
        popup = Popup(title='Translation',
                      content=Label(text=f"{word}: {translation}"),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

class FlashcardLayout(BoxLayout):
    correct_streak = 0
    review_mode = False  # Add a flag for review mode
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.scoreboard_label = Label(size_hint_y=0.1, font_size=18)
        self.add_widget(self.scoreboard_label)
        
        self.question_label = Label(size_hint_y=0.2, font_size=20)
        self.add_widget(self.question_label)
        
        self.answer_button1 = Button(size_hint_y=0.1)
        self.answer_button1.bind(on_press=self.answer)
        self.add_widget(self.answer_button1)
        
        self.answer_button2 = Button(size_hint_y=0.1)
        self.answer_button2.bind(on_press=self.answer)
        self.add_widget(self.answer_button2)
        
        self.feedback_label = Label(size_hint_y=0.1, font_size=18)
        self.add_widget(self.feedback_label)
        
        self.mistakes_view = MistakesView(size_hint_y=0.5)
        self.add_widget(self.mistakes_view)
        
        # Adjust the size and add a button to toggle review mode
        self.toggle_review_btn = Button(text='Toggle Review Mode', size_hint_y=0.05, size_hint_x=None, width=200)
        self.toggle_review_btn.bind(on_press=lambda instance: self.toggle_review_mode())
        self.add_widget(self.toggle_review_btn)
        
        self.next_word()
        self.update_scoreboard()

    def toggle_review_mode(self):
        # Method to toggle review mode
        self.review_mode = not self.review_mode
        logging.info(f"Review Mode {'enabled' if self.review_mode else 'disabled'}.")
        self.next_word()  # Refresh the word selection based on the new mode

    def next_word(self):
        eligible_words = words_df[words_df['correct_streak'] < 4]
        if self.review_mode:
            difficult_words = eligible_words[eligible_words['difficulty'] > 1.0]
            if not difficult_words.empty:
                weighted_selection = difficult_words.sample(n=1, weights='difficulty')
            else:
                self.review_mode = False
                weighted_selection = eligible_words.sample(n=1, weights='difficulty')
        else:
            weighted_selection = eligible_words.sample(n=1, weights='difficulty')
        
        if weighted_selection.empty:
            self.question_label.text = "Congratulations! You've practiced all words."
            return
        
        self.current_word = weighted_selection.iloc[0]
        self.question_label.text = f"Translate: {self.current_word['spanish_word']}"
        logging.info(f"Selected word: {self.current_word['spanish_word']} with difficulty: {self.current_word['difficulty']}")
        
        correct_answer = self.current_word['english_translation']
        wrong_answer = eligible_words[eligible_words['english_translation'] != correct_answer].sample(1).iloc[0]['english_translation']
        if np.random.rand() > 0.5:
            self.answer_button1.text = correct_answer
            self.answer_button2.text = wrong_answer
        else:
            self.answer_button2.text = correct_answer
            self.answer_button1.text = wrong_answer
    
    def answer(self, instance):
        word = self.current_word['spanish_word']
        if instance.text == self.current_word['english_translation']:
            self.feedback_label.text = "Correct!"
            words_df.loc[words_df['spanish_word'] == word, 'correct'] += 1
            new_streak = words_df.loc[words_df['spanish_word'] == word, 'correct_streak'] + 1
            words_df.loc[words_df['spanish_word'] == word, 'correct_streak'] = new_streak
            self.correct_streak += 1
            logging.info(f"Correct answer for '{word}'. Correct streak updated to {new_streak.values[0]}.")
            if new_streak.values[0] >= 4:
                logging.info(f"'{word}' has been mastered and will be excluded from future selections.")
        else:
            self.feedback_label.text = f"Incorrect! The correct answer was: {self.current_word['english_translation']}"
            words_df.loc[words_df['spanish_word'] == word, 'incorrect'] += 1
            words_df.loc[words_df['spanish_word'] == word, 'correct_streak'] = 0
            self.correct_streak = 0
            logging.info(f"Incorrect answer for '{word}'. Correct streak reset to 0.")
        
        self.update_scoreboard()
        self.mistakes_view.update_mistakes()
        words_df.to_csv('words_with_translations.csv', index=False)  # Save progress after each answer
        self.next_word()
    
    def update_scoreboard(self):
        self.scoreboard_label.text = f"Correct Answers in a Row: {self.correct_streak}"

class FlashcardApp(App):
    def build(self):
        return FlashcardLayout()

if __name__ == '__main__':
    FlashcardApp().run()
