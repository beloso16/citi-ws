import sql_connect
import getpass
# get header of each csv file and compile in one df with a new column file
#get the odd ones out

chs_file_path = ''
passphrase = getpass.getpass("Enter your passphrase: ")
sql_connect.open_ssh_tunnel(passphrase)
sql_connect.server.start()
connection = sql_connect.connect_to_server('citi_db')
print(connection)

#insert chs
sql_connect.execute_query(connection, "LOAD DATA LOCAL INFILE '/Users/faustine/Desktop/trex_tech_exam/citi-ws/downloaded_files/chs_df.csv' INTO TABLE certificate_holders_statement FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS;")

#insert lld
sql_connect.execute_query(connection, "LOAD DATA LOCAL INFILE '/Users/faustine/Desktop/trex_tech_exam/citi-ws/downloaded_files/final_lld_df.csv' INTO TABLE enhanced_loan_level_data FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS;")

#insert ellt
sql_connect.execute_query(connection, "LOAD DATA LOCAL INFILE '/Users/faustine/Desktop/trex_tech_exam/citi-ws/downloaded_files/final_ellt_df.csv' INTO TABLE loan_level_data FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS;")

sql_connect.close_connection(connection)
sql_connect.server.stop()