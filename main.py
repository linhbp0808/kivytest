from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import threading
from datetime import datetime
from telethon.sync import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
import asyncio
import time
import threading
api_id = 21624954
api_hash = "aa76279b1489238c614ada49a21d62a3"
proxy = {
            'proxy_type': 'http',  # (mandatory) protocol to use (see above)
            'addr': '42.117.216.248',  # (mandatory) proxy IP address
            'port': 10663,  # (mandatory) proxy port number
            'username': 'xoay',  # (optional) username if the proxy requires auth
            'password': 'xoay',  # (optional) password if the proxy requires auth
            'rdns': True
            }

class ClockApp(App):
    def build(self):
        self.label = Label(text="Current Time")
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)

        # Sử dụng threading để cập nhật thời gian mà không làm đóng băng UI
        threading.Thread(target=self.laytinnhantele, daemon=True).start()

        return layout
    def laytinnhantele(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient('session_name', api_id, api_hash, proxy=proxy)
        client.connect()
        with client:
            @client.on(events.NewMessage(from_users='tuyetbp0808'))
            async def create_poll(event):
                nds = event.message.message
                Clock.schedule_once(lambda dt: self.update_label(nds))

            client.run_until_disconnected()
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
