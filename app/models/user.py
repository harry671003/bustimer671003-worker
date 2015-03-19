class User:
	def __init__(self, id, clearance):
		self.id = id
		self.clearance = clearance
	def is_authenticated(self):
		return True
	def is_active(self):
		return True
	def is_anonymous(self):
		return False
	# Clearance of a user
	# This is used to set the 
	def get_clearance(self):
		return self.clearance
	def get_id(self):
		try:
			return unicode(self.id)  # python 2
		except NameError:
			return str(self.id)  # python 3
	def __repr__(self):
		return '<User %r>' % (self.id)