from matplotlib.pyplot import table
import requests
import datetime
import time
import csv
import sys
from geopy.geocoders import Nominatim
import re
import math
import os

class ResyBot():
	def __init__(self, res_date, party_size, table_time, venue_id):
		self.headers = {
		'origin': 'https://resy.com',
		'accept-encoding': 'gzip, deflate, br',
		'x-origin': 'https://resy.com',
		'accept-language': 'en-US,en;q=0.9',
		'authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
		'content-type': 'application/x-www-form-urlencoded',
		'accept': 'application/json, text/plain, */*',
		'referer': 'https://resy.com/',
		'authority': 'api.resy.com',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
		}
		self.res_date = res_date
		self.party_size = party_size
		self.table_time = table_time
		self.venue_id = venue_id
		self.open_slots = []
		self.best_table = {}
		self.best_tables = []
	
	def run(self):
		self.login()
		if self.auth_token and self.payment_method_string:
			print(f"Logged in as {self.username}, now looking for best table...")
			self.find_table()
			if self.best_table:
				print(f"Found best table for you as: {self.best_table}, now completing reservation")
	
	def find_table(self, auth_token, venue_id):
		#convert datetime to string
		split_table_time = self.table_time.split(':')
		table_time_hour = int(split_table_time[0])
		table_time_minute = float(int(split_table_time[1])/60)
		dec_table_time = table_time_hour + table_time_minute
		params = (
		('x-resy-auth-token', auth_token),
		('day', self.res_date),
		('lat', '0'),
		('long', '0'),
		('party_size', self.party_size),
		('venue_id', venue_id)
		)
		best_tables = []
		response = requests.get('https://api.resy.com/4/find', headers=self.headers, params=params)
		data = response.json()
		results = data['results']
		if len(results['venues']) > 0:
			open_slots = results['venues'][0]['slots']
			self.open_slots = open_slots
			if len(open_slots) > 0:
				available_times = [(k['date']['start'],datetime.datetime.strptime(k['date']['start'],"%Y-%m-%d %H:%M:00").hour, datetime.datetime.strptime(k['date']['start'],"%Y-%m-%d %H:%M:00").minute) for k in open_slots]

				decimal_available_times = []
				for i in range (0, len(available_times)):
					decimal_available_times.append(available_times[i][1] + available_times[i][2]/60)
				absolute_difference_function = lambda list_value : abs(list_value - dec_table_time)
				decimal_closest_time = min(decimal_available_times, key= absolute_difference_function)
				closest_time = available_times[decimal_available_times.index(decimal_closest_time)][0]
				print("CLOSEST TIME", closest_time)
				best_table = [k for k in open_slots if k['date']['start'] == closest_time][0]
				best_tables = [k for k in open_slots if k['date']['start'] == closest_time][0:2]
				self.best_table = best_table
				self.best_tables = best_tables
				return best_table
			else:
				print(f"No open slots currently found for {self.venue_id} on {self.res_date} for {self.party_size} people")
		else:
			print(f"No restaurants found with ID: {self.venue_id}")
		
		
	
	def make_reservation(self):
	#convert datetime to string
		day = self.res_date
		party_size = self.party_size
		config_id = str(self.best_table["config"]["token"])
		params = (
			('x-resy-auth-token', self.auth_token),
			('config_id', config_id),
			('day', day),
			('party_size', self.party_size)
		)
		details_request = requests.get('https://api.resy.com/3/details', headers=self.headers, params=params)
		details = details_request.json()
		book_token = details['book_token']['value']
		self.headers['x-resy-auth-token'] = self.auth_token
		data = {
		'book_token': book_token,
		'struct_payment_method': self.payment_method_string,
		'source_id': 'resy.com-venue-details'
		}
		
		response = requests.post('https://api.resy.com/3/book', headers=self.headers, data=data)

			


if __name__ == "__main__":
	test_res = ResyBot(
		res_date="2022-07-20",
		party_size="2",
		table_time="9:30",
		venue_id="29967"
	)
	test_res.run()


			


