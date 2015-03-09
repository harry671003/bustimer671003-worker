import json
def error(message):
	data = {
		"status": "error",
		"message": message
	}
	return json.dumps(data)

# Return success json
def success():
	data = {
		"status": "success"
	}
	return json.dumps(data)
