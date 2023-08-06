import websocket
import socket
import json 
from .config import DEBUG, WS_URL
from .handlers import Cmds, Handlers, decodePacket, encodePacket

if DEBUG:
	websocket.enableTrace(True) 

def doConnect():
	def on_message(wsapp, message):
		"""
		接收消息处理函数
		"""
		print(f"on_message, packet: {message}")
		packet = decodePacket(message)
		cmd = packet["cmd"]
		# 根据cmd获取处理器
		handler = Handlers[cmd]
		if handler is None:
			print(f"cmd: {cmd}对应的handler不存在")
		handler(packet, wsapp)
		
	def on_connect(wsapp):
		"""
		连接事件处理函数
		"""
		print(f"on_open")
		#发起第一个指令
		wsapp.send(encodePacket(Cmds["CONNECT_C"]));
		
	wsapp = websocket.WebSocketApp(WS_URL, on_message=on_message, on_open=on_connect)
	wsapp.run_forever() 

if __name__ == "__main__":
	doConnect()

	