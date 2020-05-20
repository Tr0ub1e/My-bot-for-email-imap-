from email import *
from imaplib import IMAP4_SSL
from base64 import b64decode
from quopri import decodestring

class Mail_tg():

    def __init__(self, log_pass, site_port):

        try:
            self.log, self.pwd = log_pass
            self.site, self.port = site_port

            self.con = IMAP4_SSL(self.site, self.port)
            self.con.login(self.log, self.pwd)
        except:
            print('Ошибка ввода: проверьте правильность данных')


    def return_folders(self):
        #получаем список папок и выводим их
        #также получаем указание в какую папку нам зайти
        self.folders = set()
        for i in self.con.list()[1]:
            self.folders.add(i.split()[-1].decode('utf-8'))

        return self.folders

    def prepare_data(self, user_folder):
        buf = []

        if not user_folder in self.folders:
            return NameError

        self.con.select(user_folder)

        _, data = self.con.search(None, 'ALL')

        return data[0].split()[-1].decode('utf-8')

    def read_mail(self, id_m):

        mail = message_from_bytes(self.con.fetch(id_m.encode('utf-8'), 'RFC822')[1][0][1])

        #ПОЛЯ СООБЩЕНИЯ
        keys = ['Date', 'From', 'Subject']
        response = []

        for key in keys:

            if mail[key][:9] == '=?UTF-8?B' or mail[key][:9] == '=?utf-8?B':
                response.append(b64decode(mail[key][9:]).decode('utf-8'))

            elif mail[key][:9] == '=?UTF-8?Q' or mail[key][:9] == '=?utf-8?Q':
                response.append(decodestring(mail[key][9:]).decode('utf-8'))
            else:
                response.append(mail[key])

        return response

    def listening(self, buf, bot, resp):

        while True:
            if buf != self.prepare_data(resp['result'][-1]['message']['text']):
                bot.send_message('У вас новое сообщение!')

                for msg in self.read_mail(self.prepare_data(resp['result'][-1]['message']['text'])):
                    bot.send_message(msg)

                buf = self.prepare_data(resp['result'][-1]['message']['text'])
