class Coords:
	def __init__(self):
		self.__decimal_points = 7
		self.__divisor = 10 ** self.__decimal_points
	# Convert a floating point cordinate
	# to a 7 decimal point integer
	def integerify(self, coord):
		try:
			coord = float(coord)
		except:
			return None

		integral = int(coord) # Get the integral part
		decimal  = str(coord - integral)[2:9] # Get the first 7 digits from decimal
		format_str = '{:<0' + str(self.__decimal_points) + '}'
		return int(str(integral) + format_str.format(decimal)) # Combine both with zeroes in the end

	def floatify(self, coord):
		if type(coord) != int:
			return None
		return float(coord) / float(self.__divisor)