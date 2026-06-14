# 🕉 Sovereign Vedic AGI — Android App Entry Point
import subprocess
import os

def query_agi(prompt):
    """Call the C++ AGI binary"""
    agi_path = os.path.join(os.path.dirname(__file__), 'vedic_agi')
    result = subprocess.run([agi_path, prompt], capture_output=True, text=True)
    return result.stdout

# Kivy UI
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class VedicAGIApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        self.output = TextInput(readonly=True, size_hint=(1, 0.85), 
                                 background_color=(0.05,0.05,0.1,1),
                                 foreground_color=(0.9,0.85,0.75,1))
        scroll = ScrollView()
        scroll.add_widget(self.output)
        layout.add_widget(scroll)
        
        input_layout = BoxLayout(size_hint=(1, 0.1), spacing=5)
        self.input = TextInput(hint_text='Ask the Vedic AGI...',
                                background_color=(0.1,0.1,0.2,1),
                                foreground_color=(0.9,0.85,0.75,1))
        input_layout.add_widget(self.input)
        
        btn = Button(text='Send', size_hint=(0.2, 1),
                     background_color=(0.78,0.65,0.3,1))
        btn.bind(on_press=self.ask)
        input_layout.add_widget(btn)
        layout.add_widget(input_layout)
        
        return layout
    
    def ask(self, instance):
        prompt = self.input.text.strip()
        if prompt:
            self.output.text += f'\n\n🕉 You: {prompt}\n'
            try:
                response = query_agi(prompt)
                for line in response.split('\n'):
                    if 'Knowledge:' in line:
                        self.output.text += f'🕉 {line.strip()}\n'
            except:
                self.output.text += '🕉 AGI connection error\n'
            self.input.text = ''

if __name__ == '__main__':
    VedicAGIApp().run()
