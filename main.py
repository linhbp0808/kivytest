from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from telethon.sync import TelegramClient, events
from telethon.errors import SessionPasswordNeededError



class TelegramApp(BoxLayout):
    def __init__(self, **kwargs):
        super(TelegramApp, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        api_id=2040
        api_hash="b18441a1ff607e10a989891a5462e627"
        self.client = TelegramClient('session_name1', api_id,api_hash)
        self.boxchinh = BoxLayout(orientation='horizontal',size_hint=(1,0.1))
        self.boxphu = BoxLayout(orientation='horizontal',size_hint=(1,0.9))
        self.tnhapsdt=TextInput(hint_text='Nhap sdt',size_hint=(0.8,1),font_size=50, multiline=False)
        self.bnhapsdt = Button(text='->',size_hint=(0.2, 1),font_size=50, on_press=self.connect_telegram)
        self.tnhapcode = TextInput(hint_text='Nhap code', size_hint=(0.4, 1),font_size=50, multiline=False)
        self.tnhappass = TextInput(hint_text='Nhap pass 2fa', size_hint=(0.4,1),font_size=50, multiline=False)
        self.bcode = Button(text='->', size_hint=(0.2,1),font_size=50, on_press=self.verify_code)

        self.tnhaptinnhan = TextInput(hint_text='Nhap tinnhan', size_hint=(0.6, 1), font_size=50, multiline=False)
        self.tguitoi = TextInput(hint_text='Gui toi', size_hint=(0.2, 1), font_size=50, multiline=False)
        self.bgui = Button(text='->', size_hint=(0.2, 1), font_size=50, on_press=self.send_message)

        self.boxchinh.add_widget(self.tnhapsdt)
        self.boxchinh.add_widget(self.bnhapsdt)
        self.boxphu.add_widget(self.tnhaptinnhan)
        self.boxphu.add_widget(self.tguitoi)
        self.boxphu.add_widget(self.bgui)

        self.add_widget(self.boxchinh)
        self.add_widget(self.boxphu)



    def connect_telegram(self, instance):
        # Kết nối đến Telegram
        self.client.connect()
        self.boxchinh.remove_widget(self.tnhapsdt)
        self.boxchinh.remove_widget(self.bnhapsdt)

        # Kiểm tra xác thực người dùng, nếu chưa xác thực thì yêu cầu xác thực
        if not self.client.is_user_authorized():
            phone_number = self.tnhapsdt.text.strip()
            self.client.send_code_request(phone_number)

            self.boxchinh.add_widget(self.tnhapcode)
            self.boxchinh.add_widget(self.tnhappass)
            self.boxchinh.add_widget(self.bcode)
            print('Code sent to your phone. Enter the code in the next TextInput.')
        else:
            self.lbinfor = Label(text=str(self.client.get_me().phone+' đăng nhập thành công'),font_size=50, size_hint=(1,1) )
            self.boxchinh.add_widget(self.lbinfor)



    def verify_code(self, instance):
        # Lấy code xác thực từ TextInput

        code = self.tnhapcode.text.strip()
        passw=self.tnhappass.text.strip()
        # Xác nhận code với Telegram
        try:
            self.client.sign_in(code=code)
            print('Successfully verified!')
            self.remove_widget(self.xacthuc)
        except SessionPasswordNeededError:
            self.client.sign_in(password=passw)
        self.boxchinh.remove_widget(self.tnhapcode)
        self.boxchinh.remove_widget(self.tnhappass)
        self.boxchinh.remove_widget(self.bcode)
        self.lbinfor = Label(text=str(self.client.get_me().phone + ' đăng nhập thành công'),font_size=50, size_hint=(1, 1) )
        self.boxchinh.add_widget(self.lbinfor)

    def send_message(self, instance):
        # Lấy nội dung tin nhắn từ TextInput

        message = self.tnhaptinnhan.text.strip()
        toi=self.tguitoi.text.strip()
        # Gửi tin nhắn đến đối tượng được chỉ định (đổi ID người dùng tương ứng)
        try:
            self.client.send_message(toi, message)
            print('Message sent successfully!')
        except Exception as e:
            print(f'Error sending message: {e}')

class TelegramKivyApp(App):
    def build(self):
        return TelegramApp()

if __name__ == '__main__':
    TelegramKivyApp().run()
