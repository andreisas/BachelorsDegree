class TransitionClass:
	def __init__(self, name, cond, src, dest):
		self.name = name
		self.cond = cond
		self.src = src
		self.dest = dest

	def toString(self):
		return "%s %s %s %s" % (self.name, self.cond, self.src.toString(), self.dest.toString())