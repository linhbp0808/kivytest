from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import threading
from datetime import datetime

class ClockApp(App):
    def build(self):
        self.label = Label(text="Current Time")
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)

        # Sử dụng threading để cập nhật thời gian mà không làm đóng băng UI
        threading.Thread(target=self.update_time_thread, daemon=True).start()

        return layout

    def update_time_thread(self):
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            # Sử dụng Clock.schedule_once để đảm bảo cập nhật được thực hiện trên luồng chính của Kivy
            Clock.schedule_once(lambda dt: self.update_label(current_time))
            # Đợi 1 giây trước khi cập nhật thời gian
            threading.Event().wait(1)

    def update_label(self, current_time):
        self.label.text = f"Current Time: {current_time}"

if __name__ == '__main__':
    ClockApp().run()
