import random
import string
import hashlib
import uuid

def generate_random_string(length):
	if(length > 512):
		return None

	# Generate the random string
	random_string = ''
	for i in range(0, length):
		random_string += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)

	return random_string

# Generate a new users ID
# Generate a 128 bit stop_id
def generate_stopid(stop_name):
	return hashlib.sha1(
		str(uuid.uuid4()) + generate_random_string(40) + stop_name
	).hexdigest()
