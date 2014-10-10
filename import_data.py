import csv
import codecs
import Classes

def get_data(csvfile):
	players = {}
	with codecs.open(csvfile, encoding='utf-8-sig') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			batID = row["Batter_ID"]
			year = int(row["Year"])
			if batID not in players:
				players[batID] = Classes.Player(batID)
				players[batID].stats["SO"] = Classes.Stat("SO")
			so = players[batID].stats["SO"]
			if year not in so.num_by_year:
				so.num_by_year[year] = {}
			if year not in so.succ_by_year:
				so.succ_by_year[year] = {}
			so.num_by_year[year][row["Batter_Hand"]+row["Pitcher_Hand"]] = int(row["NonBuntNonIBBPA"])
			so.succ_by_year[year][row["Batter_Hand"]+row["Pitcher_Hand"]] = int(row["SO"])
	return players
