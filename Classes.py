class Stat:
	def __init__(self, name):
		self.name = name
		self.num_by_year = {}	#attempts per year ex. PA
		self.succ_by_year = {} #successful attempts ex. hit, so
		self.avg_by_year = {}
		self.w_avg = {"RR":0,"RL":0,"LL":0,"LR":0}
		self.w_var = {"RR":0,"RL":0,"LL":0,"LR":0}
		self.uncertainty = {"RR":0,"RL":0,"LL":0,"LR":0}
		self.projection = {"RR":0,"RL":0,"LL":0,"LR":0}
		
class Player:
	def __init__(self,id):
		self.id = id
		self.age = 27
		self.stats = {}
