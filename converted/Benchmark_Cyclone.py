import cyclone.web
from twisted.internet import reactor

import sockjs.cyclone
import time
import webbrowser

class _cyclone_index_handler(cyclone.web._request_handler):
    """ _serve the chat html page """
    def get(self):
        self.render('_static/index.html')


class _cyclone_chat_connection(sockjs.cyclone._sock_js_connection):
    """ _chat sockjs connection """
    participants = set()
    _message_count = 0
    _message_target = 10
    _message_start_time = 0
    _message_stop_time = 0
    _setup_stop_time = 0
    _teardown_start_time = 0
    _summary = ''

    def connection_made(self, info):
        with open('_data/_setup_stop_time.txt', 'a+') as _setup_stop_file:
            self._setup_stop_time = time.time()
            _setup_stop_file.write(str(self._setup_stop_time) + '\n')

        self.participants.add(self)

        with open('_data/_message_start_time.txt', 'a+') as _message_start_file:
            self._message_start_time = time.time()
            _message_start_file.write(str(self._message_start_time) + '\n')


    def message_received(self, message):

        self.broadcast(self.participants, message)
        self._message_count += 1
        if self._message_count == self._message_target:
            self.close()

    def connection_lost(self):

        with open('_data/_message_stop_time.txt', 'a+') as _message_stop_file:
            self._message_stop_time = time.time()
            _message_stop_file.write(str(self._message_stop_time) + '\n')

        # self._summary += '=========================================\n'
        # self._summary += 'cyclone summary\n'
        # self._summary += str(self._message_count)
        # self._summary += ' total messages were sent/received in '
        # self._summary += str(self._message_stop_time - self._message_start_time)
        # self._summary += ' seconds.\n'
        # self._summary += '=========================================\n'

        with open('_data/_teardown_start_time.txt', 'a+') as _teardown_start_file:
            self._teardown_start_time = time.time()
            _teardown_start_file.write(str(self._teardown_start_time) + '\n')

        #print self._summary

        self.participants.remove(self)
        reactor.stop()


def _server_setup(port):

    _cyclone_router = sockjs.cyclone._sock_js_router(_cyclone_chat_connection, '/chat')

    app = cyclone.web._application( [ (r"/", _cyclone_index_handler) ] +
                                   _cyclone_router.urls )
    reactor.listen_tcp(port, app)
    address = 'http://127.0.0.1:' + str(port)
    webbrowser.open_new_tab(address)
    reactor.run()

server_setup(8010)