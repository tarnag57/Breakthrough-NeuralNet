import math
import time
import network
import numpy as np
from graphics import *

class Ball:

	def __init__(self, x, y, game):
		self.x = x
		self.y = y
		self.past_x = x
		self.past_y = y
		self.game = game

		if self.game.graphics:
			self.circ = Circle(Point(int(self.x), int(self.y)), self.game.ball_radius)
			self.circ.setFill('Blue')
			self.circ.draw(self.game.win)

	def move_ball(self, direction, velocity):
		self.past_x = self.x
		self.past_y = self.y
		self.x = self.x + self.game.velocity * math.cos(math.radians(self.game.direction))
		#print("x: {0}, past_x: {1}\n".format(self.x, self.past_x))
		self.y = self.y - self.game.velocity * math.sin(math.radians(self.game.direction))
		#print("y: {0}, past_y: {1}\n".format(self.y, self.past_y))

		if self.game.graphics:
		#move ball on win
			self.circ.move(int(self.x) - int(self.past_x), int(self.y) - int(self.past_y)) 


	def detect_collision(self, tray, squares):
		'''First detects collision with wall'''
		# up-wall
		if self.y - self.game.ball_radius < 0:
			self.game.direction = 360 - self.game.direction

		# left-wall
		if self.x - self.game.ball_radius < 0:
			self.game.direction = 180 - self.game.direction

		# right-wall
		if self.x + self.game.ball_radius > self.game.game_width:
			self.game.direction = 180 - self.game.direction


		'''Second detects collision with tray'''
		if self.y + self.game.ball_radius > tray.y:
			if self.x > tray.x and self.x < tray.x + self.game.tray_width:
				#collision with tray
				centre_delta = tray.x + self.game.tray_width / 2.0
				direction_adjust = int(0.4 / self.game.tray_width * centre_delta)
				self.game.direction = 360 - self.game.direction + direction_adjust

		
		'''Finally detects collision with squares'''
		if self.game.just_started > 0:
			return
		for square in squares:

			#if it's still in game
			if square.live:
					
				#if it was from down or up
				if square.x < self.x and self.x < square.x + self.game.square_width:
							
					#if it was down
					if square.y < self.y + self.game.ball_radius and self.y + self.game.ball_radius < square.y + self.game.square_height:
						square.kill()
						self.game.direction = 360 - self.game.direction

					#if it was up
					if square.y < self.y - self.game.ball_radius and self.y - self.game.ball_radius < square.y + self.game.square_height:
						square.kill()
						self.game.direction = 360 - self.game.direction

				#if it was from right or left
				if square.y < self.y and self.y < square.y + self.game.square_height:
							
					#if it was left
					if square.x < self.x + self.game.ball_radius and self.x + self.game.ball_radius < square.x + self.game.square_width:
						square.kill()
						self.game.direction = 180 - self.game.direction

					#if it was right
					if square.x < self.x - self.game.ball_radius and self.x - self.game.ball_radius < square.x + self.game.square_width:
						square.kill()
						self.game.direction = 180 - self.game.direction


	def has_fallen(self, tray):
		'''Returns wether the ball has fallen down'''		
		if self.y > tray.y:
			if self.x < tray.x or self.x > tray.x + self.game.tray_width:
				return True

		return False


class Tray:

	def __init__(self, x, y, game):
		self.x = x
		self.y = y
		self.past_x = x
		self.past_y = y
		self.game = game

		if self.game.graphics:
			#create rectangle on screen
			self.rect = Rectangle(Point(int(self.x), int(self.y)), Point(int(self.x) + self.game.tray_width, int(self.y) + self.game.tray_height))
			self.rect.setFill('red')
			self.rect.draw(self.game.win)

	def move_tray(self, direction):
				
		#determining the move of tray
		delta = 0
		if direction == 1:
			delta = self.game.traystep
		if direction == -1:
			delta = -self.game.traystep
		if direction == 0:
			delta = 0

		#only have to update x coordinate
		self.past_x = self.x
		self.x = self.x + delta

		#bounce back from the edges
		if self.x < 0:
			self.x = 0
		if self.x + self.game.tray_width > self.game.game_width:
			self.x = self.game.game_width - self.game.tray_width

		#redraw tray
		if self.game.graphics:
			#white_rect = Rectangle(Point(0, int(self.y)), Point(int(self.game.game_width), int(self.y) + self.game.tray_height))
			#white_rect.setFill('white')
			#white_rect.draw(self.game.win)
			self.rect.move(self.x - self.past_x, 0)
			#rect = Rectangle(Point(int(self.x), int(self.y)), Point(int(self.x) + self.game.tray_width, int(self.y) + self.game.tray_height))
			#rect.setFill('red')
			#rect.draw(self.game.win)

class Square:

	def __init__(self, x, y, game):
		self.x = x
		self.y = y
		self.live = True
		self.game = game

		if self.game.graphics:
			self.draw()

	def kill(self):
		self.live = False
		self.game.score = self.game.score + 1

		if self.game.graphics:
			rect = Rectangle(Point(self.x, self.y), Point(self.x + self.game.square_width, self.y + self.game.square_height))
			rect.setFill('white')
			rect.draw(self.game.win)

	def draw(self):
		if self.live:
			rect = Rectangle(Point(self.x, self.y), Point(self.x + self.game.square_width, self.y + self.game.square_height))
			rect.setFill('red')
			rect.draw(self.game.win)	

	def revive(self):
		self.live = True
		if self.game.graphics:
			self.draw()		


class Game:

	def __init__(self):
	
		#super parameters
		self.graphics = True	#toggles wether to use graphics
		self.traystep = 25
		self.wait_time = 0.000

		#super constants
		self.game_height = 587
		self.game_width = 1048

		self.tray_height = 15
		self.tray_width = 150

		self.ball_radius = 6

		self.velocity_first = 2.5
		self.velocity_inc = 0.05

		self.direction_first = 60

		self.square_width = 30
		self.square_height = 30

		self.velocity = self.velocity_first
		self.direction = self.direction_first

		self.score = 0

		self.win = 0

		self.just_started = 3

	def prep_input(self, ball, tray, squares):
		input_array = []
		input_array.append(ball.x)
		input_array.append(ball.y)
		input_array.append(tray.x)
		
		#adding direction of ball
		while self.direction < 0:
			self.direction = self.direction + 360
		while self.direction >= 360:
			self.direction = self.direction - 360
		input_dir = (self.direction - 180) / float(180)
		input_array.append(input_dir)
		
		for square in squares:
			if square.live:
				input_array.append(1)
			else:
				input_array.append(0)
		
		#convert to numpy array
		input_matrix = np.asmatrix(input_array).transpose()
		return input_matrix

	def feedforward(self, net_input, network):
		
		result = network.feedforward(net_input)
		result_array = []
		for element in result:
			result_array.append(element)
		max_place = result_array.index(max(result_array))
		#print("max_place: {0}".format(max_place))

		move = -1
		if max_place == 1:
			move = 0
		if max_place == 2:
			move = 1
		return move


	def play(self, net):

		if self.graphics:
			self.win = GraphWin("GameWin", self.game_width, self.game_height)
			self.win.setBackground('white')

		#starting postions
		tray_x = 50.0
		tray_y = 505.0
		ball_x = 100.0
		ball_y = 490.0

		squares = []

		#starting postions for squares
		for i in range(1, 11):
			for j in range(1, 5):
				squares.append(Square(10 + i*90, j*73 - 23, self))


		#starting game loop
		in_game = True
		ball = Ball(ball_x, ball_y, self)
		tray = Tray(tray_x, tray_y, self)

		it = 0

		total_it = 0

		while in_game:
			ball.move_ball(self.direction, self.velocity)		#moves ball
			ball.detect_collision(tray, squares)				#detects collision with wall, tray and squares; returns the new direction
			if ball.has_fallen(tray):							#checks wether the ball has fallen down
				in_game = False


			if it == 5:
				net_input = self.prep_input(ball, tray, squares)	#prepares input
				output = self.feedforward(net_input, net)			#feedforward; output = 1/0/-1
				tray.move_tray(output)								#moves the tray
				it = 0
			else:
				it = it + 1

			if self.graphics:
				time.sleep(self.wait_time)						#waits some time

			total_it = total_it + 1
			if self.just_started > 0:
				self.just_started = self.just_started - 1

			#check for special cases
			all_dead = True
			for square in squares:
				if square.live:
					all_dead = False

			if all_dead:
				for square in squares:
					square.revive()

			if total_it == 100000:
				in_game = False



		if self.graphics:
			self.win.close()

		return self.score
