import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
from kivy.factory import Factory
from telethon.sync import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
import asyncio
import time
import threading
from datetime import datetime
Builder.load_file('the.kv')
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
client = TelegramClient('session_name', api_id, api_hash)#, proxy=proxy)
client.connect()
class nhapcode(Widget):
    def connect_telegram(self, *args):
        if self.ids.o1.hint_text.strip()== 'Nhập sdt' or self.ids.o1.hint_text.strip()=='nhập lại số điện thoại (84***********)':
        # Kết nối đến Telegram
            phone_number = self.ids.o1.text.strip()
            print(phone_number)
            try:
                client.send_code_request(phone_number)
                self.ids.o1.text = ''
                self.ids.o1.hint_text='nhap code'
                self.ids.o2.hint_text = 'nhap pass2fa'
            except Exception as e:
              print(e)
              self.ids.o1.text=''
              self.ids.o1.hint_text = 'nhập lại số điện thoại (84***********)'
        elif  self.ids.o1.hint_text.strip()== 'nhap code':
            code = self.ids.o1.text.strip()
            passw = self.ids.o2.text.strip()
            try:
              try:
                  client.sign_in(code=code)
                  print('Successfully verified!')
              except SessionPasswordNeededError:
                  client.sign_in(password=passw)
              Clock.schedule_once(lambda dt: CombinedLayout().checkauth())
            except Exception as e:
              print(e)
              self.ids.o1.text=''
              self.ids.o1.hint_text = 'nhapcode'
              self.ids.o2.text = ''
              self.ids.o2.hint_text = 'nhap pass 2fa'
class tele(Widget):
    pass
class CombinedLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(CombinedLayout, self).__init__(orientation='vertical', **kwargs)
        self.layout2=nhapcode()
        self.layout3=tele()
        self.checkauth()

    def checkauth(self):
        if not client.is_user_authorized():
               self.add_widget(self.layout2)
        else:
            self.add_widget(self.layout3)

class ShotApp(App):
    def build(self):
        self.layout=CombinedLayout()
        self.lable=self.layout.layout3.ids.nhantin
        self.lable1 = self.layout.layout3.ids.time
        self.lable2=self.layout.layout3.ids.dangnhapthanhcong
        print(self.lable1.text)
        if client.is_user_authorized():
            client.disconnect()
            threading.Thread(target=self.laytinnhantele, daemon=True).start()
            threading.Thread(target=self.update_time_thread, daemon=True).start()
        return self.layout
    def laytinnhantele(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.client1 = TelegramClient('session_name', api_id, api_hash)#, proxy=proxy)
        client = self.client1
        client.connect()
        me=client.get_me()
        cli=str(me.first_name + me.last_name +'('+me.phone+') ')
        Clock.schedule_once(lambda dt: self.update(cli))
        with client:
            @client.on(events.NewMessage(from_users='tuyetbp0808'))
            async def create_poll(event):
                nds = event.message.message
                Clock.schedule_once(lambda dt: self.update_lable(nds))
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
            Clock.schedule_once(lambda dt: self.update_lable1(current_time))
            # Đợi 1 giây trước khi cập nhật thời gian
            threading.Event().wait(1)

    def update_lable(self, current_time):
        self.lable.text = f"tn: {current_time}"

    def update_lable1(self, current_time):
        self.lable1.text = f"Current Time: {current_time,self.layout.layout3.ids.gapthep.text}"
    def update(self,cli):
        self.lable2.text=str(cli)

if __name__ == '__main__':
    ShotApp().run()
