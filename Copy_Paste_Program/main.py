import tkinter
import socket
import threading
import time
import sys


def set_oth_ip():
	# Set IP for connected computer
	global where_to_send
	ip = oth_ip_addr.get()
	print("SET_IP:",ip)
	ip_expl = ip.split(":")
	port = ip_expl[1]
	loc = ip_expl[0]
	try:
		p = socket.gethostbyaddr(loc)
		where_to_send = "{0}:{1}".format(loc, port)
	except socket.error:
		oth_ip_addr.set("FAILED")
	

def set_my_ip():
	# Set IP to listen on
	global server
	ip = my_ip_addr.get()
	ip_expl = ip.split(":")
	port = int(ip_expl[1])
	my_ip_addr.set("{0}:{1}".format(socket.gethostbyname(h_name), port))
	server.bind((h_name, port))
	print("SERVER BOUND")
	server.listen(2)
	print("SERVER LISTENING")
	c, addr = server.accept()
	while True:
		data = c.recv(1024).decode()
		if not data:
			break
		copy_paste.set(str(data))
	c.close()


def server_launcher():
	global keep_alive
	global t1
	global server
	keep_alive = False
	server.close()
	time.sleep(1)
	t1.join()
	print("REJOINED")
	server = socket.socket()
	keep_alive = True
	t1 = threading.Thread(target = set_my_ip)
	t1.start()


def send():
	client_socket = socket.socket()
	ip = where_to_send.split(":")[0]
	print("IP:",ip)
	port = where_to_send.split(":")[1]
	port = int(port)
	try:
		client_socket.connect((ip, port))
		message = copy_paste.get()
		client_socket.send(message.encode())
		client_socket.close()
	except ConnectionRefusedError:
		copy_paste.set("Connection_Not_Made")


if __name__ == '__main__':
	m = tkinter.Tk()

	my_ip_addr = tkinter.StringVar()
	oth_ip_addr = tkinter.StringVar()
	copy_paste = tkinter.StringVar()

	# Configuration
	h_name = socket.gethostname()
	print(h_name)
	my_addr = socket.gethostbyname(h_name)
	my_port = "5000"
	oth_addr = "10.13.18.8"
	oth_port = "4000"
	where_to_send = "{0}:{1}".format(oth_addr, oth_port)
	where_to_listen = "{0}:{1}".format(my_addr, my_port)

	# Prep for Window
	my_ip_addr.set("{0}:{1}".format(my_addr, my_port))
	oth_ip_addr.set("{0}:{1}".format(oth_addr, oth_port))
	copy_paste.set("")

	# Server Threading
	keep_alive = True
	server = socket.socket()
	t1 = threading.Thread(target = set_my_ip)
	t1.start()

	# Window formatting
	F1 = tkinter.Frame(m)
	F2 = tkinter.Frame(m)
	F3 = tkinter.Frame(m)
	F1.pack(side = tkinter.TOP)
	F2.pack()
	F3.pack(side=tkinter.BOTTOM)
	## CONNECTION
	# LISTENING
	B1 = tkinter.Button(F1, text="LISTENING_ON:", command = server_launcher)
	B1.pack(side=tkinter.LEFT)
	E1 = tkinter.Entry(F1, textvariable=my_ip_addr)
	E1.pack(side=tkinter.RIGHT)
	# SENDING
	B2 = tkinter.Button(F2, text="CONNECTED_TO:", command = set_oth_ip)
	B2.pack(side=tkinter.LEFT)
	E2 = tkinter.Entry(F2, textvariable=oth_ip_addr)
	E2.pack(side = tkinter.RIGHT)
	# SEND/RECEIVE
	L3 = tkinter.Entry(F3, textvariable = copy_paste)
	L3.pack(side=tkinter.LEFT)
	B3 = tkinter.Button(F3, text="SEND", command = send)
	B3.pack(side = tkinter.RIGHT)

	m.mainloop()
	sys.exit(0)