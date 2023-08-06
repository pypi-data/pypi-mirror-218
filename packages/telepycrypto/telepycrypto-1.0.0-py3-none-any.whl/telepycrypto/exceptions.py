class invalid_code(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class UNAUTH(Exception):
    def __init__(self):
        super().__init__("UNAUTH Error")

def check_exceptions(code=0):
	if code == 401:
		raise UNAUTH()