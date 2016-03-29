# -*- coding: utf-8 -*-

import tornado
import tornadoredis
from sockjs.tornado import SockJSConnection

import django
from importlib import  import_module
from django.conf import settings
import simplejson

_engine = import_module(settings.SESSION_ENGINE).SessionStore

def get_session(session_key):
	return _engine(session_key)

def get_user(session):
	class Dummy(object):
		pass

	django_request = Dummy()
	django_request.session = session

	return django.contrib.auth.get_user(django_request)

ORDERS_REDIS_HOST = getattr(settings, 'ORDERS_REDIS_HOST', 'localhost')
ORDERS_REDIS_PORT = getattr(settings, 'ORDERS_REDIS_PORT', 6379)
ORDERS_REDIS_PASSWORD = getattr(settings, 'ORDERS_REDIS_PASSWORD', None)
ORDERS_REDIS_DB = getattr(settings, 'ORDERS_REDIS_DB', None)

unjson = simplejson.loads
json = simplejson.dumps

class Connection(SockJSConnection):
	def __init__ (self, *args, **kwargs):
		super(Connection, self).__init__(*args, **kwargs)
		self.listen_redis()

	@tornado.gen.engine
	def listen_redis(self):
		self.redis_client = tornadoredis.Client(
			host = ORDERS_REDIS_HOST,
			port = ORDERS_REDIS_PORT,
			password = ORDERS_REDIS_PASSWORD,
			selected_db = ORDERS_REDIS_DB
			)
		self.redis_client.connect()

		yield tornado.gen.Task(self.redis_client.subscribe, [
			'coords_lock',
			'coords_server_lock',
			'order_done',
			'update_unique',
			'show_location'
		])
		self.redis_client.listen(self.on_redis_queue)

	def send(self, msg_type, message):
		return super(Connection, self).send({
			'type': msg_type,
			'data':message,	
		})

	def on_open(self, info):
		self.django_session = get_session(info.get_cookie('sessionid').value)
		self.user = get_user(self.django_session)

	def on_message(self):
		pass

	# message channel redirection
	def on_redis_queue(self, message):
		if message.kind == 'message':
			message_body =  unjson(message.body)
			if message.channel == 'coords_lock':
				self.on_lock(message_body)
			if message.channel == 'coords_server_lock':
				self.on_server_lock(message_body)
			if message.channel == 'order_done':
				self.on_done(message_body)
			if message.channel == 'update_unique':
				self.on_unique(message_body)
			if message.channel == 'show_location':
				self.on_location(message_body)
	#send to user messages
	def on_lock(self, message):
		if message['user'] == self.user.pk:
			self.send('lock', message)

	def on_server_lock(self, message):
		if message['user'] == self.user.pk:
			self.send('server_lock', message)

	def on_unique(self, message):
		if message['user'] == self.user.pk:
			self.send('unique', message)

	def on_location(self, message):
		if message['user'] == self.user.pk:
			self.send('location', message)


	def on_done(self, message):
		if message['user'] != self.user.pk:
			if self.is_client:
				message['action'] = 'hide'
			else:
				message['action'] = 'highlight'
			self.send('done', message)

	def on_close(self):
		self.redis_client.unsubscribe([
			'order_lock',
			'coords_server_lock',
			'order_done'
		])
		self.redis_client.disconnect()