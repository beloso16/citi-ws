import mysql.connector
from mysql.connector import Error
from sshtunnel import SSHTunnelForwarder
import db_configs

# ssh variables
host = db_configs.host
localhost = db_configs.localhost
ssh_username = db_configs.ssh_username
ssh_private_key = db_configs.ssh_private_key

# database variables
user=db_configs.user
password=db_configs.password

#ssh
def open_ssh_tunnel(passphrase):
	global server
	server = SSHTunnelForwarder(
		(host, 22),
		ssh_username=ssh_username,
		ssh_pkey=ssh_private_key,
				ssh_private_key_password=passphrase,
		remote_bind_address=(localhost, 3306)
	)

def connect_to_server(database):
	connection = None
	try:
	#connects to growsari db server and runs query q on database database
		connection = mysql.connector.connect(host='127.0.0.1',
							port=server.local_bind_port,
							user=user,
							passwd=password,
							db=database)
		print("Connected to " +str(database))
	except Error as err:
		print(f"Error: '{err}'")
	return connection

def execute_query(connection, query, val=None, many=False):
	cursor = connection.cursor()
	try:
		response = cursor.execute(query)
		connection.commit()
		if cursor.lastrowid:
			insertid = cursor.lastrowid
		else:
			insertid = 'none'
	except Error as err:
		print(f"Error: '{err}'")
	return insertid

def read_query(connection, query):
	cursor = connection.cursor()
	result = None
	try:
		cursor.execute(query)
		rows = cursor.fetchall()
		if cursor.rowcount > 0: 
			result = rows
		else:
				result is None
	except Error as err:
		print(f"Error: '{err}'")
	return result		

def close_connection(connection):
	connection.close()