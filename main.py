import numpy as np
import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

# Load the DataFrame
words_df = pd.read_csv('words_with_translations.csv')
# Initialize correct and incorrect answer counters if not already present
words_df['correct'] = words_df.get('correct', 0)
words_df['incorrect'] = words_df.get('incorrect', 0)

class MistakesView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1  # Set the number of columns to 1
        self.spacing = 5  # Adjust spacing between widgets
        
    def update_mistakes(self):
        print("Updating mistakes...")
        # Sort and update the top 10 mistakes
        mistakes = words_df.sort_values(by='incorrect', ascending=False).head(10)
        self.clear_widgets()  # Clear existing widgets
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
    correct_streak = 0  # Track correct answers in a row
    
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
        
        self.next_word()
        self.update_scoreboard()

    def next_word(self):
        self.current_word = words_df.sample(1).iloc[0]
        self.question_label.text = f"Translate: {self.current_word['spanish_word']}"
        
        # Randomize answer positions
        if np.random.rand() > 0.5:
            self.answer_button1.text = self.current_word['english_translation']
            self.answer_button2.text = words_df.sample(1).iloc[0]['english_translation']
        else:
            self.answer_button2.text = self.current_word['english_translation']
            self.answer_button1.text = words_df.sample(1).iloc[0]['english_translation']
    
    def answer(self, instance):
        if instance.text == self.current_word['english_translation']:
            self.feedback_label.text = "Correct!"
            words_df.loc[words_df['spanish_word'] == self.current_word['spanish_word'], 'correct'] += 1
            self.correct_streak += 1
        else:
            self.feedback_label.text = f"Incorrect! The correct answer was: {self.current_word['english_translation']}"
            words_df.loc[words_df['spanish_word'] == self.current_word['spanish_word'], 'incorrect'] += 1
            self.correct_streak = 0
        self.update_scoreboard()
        self.mistakes_view.update_mistakes()
        self.next_word()
    
    def update_scoreboard(self):
        self.scoreboard_label.text = f"Correct Answers in a Row: {self.correct_streak}"

class FlashcardApp(App):
    def build(self):
        return FlashcardLayout()

if __name__ == '__main__':
    FlashcardApp().run()
