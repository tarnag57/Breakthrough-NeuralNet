import game
import network

def test(file_name):
    net = network.network_from_file(file_name)
    new_game = game.Game()
    score = new_game.play(net)
    print("Evaluated score: {0}".format(score))
