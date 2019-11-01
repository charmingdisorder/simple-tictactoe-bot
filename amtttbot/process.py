"""
Tic tac toe game
"""
import logging

from amtttbot.daemon import Daemon
from amtttbot.game import ATBGame

from telegram.ext import Updater, CommandHandler, InlineQueryHandler, RegexHandler

PROXY_URL = "socks5://139.130.228.72:28842"

class ATBGameProcess(Daemon):
    def __init__(self, pidfile, token):
        super(ATBGameProcess, self).__init__(pidfile)
        self.token = token
        self.log = logging.getLogger('tictactoe')
        self.sessions = {}
        ATBGameProcess.daemon = self

    def process_start(self, update, ctx):
        if update.message.chat_id in self.sessions:
            ctx.bot.send_message(chat_id=update.effective_chat.id, text="Restarting game")
            del self.sessions[update.message.chat_id]

        ctx.bot.send_message(chat_id=update.effective_chat.id, text="Starting new game")
        self.sessions[update.message.chat_id] = ATBGame(ctx, update.effective_chat.id)
        ctx.bot.send_message(chat_id=update.effective_chat.id, text="Your turn!")

    def process_move(self, update, ctx):
        if not update.message.chat_id in self.sessions:
            ctx.bot.send_message(chat_id=update.effective_chat.id, text="There is no game running")
            return

        move = update.message.text.split()

        if self.sessions[update.message.chat_id].move(int(move[0]), int(move[1])) > 0:
            del self.sessions[update.message.chat_id]

    def run(self):
        self.log.info("Initializing")

        updater = Updater(self.token, use_context='True', request_kwargs={
            'proxy_url': PROXY_URL
        })

        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", self.process_start))
        dp.add_handler(RegexHandler(r'^\d+ \d+$', self.process_move))

        updater.start_polling()

        self.log.info("Idling")

        updater.idle()
