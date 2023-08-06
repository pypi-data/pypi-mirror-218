import requests

class Invoice:
	def __init__(self, token=None):
		self.headers = {
			"accept": "application/json",
			"Crypto-Pay-API-Token": token
		}
	def get_status(self, ids):
		responce = requests.get("https://testnet-pay.crypt.bot/api/getInvoices", data = {
				"invoice_ids": ids,
			},
			headers=self.headers).json()
		return responce.get("result").get("items")[0].get("status")