# -*- coding: utf-8 -*-

import tornado
import tornadio2 as tornadio
from sockjs.tornado import SockJSRouter
from django.core.management.base import NoArgsCommand

from mainapp.service import Connection


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        router = SockJSRouter(Connection, '/orders')  # sockjs не захотел работать с корнем :(
        app = tornado.web.Application(router.urls)
        app.listen(8989)
        tornado.ioloop.IOLoop.instance().start()