# -*- coding: utf-8 -*-

import tornado
import tornadoredis
from sockjs.tornado import SockJSConnection
import django
from importlib import import_module
from django.conf import settings
import simplejson as simplejson

#старт источников kmike'simplejson
_engine = import_module(settings.SESSION_ENGINE)

def get_session(session_key):
	return _engine.SessionStore(session_key)

def get_user(session):
	class Dummy(object):
		pass

	django_request = Dummy()
	djanfo_request.session = session

	return django.contrib.auth.get_user(django_request)

#конфигуратор подключения к redis (асинхронные запросы)
ORDERS_REDIS_HOST = getattr(settings, 'ORDERS_REDIS_HOST', 'localhost')
ORDERS_REDIS_PORT = getattr(settings, 'ORDERS_REDIS_PORT', 6379)
ORDERS_REDIS_PASSWORD = getattr(settings, 'ORDERS_REDIS_PASSWORD', None)
ORDERS_REDIS_DB = getattr(settings, 'ORDERS_REDIS_DB', None)

unjson = simplejson.loads
json = simplejson.dumps

class Connection(SockJSConnection):
	def __init__(self, *args, **kwargs):
		super(Connection, self).__init__(*args, **kwargs)
		self.listen_redis()

	@tornado.gen.engine
	def listen_redis(self):
		"""
		Вешаем подписчиков на каналы сообщений.
		"""

		self.redis_client = tornadoredis.Client(
			host=ORDERS_REDIS_HOST,
			port=ORDERS_REDIS_PORT,
			password=ORDERS_REDIS_PASSWORD,
			selected_db=ORDERS_REDIS_DB
			)
		self.redis_client.connect()

		yield tornado.gen.Task(self.redis_client.subscribe, [
				'order_lock', #вызывает методы views.py
				'order_done'  #вызывает методы views.py
		])
		self.redis_client.listen(self.on_redis_queue) #при получении сообщения 
		#вызов self.on_redis_queue метод

	def send(self, msg_type, message):
		"""
		Отправка сообщений.
		"""
		return super(Connection, self).send({
			'type': msg_type,
			'data': message,
			})

	def on_open(self, info):
		"""
		Определяем сессию django
		"""
		self.django_session = get_session(info.get_cookie('sessionid').value)
		self.user = get_user(self.django_session)
		self.is_client = self.user.has_perm('order.lock')
		self.is_moder = self.user.has_perm('order.delete')

	def on_message(self):
		"""
		Обязательный метод.
		"""
		pass

	def on_redis_queue(self, message):
		"""
		Обновление в списке заказов
		"""
		if message.kind == "message":
			message_body = unjson(message.body)

			#в зависимости от канала получения распределяем сообщения
			if message.channel == 'order_lock':
				self.on_lock(message_body)

			if message.channel == 'order_done':
				self.on_done(message_body)

	def on_lock(self, message):
		"""
		Заказ закреплен
		"""
		if message['user'] != self.user.pk: #юзеру-источника действия сообщать о нем не нужно
			self.send('lock', message)

	def on_done(self, message):
		"""
		Заказ выполнен
		"""
		if message['user'] != self.user.pk:
			if self.is_client:
				message['action'] = 'hide'
			else:
				message['action'] = 'highlight'
			self.send('done', message)

	def on_close(self):
		"""
		При закрытии соединения отписываемся от сообщений
		"""
		self.redis_client.unsubscribe([
			'order_lock',
			'order_done'
		])
		self.redis_client.disconnect()