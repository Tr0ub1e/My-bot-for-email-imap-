from time import sleep
from email_f import Mail_tg
from bot_f import Bot

token = 'bot token'
log_pass = ('login', 'pass')
site_port = ('your site', 'port')

my_bot = Bot(token)
my_mail = Mail_tg(log_pass, site_port)

cmd = my_bot.get_commands()

if cmd == '/idle':

    my_bot.send_message('Папка?\n =>'+'\n=> '.join(my_mail.return_folders()))
    resp = my_bot.get_upt()

    my_bot.send_message('Начинаю слушать почту...')

    my_mail.listening(my_mail.prepare_data(resp['result'][-1]['message']['text']), my_bot, resp)
