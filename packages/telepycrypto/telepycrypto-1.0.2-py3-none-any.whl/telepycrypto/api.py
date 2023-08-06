import requests
import json
from .exceptions import *

class Client:
	def __init__(self, token: str):	
		self.headers = {
			"accept": "application/json",
			"Crypto-Pay-API-Token": token
		}

	def getme(self, test=False):
		if test == True:
			"""test mode"""
			responce = requests.get("https://testnet-pay.crypt.bot/api/getMe", headers=self.headers).json()
			x = responce.get("error")
			code = x["code"]
			if code == 200:
				return responce
			else:
				raise check_exceptions(code=code)
		elif test == False:
			"""original mode"""
			responce = requests.get("https://pay.crypt.bot/api/getMe", headers=self.headers).json()
			x = responce.get("error")
			code = x["code"]
			if code == 200:
				return responce
			else:
				raise check_exceptions(code=code)
		else:
			pass

	def balance(self, test=False):

		if test == True:
			responce = requests.get("https://testnet-pay.crypt.bot/api/getBalance", headers=self.headers)
			if responce.status_code != 200:
				raise check_exceptions(code=responce.status_code)
			else:
				return responce.json()
		elif test == False:
			responce = requests.get("https://pay.crypt.bot/api/getBalance", headers=self.headers)
			if responce.status_code != 200:
				raise check_exceptions(code=responce.status_code)
			else:
				return responce.json()

	def currencies(self, test=False):

		if test == True:
			responce = requests.get("https://testnet-pay.crypt.bot/api/getCurrencies", headers=self.headers)
			if responce.status_code != 200:
				raise check_exceptions(code=responce.status_code)
			else:
				return responce.json()
		elif test == False:
			responce = requests.get("https://pay.crypt.bot/api/getCurrencies", headers=self.headers)
			if responce.status_code != 200:
				raise check_exceptions(code=responce.status_code)
			else:
				return responce.json()

	def exchange_rates(self, test=False):

		if test == True:
			responce = requests.get("https://testnet-pay.crypt.bot/api/getExchangeRates", headers=self.headers)
			if responce.status_code != 200:
				raise check_exceptions(code=responce.status_code)
			else:
				return responce.json()
		elif test == False:
			responce = requests.get("https://pay.crypt.bot/api/getExchangeRates", headers=self.headers)
			if responce.status_code != 200:
				raise check_exceptions(code=responce.status_code)
			else:
				return responce.json()

	def createinvoice(self, data = None, test=False):
		data_desk = ["description", "hidden_message", "paid_btn_name", "paid_btn_url", "payload", "allow_comments", "allow_anonymous", "expires_in"]
		for i in data_desk:
			try:
				data[i]
			except KeyError:
				if "allow_comments" in i:
					data[i] = True
				elif "allow_anonymous" in i:
					data[i] = True
				elif "expires_in" in i:
					data[i] = 2000
				else:
					data[i] = None

		if test == True:
			responce = requests.get("https://testnet-pay.crypt.bot/api/createInvoice", data={
					"asset": data["crypto"],
					"amount": data["amount"],
					"description": data["description"],
					"hidden_message": data["hidden_message"],
					"paid_btn_name": data["paid_btn_name"],
					"paid_btn_url": data["paid_btn_url"],
					"payload": data["payload"],
					"allow_comments": data["allow_comments"],
					"allow_anonymous": data["allow_anonymous"],
					"expires_in": data["expires_in"]
				},
					headers=self.headers).json()
			return responce
		elif test == False:
			responce = requests.get("https://crypt.bot/api/createInvoice", data={
					"asset": data["crypto"],
					"amount": data["amount"],
					"description": data["description"],
					"hidden_message": data["hidden_message"],
					"paid_btn_name": data["paid_btn_name"],
					"paid_btn_url": data["paid_btn_url"],
					"payload": data["payload"],
					"allow_comments": data["allow_comments"],
					"allow_anonymous": data["allow_anonymous"],
					"expires_in": data["expires_in"]
				},
					headers=self.headers).json()
			return responce
		else:
			pass



	def invoices(self, data = {}, test=True):
		data_desk = ["crypto", "invoice_ids", "status", "offset", "count"]
		for i in data_desk:
			try:
				data[i]
			except KeyError:
				if "crypto" in i:
					data[i] = "USDT"
				elif "invoice_ids" in i:
					data[i] = None
				elif "status" in i:
					data[i] = None
				elif "offset" in i:
					data[i] = 0
				elif "count" in i:
					data[i] = 100
		if test == True:
			responce = requests.get("https://testnet-pay.crypt.bot/api/getInvoices", data = {
					"asset": data["crypto"],
					"invoice_ids": data["invoice_ids"],
					"status": data["status"],
					"offset": data["offset"],
					"count": data["count"]
				},
				headers=self.headers)
			if responce.status_code != 200:
				raise check_exceptions(code=responce.status_code)
			else:
				return responce.json()
		elif test == False:
			responce = requests.get("https://pay.crypt.bot/api/getInvoices", data = {
					"asset": data["crypto"],
					"invoice_ids": data["invoice_ids"],
					"status": data["status"],
					"offset": data["offset"],
					"count": data["count"]
				},headers=self.headers)
			if responce.status_code != 200:
				raise check_exceptions(code=responce.status_code)
			else:
				return responce.json()
