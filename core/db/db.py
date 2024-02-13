# DATABASE STRUCTURE
# 
# 
# 										soravurbot_db
#									 		|
#					users	(FK) <–>	transactions	–	usage	 –	referrals
# 				/															\
#																	- refer_id
#		- user_id 													- FK init_user
#		- first_name 												 - FK referred_user
#		- last_name 												- referral_bonus_amount
#		- username 													- timestamp
#		- signup_timestamp 
#		- last_active 
#		- language 
#		- subscription_status 
#		- balance 
#		- number_of_referrals 
#		-  
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
import os
from uuid import uuid4

from sqlalchemy import Engine, ForeignKey, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

class Base(AsyncAttrs, DeclarativeBase):
    pass


class Database:
	
	
	def __init__(self, config):
		self.config = config
		
		
	def load_database(self):
		host = self.config['host']
		port = self.config['port']
		name = self.config['name']
		username = self.config['username']
		password = self.config['password']
		
	
	def create_table_if_not_exists(self, table_name: str):
		pass
		
		
		
	def get_user(self, user_id):
		pass
	
	
	