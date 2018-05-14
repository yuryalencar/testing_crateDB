import os
import time
import random
import string
import matplotlib.pyplot as plt
from crate import client

class ClientDB():

	def start(self):
		
		option = '1'
		while(option != '0'):

			os.system('clear')
			
			print("")
			print("Choose an operation: ")
			print("----------------------------------------------------")
			print("1 - Create table for testing")			
			print("2 - Insert random data and generate the graph")
			print("3 - Select all random data and generate the graph")
			print("4 - Update all random data and generate the graph")
			print("5 - Delete all random data and generate the graph")
			print("6 - Help !")
			print("0 - Exit")
			print("----------------------------------------------------")
			print("")
			option = str(input('Chosen option: '))			
			print("")
						

			if(option == '0'):
				quit()
			elif(option == '6'):

				os.system("clear")
				
				print("")
				print("Require: ")
				print("   SO: Linux")
				print("   Library: Matplotlib")
				print("")
				print("Recommended execution sequence: ")
				print("   Option (1)")
				print("   Option (2)")
				print("   Option (3)")
				print("   Option (4)")
				print("   Option (5)")
				print("")
				raw_input("Press enter to continue ...")
			elif(option == '1'):
				self.start_operation('C')			
			elif(option == '2'):
				self.start_operation('I')
			elif(option == '3'):
				self.start_operation('S')
			elif(option == '4'):
				self.start_operation('U')
			elif(option == '5'):
				self.start_operation('D')
	

	def start_operation(self, operation):
			
		if(operation == 'C'):
			cursor = self.open_connection()
			query = """CREATE TABLE IF NOT EXISTS example_table (first_column STRING, second_column INTEGER)"""
			cursor.execute(query)
			cursor.close()
			print("Create table sucessfully")
		else:
			values = []
			print("")
			values.append(int(input('Enter a value for testing (Value 1 > 1): ')))
			values.append(int(input('Enter other value for testing (Value 2 > 1): ')))
			values.append(int(input('Enter other value for testing (Value 3 > 1): ')))
			values.append(int(input('Enter other value for testing (Value 4 > 1): ')))
			print("")

			values.sort()
			times = []
			graph_title = ""

		
			for i in range(len(values)):

				random_data = self.create_random_data(values[i])
		
				if(operation == 'I'):
					times.append(self.insert_values(random_data))				
					graph_title = "Time Insert - ("+ str(values) +")"
					print("Inserted sucessfully: "+ str(values[i]))

				elif(operation == 'S'):
					times.append(self.select_values(values[i]))				
					graph_title = "Time Select - ("+ str(values) +")"
					print("Selected sucessfully: "+ str(values[i]))

				elif(operation == 'D'):
					self.clearing_database()		
					times.append(self.delete_values(random_data))				
					
					graph_title = "Time Delete - ("+ str(values) +")"
					print("Delected sucessfully: "+ str(values[i]))
					

				elif(operation == 'U'):
					self.clearing_database()		
					times.append(self.update_values(random_data))				
					
					graph_title = "Time Update - ("+ str(values) +")"
					print("Updated sucessfully: "+ str(values[i]))	
		
			self.generate_graph(times, graph_title)			
		raw_input("Press enter to continue ...")

	def update_values(self, random_data):

		query = """UPDATE example_table SET first_column = 'Updated description'"""
		cursor = self.open_connection()
		
		time.sleep(8)
		cursor.execute(query)
		time.sleep(8)
		self.insert_values(random_data)
		time.sleep(8)

		print("Updating Data...")
		time_start = time.time()
		cursor.execute(query)
		time_final = time.time()
		cursor.close()
		
		return time_final - time_start
	
	def clearing_database(self):
		cursor = self.open_connection()
		query = """DELETE FROM example_table"""
		print("Clearing the database...")
		cursor.execute(query)
		cursor.close()


	def delete_values(self, random_data):

		query = """DELETE FROM example_table"""
		cursor = self.open_connection()
		
		time.sleep(8)
		cursor.execute(query)
		time.sleep(8)
		self.insert_values(random_data)
		time.sleep(8)

		print("Deleting Data...")
		time_start = time.time()
		cursor.execute(query)
		time_final = time.time()
		cursor.close()
		
		return time_final - time_start
					

	def insert_values(self, random_data):
		
		cursor = self.open_connection()
		query = """INSERT INTO example_table (first_column, second_column) VALUES (?, ?)"""

		print("Entering Data...")
		time_start = time.time()
		cursor.executemany(query, random_data)
		time_final = time.time()
		cursor.close()
		return time_final - time_start

	def select_values(self, value):
		
		cursor = self.open_connection()
		query = """SELECT * FROM example_table LIMIT """ + str(value)
		print("Selecting Data...")
		time_start = time.time()
		cursor.execute(query)
		time_final = time.time()
		cursor.close
		return time_final - time_start
				
				
	def generate_graph(self, times, title):
		plt.plot(times)
		plt.title(title)
		plt.ylabel("Time in seconds")
		plt.xlabel("Amount of operations respectively")
		plt.show()

	def open_connection(self):
		connection = client.connect('http://localhost:4200', username='crate')
		cursor = connection.cursor()
		return cursor


	def create_random_data(self, value):
		
		random_data = []
		for i in range(value):
			single_data = []
			single_data.append(''.join(random.choice(string.ascii_uppercase) for y in range(5)))
			single_data.append(random.randrange(0,100))
			random_data.append(tuple(single_data))
		
		return random_data
		


client_db = ClientDB()
client_db.start()
