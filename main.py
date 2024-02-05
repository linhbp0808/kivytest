from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty
from telethon.sync import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
import time
import asyncio
import threading
from datetime import datetime

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
client = TelegramClient('session_name', api_id, api_hash, proxy=proxy)
client.connect()
connect=False
class TelegramApp(BoxLayout):
    def __init__(self, **kwargs):
        super(TelegramApp, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.spacing = 10
        self.size_hint=(1,0.2)
        self.boxchinh = BoxLayout(orientation='horizontal',size_hint=(1,0.1))
        self.boxphu = BoxLayout(orientation='horizontal',size_hint=(1,0.1))
        self.tnhapsdt=TextInput(hint_text='Nhap sdt',size_hint=(0.8,1),font_size=50, multiline=False)
        self.bnhapsdt = Button(text='->',size_hint=(0.2, 1),font_size=50, on_press=self.connect_telegram)
        self.tnhapcode = TextInput(hint_text='Nhap code', size_hint=(0.4, 1),font_size=50, multiline=False)
        self.tnhappass = TextInput(hint_text='Nhap pass 2fa', size_hint=(0.4,1),font_size=50, multiline=False)
        self.bcode = Button(text='->', size_hint=(0.2,1),font_size=50, on_press=self.verify_code)
        self.tnhaptinnhan = TextInput(hint_text='Nhap tinnhan', size_hint=(0.6, 1), font_size=50, multiline=False)
        self.tguitoi = TextInput(hint_text='Gui toi', size_hint=(0.2, 1), font_size=50, multiline=False)


        if not client.is_user_authorized():
           self.boxchinh.add_widget(self.tnhapsdt)
           self.boxchinh.add_widget(self.bnhapsdt)
        else:

            self.lbinfor = Label(text=str(client.get_me().phone + ' đăng nhập thành công'), font_size=50,
                                 size_hint=(1, 1))

            self.boxchinh.add_widget(self.lbinfor)


        self.add_widget(self.boxchinh)


        self.add_widget(self.boxphu)

        self.a=0


    def connect_telegram(self, instance):
        # Kết nối đến Telegram
        self.boxchinh.remove_widget(self.tnhapsdt)
        self.boxchinh.remove_widget(self.bnhapsdt)
        phone_number = self.tnhapsdt.text.strip()
        client.send_code_request(phone_number)

        self.boxchinh.add_widget(self.tnhapcode)
        self.boxchinh.add_widget(self.tnhappass)
        self.boxchinh.add_widget(self.bcode)
    def verify_code(self, instance):
        # Lấy code xác thực từ TextInput
        code = self.tnhapcode.text.strip()
        passw=self.tnhappass.text.strip()
        # Xác nhận code với Telegram
        try:
            client.sign_in(code=code)
            print('Successfully verified!')
            self.remove_widget(self.xacthuc)
        except SessionPasswordNeededError:
            client.sign_in(password=passw)
        self.boxchinh.remove_widget(self.tnhapcode)
        self.boxchinh.remove_widget(self.tnhappass)
        self.boxchinh.remove_widget(self.bcode)
        self.lbinfor = Label(text=str(client.get_me().phone + ' đăng nhập thành công'),font_size=50, size_hint=(1, 1) )
        self.boxchinh.add_widget(self.lbinfor)



class Nhantin (BoxLayout):
    #chobacham = ObjectProperty(None)
    def __init__(self, **kwargs):
        pass

    def bacham(self, instance):
            self.boxphu1.remove_widget(self.blaytn)
            self.boxphu1.add_widget(self.chobacham)
            self.boxphu1.add_widget(self.chobacham1)
class CombinedLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(CombinedLayout, self).__init__(orientation='vertical', **kwargs)
        self.layout_a = TelegramApp()
        #self.layout_b = Nhantin()
        self.bgui = Button(text='->', size_hint=(0.2, 1), font_size=50, on_press=self.pa)
        self.layout_a.boxphu.add_widget(self.layout_a.tnhaptinnhan)
        self.layout_a.boxphu.add_widget(self.layout_a.tguitoi)
        self.layout_a.boxphu.add_widget(self.bgui)
        self.add_widget(self.layout_a)
        #self.add_widget(self.layout_b)
        self.client=client





    def laytinnhantele(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.a=1
        self.client1.connect()
        client=self.client1

        with client:
            @client.on(events.NewMessage(from_users='tuyetbp0808'))
            async def create_poll(event):
                nds = event.message.message
                Clock.schedule_once(lambda dt: self.update_result(nds))
                if 'MessageID:' in nds:
                    time.sleep(3)
                    nd = nds.split('\n')
                    sdus = str(nd[4]).split(':')[1].split()[0]
                    sdu = sdus.replace('.', '')
                    if int(sdu) >= 100000:
                        await client.disconnect()
                    if nd[0] == '🏆🏆🏆 THẮNG RỒI 🏆🏆🏆':
                        if nd[1] == '💶 ND cược: Xxc':
                            await client.send_message('tuyetbp0808', 'Xxl 100')
                        elif nd[1] == '💶 ND cược: Xxl':
                            await client.send_message('tuyetbp0808', 'Xxc 100')
                    elif nd[0] == '😭😭😭 THUA MẤT RỒI 😭😭😭':
                        cl = str(nd[1]).split(':')[1]
                        tiens = str(nd[2]).split(':')[1].split()[0]
                        tien = tiens.replace('.', '')
                        print(tien)
                        cuoc = int(tien) * 2
                        if cuoc >= int(sdu) / 2:
                            cuoc = 100
                        await client.send_message('tuyetbp0808', str(cl + ' ' + '100'))
                    print(sdu)

            client.run_until_disconnected()

    def send_message(self,instance):
        # Lấy nội dung tin nhắn từ TextInput

        message = self.layout_a.tnhaptinnhan.text.strip()
        toi = self.layout_a.tguitoi.text.strip()
        # Gửi tin nhắn đến đối tượng được chỉ định (đổi ID người dùng tương ứng)
        try:
            self.client1.connect()
            self.client1.send_message(toi, message)
            print('Message sent successfully!')
        except Exception as e:
            print(f'Error sending message: {e}')
    def pa(self,instance):
        pass

    def update_result(self, result):
        # Use Clock.schedule_once to update the label in the main thread
        self.layout_b.chobacham.text = str(result)


class TelegramKivyApp(App):
    def build(self):
        self.label = Label(text="tn",size_hint=(1,0.2))
        self.label1 = Label(text="Current Time",size_hint=(1,0.2))

        layout = CombinedLayout()
        layout.add_widget(self.label)
        layout.add_widget(self.label1)

        # Sử dụng threading để cập nhật thời gian mà không làm đóng băng UI

        if  client.is_user_authorized():
            client.disconnect()
            threading.Thread(target=self.laytinnhantele, daemon=True).start()
            threading.Thread(target=self.update_time_thread, daemon=True).start()

        return layout
    def laytinnhantele(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client1= TelegramClient('session_name', api_id, api_hash, proxy=proxy)
        client=client1
        with client:
            @client.on(events.NewMessage(from_users='tuyetbp0808'))
            async def create_poll(event):
                nds = event.message.message
                Clock.schedule_once(lambda dt: self.update_label(nds))
                if 'MessageID:' in nds:
                    time.sleep(3)
                    nd = nds.split('\n')
                    sdus = str(nd[4]).split(':')[1].split()[0]
                    sdu = sdus.replace('.', '')
                    if int(sdu) >= 100000:
                        await client.disconnect()
                    if nd[0] == '🏆🏆🏆 THẮNG RỒI 🏆🏆🏆':
                        if nd[1] == '💶 ND cược: Xxc':
                            await client.send_message('tuyetbp0808', 'Xxl 100')
                        elif nd[1] == '💶 ND cược: Xxl':
                            await client.send_message('tuyetbp0808', 'Xxc 100')
                    elif nd[0] == '😭😭😭 THUA MẤT RỒI 😭😭😭':
                        cl = str(nd[1]).split(':')[1]
                        tiens = str(nd[2]).split(':')[1].split()[0]
                        tien = tiens.replace('.', '')
                        print(tien)
                        cuoc = int(tien) * 2
                        if cuoc >= int(sdu) / 2:
                            cuoc = 100
                        await client.send_message('tuyetbp0808', str(cl + ' ' + '100'))
                    print(sdu)

            client.run_until_disconnected()

    def update_time_thread(self):
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            # Sử dụng Clock.schedule_once để đảm bảo cập nhật được thực hiện trên luồng chính của Kivy
            Clock.schedule_once(lambda dt: self.update_label1(current_time))
            # Đợi 1 giây trước khi cập nhật thời gian
            #threading.Event().wait(1)

    def update_label(self, current_time):
        self.label.text = f"tn: {current_time}"
    def update_label1(self, current_time):
        self.label1.text = f"Current Time: {current_time}"



if __name__ == '__main__':
    TelegramKivyApp().run()
