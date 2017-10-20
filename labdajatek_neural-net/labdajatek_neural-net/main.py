import game
import network

specimens = 400
breed = 100
sizes = [44, 10, 3]
generation_num = 50

networks = []

def generate_first():
	for _ in range(0, specimens):
		networks.append(network.Network(sizes))

def add_score():
	for net in networks:
		new_game = game.Game()
		score = new_game.play(net)
		net.add_score(score)

def sort_generation():
	networks.sort(key = lambda network: network.score, reverse = True)

def next_generation():
	new = []
	for i in range(0, breed):
		children = networks[i].breed()
		for child in children:
			new.append(child)

	for i in range(0, specimens):
		networks[i] = new[i]

	print("New generation is ready")

def avg_score():
	sum_score = 0
	for net in networks:
		sum_score = sum_score + net.score
	avg_score = sum_score / float(specimens)
	return avg_score

def run():
	for i in range(0, generation_num):

		if i == 0:
			generate_first()
		else:
			next_generation()

		add_score()
		sort_generation()
		avg = avg_score()
		print("Max score for generation #{0}: {1}".format(i, networks[0].score))
		print("Avg score for generation #{0}: {1}".format(i, avg))

		for k in range(0, len(networks)):

			generation_string = ""
			if i < 10:
				generation_string = "00" + str(i)
			else:
				if i < 100:
					generation_string = "0" + str(i)
				else:
					generation_string = str(i)

			specimen_string = ""
			if k < 10:
				specimen_string = "00" + str(k)
			else:
				if k < 100:
					specimen_string = "0" + str(k)
				else:
					specimen_string = str(k)

			name = "_generation-{0}-specimen-{1}".format(generation_string, specimen_string)
			networks[k].write_to_file(name)
