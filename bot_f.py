from time import sleep
import requests as req


class Bot:

    def __init__(self, token):

        self.comands = {'/idle':'Ожидание письма'}
        self.token = token
        self._url = 'https://api.telegram.org/bot'
        self.s = req.Session()
        self.con = self.s.get(self._url+self.token+'/getUpdates')

        self.chat_id = self.con.json()['result'][-1]['message']['chat']['id']
        self.offset = self.con.json()['result'][-1]['update_id']

    def get_upt(self):
        data = {'offset': str(int(self.offset))}
        self.con = self.s.post(self._url+self.token+'/getUpdates', data=data)

        while self.con.json()['result'][-1]['update_id'] == self.offset:
            self.con = self.s.get(self._url+self.token+'/getUpdates')
            sleep(2)

        self.offset = self.con.json()['result'][-1]['update_id']

        return self.con.json()

    def send_message(self, msg):
        data = {'chat_id':self.chat_id, 'text':str(msg)}
        self.con = self.s.post(self._url+self.token+'/sendMessage', data=data)

    def get_commands(self):
        self.send_message('Мои команды')
        for key in self.comands:
            self.send_message('{} => {}'.format(key, self.comands[key]))

        com_resp = self.get_upt()

        while not com_resp['result'][-1]['message']['text'] in self.comands.keys():
            self.send_message('Такой команды нет у меня ((')
            com_resp = self.get_upt()

        else:
            return com_resp['result'][-1]['message']['text']
