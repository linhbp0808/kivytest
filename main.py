from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from telethon.sync import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

class TelegramApp(BoxLayout):
    def __init__(self, **kwargs):
        super(TelegramApp, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10

        self.horizontal_box = BoxLayout(orientation='horizontal',size_hint=(None, None), size=(400, 40), pos=(0, 0))
        # Thay thế các giá trị sau bằng thông tin tài khoản Telegram của bạn
        from opentele.td import TDesktop
        from opentele.tl import TelegramClient
        from opentele.api import API, UseCurrentSession
        import asyncio
        api = API.TelegramDesktop.Generate(system='macos',unique_id='2')
        print(api)
        api_id=2040
        api_hash="b18441a1ff607e10a989891a5462e627"
        # Khởi tạo đối tượng TelegramClient
        proxy = {
            'proxy_type': 'http',  # (mandatory) protocol to use (see above)
            'addr': '42.117.216.248',  # (mandatory) proxy IP address
            'port': 10663,  # (mandatory) proxy port number
            'username': 'xoay',  # (optional) username if the proxy requires auth
            'password': 'xoay',  # (optional) password if the proxy requires auth
            'rdns': True
            }
        self.client = TelegramClient('session_name',api=api)#,proxy=proxy)


        # Tạo TextInput để nhập số điện thoại
        self.phone_input = TextInput(hint_text='Enter phone number', size_hint=(None, None), size=(180, 40),multiline=False)

        self.horizontal_box.add_widget(self.phone_input)

        # Tạo Button để xác nhận số điện thoại và kết nối đến Telegram
        self.connect_button = Button(text='->', size_hint=(None, None), size=(50, 40),pos=(190, 0),on_press=self.connect_telegram )

        self.horizontal_box.add_widget(self.connect_button)
        self.add_widget(self.horizontal_box)


        # Tạo TextInput để nhập code xác thực
        self.xacthuc = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(400, 40), pos=(0, 0))
        self.code_input = TextInput(hint_text='Enter code', multiline=False)
        self.pass_input = TextInput(hint_text='Enter pass', multiline=False)
        self.xacthuc.add_widget(self.code_input)
        self.xacthuc.add_widget(self.pass_input)

        # Tạo Button để xác nhận code xác thực
        self.verify_button = Button(text='Verify Code', on_press=self.verify_code)
        self.xacthuc.add_widget(self.verify_button)

        # Tạo TextInput để nhập nội dung tin nhắn
        self.mes=BoxLayout(orientation='horizontal', size_hint=(None, None), size=(400, 40), pos=(0, 0))
        self.message_input = TextInput(hint_text='Enter your message', multiline=False)
        self.mes.add_widget(self.message_input)

        # Tạo Button để gửi tin nhắn
        self.send_button = Button(text='Send Message', on_press=self.send_message)
        self.mes.add_widget(self.send_button)

    def connect_telegram(self, instance):
        # Lấy số điện thoại từ TextInput


        # Kết nối đến Telegram
        self.client.connect()
        print('dd')
        self.remove_widget(self.horizontal_box)
        self.add_widget(self.mes)

        # Kiểm tra xác thực người dùng, nếu chưa xác thực thì yêu cầu xác thực
        if not self.client.is_user_authorized():
            self.add_widget(self.horizontal_box)
            phone_number = self.phone_input.text.strip()
            self.client.send_code_request(phone_number)
            self.add_widget(self.xacthuc)

            print('Code sent to your phone. Enter the code in the next TextInput.')

    def verify_code(self, instance):
        # Lấy code xác thực từ TextInput

        code = self.code_input.text.strip()
        passw=self.pass_input.text.strip()
        # Xác nhận code với Telegram
        try:
            self.client.sign_in(code=code)
            print('Successfully verified!')
            self.remove_widget(self.xacthuc)
        except SessionPasswordNeededError:
            self.client.sign_in(password=passw)

    def send_message(self, instance):
        # Lấy nội dung tin nhắn từ TextInput

        message = self.message_input.text.strip()

        # Gửi tin nhắn đến đối tượng được chỉ định (đổi ID người dùng tương ứng)
        try:
            self.client.send_message('@hieuhieu0808', message)
            print('Message sent successfully!')
        except Exception as e:
            print(f'Error sending message: {e}')

class TelegramKivyApp(App):
    def build(self):
        return TelegramApp()

if __name__ == '__main__':
    TelegramKivyApp().run()
