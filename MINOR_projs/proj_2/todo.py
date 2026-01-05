from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

Window.clearcolor = (0.07, 0.07, 0.07, 1) 


class Card(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = 10
        self.spacing = 10
        with self.canvas.before:
            Color(0.12, 0.12, 0.12, 1)
            self.rect = RoundedRectangle(radius=[10])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class TodoApp(App):
    def build(self):
        self.tasks = []

        root = BoxLayout(orientation='vertical', padding=20, spacing=15)

        title = Label(
            text='My Todo App',
            font_size='24sp',
            size_hint_y=None,
            height=50,
            bold=True
        )
        root.add_widget(title)


        self.input_task = TextInput(
            hint_text='Add or update task...',
            size_hint_y=None,
            height=45,
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1)
        )
        root.add_widget(self.input_task)

        btn_row = BoxLayout(size_hint_y=None, height=45, spacing=10)

        add_btn = Button(text='Add', background_color=(0.3, 0.7, 0.3, 1))
        add_btn.bind(on_press=self.add_task)

        update_btn = Button(text='Update', background_color=(0.2, 0.6, 1, 1))
        update_btn.bind(on_press=self.update_task)

        btn_row.add_widget(add_btn)
        btn_row.add_widget(update_btn)
        root.add_widget(btn_row)


        self.tasks_layout = BoxLayout(orientation='vertical', spacing=10)
        root.add_widget(self.tasks_layout)

        del_btn = Button(
            text='Delete Completed',
            size_hint_y=None,
            height=45,
            background_color=(0.9, 0.2, 0.2, 1)
        )
        del_btn.bind(on_press=self.delete_completed_tasks)
        root.add_widget(del_btn)

        return root

    def add_task(self, instance):
        text = self.input_task.text.strip()
        if not text:
            return

        card = Card(size_hint_y=None, height=50)

        checkbox = CheckBox(size_hint_x=None, width=40)
        label = Label(text=text, halign='left', valign='middle')
        label.bind(size=lambda s, *_: setattr(s, 'text_size', s.size))

        card.add_widget(checkbox)
        card.add_widget(label)

        self.tasks_layout.add_widget(card)
        self.tasks.append(card)

        self.input_task.text = ''

    def update_task(self, instance):
        new_text = self.input_task.text.strip()
        if not new_text:
            return

        for task in self.tasks:
            checkbox = task.children[1]
            label = task.children[0]

            if checkbox.active:
                label.text = new_text
                checkbox.active = False

        self.input_task.text = ''

    def delete_completed_tasks(self, instance):
        for task in self.tasks[:]:
            checkbox = task.children[1]
            if checkbox.active:
                self.tasks_layout.remove_widget(task)
                self.tasks.remove(task)


if __name__ == "__main__":
    TodoApp().run()
