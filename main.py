from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from telethon.sync import TelegramClient, events

class TelegramApp(BoxLayout):
    def __init__(self, **kwargs):
        super(TelegramApp, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.spacing = 10

        # Thay thế các giá trị sau bằng thông tin tài khoản Telegram của bạn
        from opentele.td import TDesktop
        from opentele.tl import TelegramClient
        from opentele.api import API, UseCurrentSession
        import asyncio
        api = API.TelegramAndroid.Generate()


        # Khởi tạo đối tượng TelegramClient
        self.client = TelegramClient('session_name', api=api)

        # Tạo TextInput để nhập số điện thoại
        self.phone_input = TextInput(hint_text='Enter phone number', multiline=False)
        self.add_widget(self.phone_input)

        # Tạo Button để xác nhận số điện thoại và kết nối đến Telegram
        self.connect_button = Button(text='Connect to Telegram', on_press=self.connect_telegram)
        self.add_widget(self.connect_button)

        # Tạo TextInput để nhập code xác thực
        self.code_input = TextInput(hint_text='Enter code', multiline=False)
        self.add_widget(self.code_input)

        # Tạo Button để xác nhận code xác thực
        self.verify_button = Button(text='Verify Code', on_press=self.verify_code)
        self.add_widget(self.verify_button)

        # Tạo TextInput để nhập nội dung tin nhắn
        self.message_input = TextInput(hint_text='Enter your message', multiline=False)
        self.add_widget(self.message_input)

        # Tạo Button để gửi tin nhắn
        self.send_button = Button(text='Send Message', on_press=self.send_message)
        self.add_widget(self.send_button)

    def connect_telegram(self, instance):
        # Lấy số điện thoại từ TextInput
        phone_number = self.phone_input.text.strip()

        # Kết nối đến Telegram
        self.client.connect()

        # Kiểm tra xác thực người dùng, nếu chưa xác thực thì yêu cầu xác thực
        if not self.client.is_user_authorized():
            self.client.send_code_request(phone_number)
            print('Code sent to your phone. Enter the code in the next TextInput.')

    def verify_code(self, instance):
        # Lấy code xác thực từ TextInput
        code = self.code_input.text.strip()

        # Xác nhận code với Telegram
        try:
            self.client.sign_in(code=code)
            print('Successfully verified!')
        except Exception as e:
            print(f'Error verifying code: {e}')

    def send_message(self, instance):
        # Lấy nội dung tin nhắn từ TextInput
        message = self.message_input.text.strip()

        # Gửi tin nhắn đến đối tượng được chỉ định (đổi ID người dùng tương ứng)
        try:
            self.client.send_message('target_username', message)
            print('Message sent successfully!')
        except Exception as e:
            print(f'Error sending message: {e}')

class TelegramKivyApp(App):
    def build(self):
        return TelegramApp()

if __name__ == '__main__':
    TelegramKivyApp().run()
