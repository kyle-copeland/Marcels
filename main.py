import Classes
import import_data
import math

DISQUALIFIED= -1
WEIGHTS = [3,4,5]
YEAR_SCOPE = [2007,2008,2009]

#add up totals from all players
def init_lg_avg_stat(stat,players):
	lg_avg = Classes.Stat(stat)
	for id in players:
		player = players[id]
		p_stat = player.stats[stat]
		for name in {"num_by_year","succ_by_year"}:
			lg_attri = getattr(lg_avg,name)
			p_attri = getattr(p_stat,name)
			for year in p_attri:
				if year not in lg_attri:
					lg_attri[year] = {"RR":0,"RL":0,"LL":0,"LR":0}
				for combination in p_attri[year]:
					lg_attri[year][combination] += int(p_attri[year][combination])
	return lg_avg

def set_avg(stat):
	for year in stat.num_by_year: #Per year
		stat.avg_by_year[year] = {}
		for combination in stat.succ_by_year[year]: #Per Batter/Pitcher Hand Combination
			stat.avg_by_year[year][combination] = stat.succ_by_year[year][combination]/float(stat.num_by_year[year][combination])

def set_w_avg(stat): 
	for combination in {"RR","RL","LL","LR"}:
		for i in range(len(YEAR_SCOPE)):
			year = YEAR_SCOPE[i]
			if year not in stat.avg_by_year: #if no information exists for this player they are excluded from projection
				stat.w_avg[combination] = DISQUALIFIED
				stat.w_var[combination] = DISQUALIFIED
				break
			elif combination not in stat.avg_by_year[year]:
				stat.w_avg[combination] = DISQUALIFIED
				stat.w_var[combination] = DISQUALIFIED
				break
			elif stat.w_avg[combination] != DISQUALIFIED :
				stat.w_avg[combination] += WEIGHTS[i]*stat.avg_by_year[year][combination]
		if stat.w_avg[combination] != DISQUALIFIED:
			stat.w_avg[combination] = stat.w_avg[combination]/float(sum(WEIGHTS))

def set_w_var(stat):
	v1 = sum(WEIGHTS)
	v2 = sum([i**2 for i in WEIGHTS])
	for combination in {"RR","RL","LL","LR"}:
		if stat.w_var[combination] == DISQUALIFIED :
			continue
		for i in range(len(YEAR_SCOPE)):
			year = YEAR_SCOPE[i]
			stat.w_var[combination] +=  WEIGHTS[i]*(stat.avg_by_year[year][combination] - stat.w_avg[combination])**2
		stat.w_var[combination] = stat.w_var[combination]/(v1-(v2/v1)) 
		
def set_uncertainty(stat):
	for combination in {"RR","RL","LL","LR"}:
		N = 0
		if stat.w_var[combination] != DISQUALIFIED:
			for i in range(len(YEAR_SCOPE)):
				year = YEAR_SCOPE[i]
				N += WEIGHTS[i]*stat.num_by_year[year][combination]
			N = N /float(sum(WEIGHTS))
			#print "Player Weighted N Combination:",combination,N
			stat.uncertainty[combination] = math.sqrt(stat.w_var[combination]/N)
			
def set_lg_avg_uncertainty(stat,players):
	N = {}
	num_of_players = {}
	year_avg = {}
	for year in YEAR_SCOPE:
		N[year] = {"RR":0,"RL":0,"LL":0,"LR":0}
		num_of_players[year] = {"RR":0,"RL":0,"LL":0,"LR":0}
		year_avg[year] = {"RR":0,"RL":0,"LL":0,"LR":0}
		for id in players:
			player = players[id]
			if year in player.stats[stat.name].num_by_year:
				for combination in player.stats[stat.name].num_by_year[year]:
					num_of_players[year][combination] += 1
					N[year][combination] += player.stats[stat.name].num_by_year[year][combination]
		for combination in {"RR","RL","LL","LR"}:
			year_avg[year][combination] = N[year][combination]/num_of_players[year][combination]
	
	weighted_N = {"RR":0,"RL":0,"LL":0,"LR":0}
	for combination in {"RR","RL","LL","LR"}:
		for i in range(len(YEAR_SCOPE)):
			year = YEAR_SCOPE[i]
			weighted_N[combination] += WEIGHTS[i]*year_avg[year][combination]
		weighted_N[combination] = weighted_N[combination]/float(sum(WEIGHTS))
		stat.uncertainty[combination] = math.sqrt(stat.w_var[combination]/weighted_N[combination])
		#print "LG_AVG Weighted N Combination:",combination,weighted_N[combination]
		
		
def calc_projection(p_stat,lg_stat):
	for combination in {"LR"}:
		if p_stat.w_avg[combination] != DISQUALIFIED:
			top = (lg_stat.w_avg[combination]/lg_stat.uncertainty[combination]**2) + (p_stat.w_avg[combination]/p_stat.uncertainty[combination]**2)
			bottom = (1/lg_stat.uncertainty[combination]**2) + (1/p_stat.uncertainty[combination]**2)
			p_stat.projection[combination] = top/bottom
			
			
def set_lg_avg_stats(players):
	lg_avg = init_lg_avg_stat("SO",players)
	set_avg(lg_avg)
	set_w_avg(lg_avg)
	set_w_var(lg_avg)
	set_lg_avg_uncertainty(lg_avg,players)
	return lg_avg
	
def init_players():
	players = import_data.get_data("KRates.csv")
	lg_avg = set_lg_avg_stats(players)
	id = "andeg001"
	set_avg(players[id].stats["SO"])
	set_w_avg(players[id].stats["SO"])
	set_w_var(players[id].stats["SO"])
	set_uncertainty(players[id].stats["SO"])
	calc_projection(players[id].stats["SO"],lg_avg)
	print_results(players[id],lg_avg)
def print_results(player,lg_avg):
	print "Projections for:", YEAR_SCOPE[-1] + 1
	for combination in {"RR","RL","LL","LR"}:
		if player.stats[lg_avg.name].projection[combination]:
			#print player.stats[lg_avg.name].projection[combination],combination
			print "Weighted Avg"
			print "League:",lg_avg.w_avg[combination],player.id,":", player.stats[lg_avg.name].w_avg[combination]
def main():
	init_players()

if __name__ == '__main__':
	main()
