import random
import copy

class Player11():

	def __init__(self):
		self.APPROXIMATE_WIN_SCORE = 7
		self.BIG_BOARD_WEIGHT = 23
		self.WIN_SCORE = 10**6
		self.ALPHA_BETA_DEPTH = 3
		self.POSSIBLE_WIN_SEQUENCES = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
		self.stored_score = [0]*8
		self.first = 0
		self.maxxx = 9223372036854775807
		self.seq_to_cell = {0: (0, 1, 2), 1: (3, 4, 5), 2: (6, 7, 8), 3: (0, 3, 6), 4: (1, 4, 7), 5: (2, 5, 8), 6: (0, 4, 8), 7: (2, 4, 6)}
		self.cell_to_seq = { 0:[0,3,6],1:[0,4],2:[0,5,7],3:[1,3],4:[1,4,6,7],5:[1,5],6:[2,3,6],7:[2,4],8:[2,5,6]}
	MAXX = 9223372036854775807


	def move(self, state, temp_block, old_move, flag):
		#print flag
		self.first = 0
		# print str(old_move[0]) +" "+ str(old_move[1])
		if(old_move[0] == -1 and old_move[1] == -1):
			return (3,3)
		acts_res = []
		final_choices = []
		cells = []
		cells = self.get_legal_actions(state,temp_block,old_move,flag)

		if type(cells) == tuple:
			y = []
			y.append(cells)
			cells = y

		if(len(cells) == 1):
			return (cells[0][0], cells[0][1])

		if (len(cells) >= 2):
			self.ALPHA_BETA_DEPTH = 3
		else:
			self.ALPHA_BETA_DEPTH = 3

		for act in cells:
			successor_state = self.generate_successor(state, act, flag)
			acts_res.append((act, self.__min_val_ab(successor_state, self.ALPHA_BETA_DEPTH, temp_block, flag, old_move)))
		_, best_val = max(acts_res, key=lambda x: x[1])
	 	# return random.choice([best_action for best_action, val in acts_res if val == best_val])
		final_choices = [best_action for best_action, val in acts_res if val == best_val]
		# print "Final choices are " + str(final_choices)
		i = final_choices[0]
		x = i[0] - (i[0]%3)
		y = i[1] - (i[1]%3)
		arr = []
		for j in [x,x+1,x+2]:
			for k in [y,y+1,y+2]:
				if state[j][k] == flag:
					arr.append(1)
				elif state[j][k] == self.op(flag):
					arr.append(-1)
				else:
					arr.append(0)
		loc = []
		for i in xrange(len(arr)):
			if arr[i] == 1:
				self.rtup(i,arr,x,y,loc)
		# print "Some extra ones are " + str(loc)
		# print "X and Y of block are " + str(x) + " "+ str(y)
		final_choices = list(set(loc).intersection(set(final_choices)))
		if len(final_choices) == 0:
			return random.choice([best_action for best_action, val in acts_res if val == best_val])
		return random.choice(final_choices)

	def rtup(self, i, arr, sx, sy, x):
		for j in self.POSSIBLE_WIN_SEQUENCES:
			if i in j:
				var = j.index(i)
				for k in xrange(len(j)):
					if k != var:
						if arr[k] == -1:
							break
						elif k == 2:
							for s in xrange(len(j)):
								if s != var:
									v1 = sx + (s/3)
									v2 = sy + (s%3)
									x.append((v1,v2))
		return

	def filter(self, temp_block, flag):
		op = self.op(flag)
		for x in self.POSSIBLE_WIN_SEQUENCES:
			for y in x:
				if temp_block[y] == op:
					self.stored_score[self.POSSIBLE_WIN_SEQUENCES.index(x)] = 0
					break
				elif temp_block[y] == flag:
					self.stored_score[self.POSSIBLE_WIN_SEQUENCES.index(x)] += 1



	def func(self, index, temp_block):

		L = self.seq_to_cell[index]
		for j in L:
			if temp_block[j] == '-':
				return j


	def select(self, blocks_allowed, temp_block):
		if len(blocks_allowed) == 0:
			check = [0, 1, 2, 3, 4, 5, 6, 7]
			check = list(reversed([x for (y,x) in sorted(zip(self.stored_score,check))]))
			for i in check:
				ret = self.func(i, temp_block)
				if ret != None:
					# print "Block available = "+str(ret)
					return ret

		elif len(blocks_allowed) == 1:
			return blocks_allowed[0]

		else:
			max_value = 0
			block = []
			for i in blocks_allowed:
				L = self.cell_to_seq[i]
				for x in L:
					block.append(x)

			index = block[0]
			block = list(set(block))
			for i in block:
				if self.stored_score[i] >= max_value:
					index = i
					max_value = self.stored_score[i]

			L = self.seq_to_cell[index]
			for j in list(set(L).intersection(blocks_allowed)):
				if temp_block[j] == '-':
					return j
			

	def get_legal_actions(self,state,temp_block,old_move,flag):

		for_corner = [0,2,6,8]
		D = { 0:[1,3],1:[0,2],2:[1,5],3:[0,6],4:[4],5:[2,8],6:[3,7],7:[6,8],8:[7,5]}
		index = (old_move[0]%3)*3 + old_move[1]%3

		blocks_allowed = D[index]

		for i in reversed(blocks_allowed):
			if temp_block[i] != '-':
				blocks_allowed.remove(i)
		# print "Stronger cell " + str(index)
		# print "Stronger blocks_allowed " + str(blocks_allowed)

		if self.first == 0:
			self.first = 1
			cells = []
			mv = []
			ball = []
			ball = copy.deepcopy(blocks_allowed)
			if len(ball) == 0:
				for i in xrange(9):
					if temp_block[i] == '-':
						ball.append(i)
			for i in ball:
				var = self.analyze(state,i,flag)
				cells.append(var)
			for i in cells:
				if i != (-1,-1):
					mv.append(i)
			for i in mv:
				if (((i[0]/3)*3) + (i[1]%3)) in for_corner:
					return i
			if len(mv) != 0:			
				return mv[0]
			mv = []
			for i in ball:
				var = self.analyze(state,i,self.op(flag))
				cells.append(var)
			for i in cells:
				if i != (-1,-1):
					mv.append(i)
			for i in mv:
				if (((i[0]/3)*3) + (i[1]%3)) in for_corner:
					return i
			if len(mv) != 0:	
				return mv[0]

		cells = []

		blocks_a = []
		self.stored_score = [0]*8
		self.filter(temp_block, flag)
		blocks_a.append(self.select(blocks_allowed, temp_block))
		cells = self.get_empty_of(state,blocks_a,temp_block)
		# print "Stronger cells all blocks filled "+ str(cells)
		return cells

	def op(self, flag):
		if flag == 'x':
			return 'o'
		else:
			return 'x'

	def __min_val_ab(self,state, depth, temp_block, flag, old_move, alpha=-(MAXX), beta=(MAXX)):	
		if self.terminal_test(state, depth, temp_block):
			return self.__eval_state(state, temp_block, flag)
		val = (self.maxxx)
		for act in self.get_legal_actions(state,temp_block,old_move,flag):
			successor_state = self.generate_successor(state, act, flag)
			val = min(val, self.__max_val_ab(successor_state,  depth - 1, temp_block, flag, old_move, alpha, beta))
			if val <= alpha:
				return val
			beta = min(beta, val)
		return beta

	def __max_val_ab(self,state, depth, temp_block,flag, old_move, alpha=-(MAXX), beta=(MAXX)):
		if self.terminal_test(state, depth, temp_block):
			return self.__eval_state(state, temp_block, flag)
		val = -(self.maxxx)
		for act in self.get_legal_actions(state,temp_block,old_move,flag):
			successor_state = self.generate_successor(state, act, flag)
			val = max(val, self.__min_val_ab(successor_state, depth, temp_block, flag, old_move, alpha, beta))
			if val >= beta:
				return val
			alpha = max(alpha, val)
		return alpha

	def terminal_test(self,state, depth, temp_block):
		if depth==0:
			return True
		a,b =  self.terminal_state_reached(state, temp_block)
		return a

	def generate_successor(self, state, action, flag):
		brd = copy.deepcopy(state)
		brd[action[0]][action[1]] = flag
		return brd

	def __eval_state(self,state, temp_block, flag):
		uttt_board = copy.deepcopy(state)
		mini_board = copy.deepcopy(temp_block)

		if self.get_winner(temp_block) != False:
			free_cells = 0
			for i in xrange(9):
				for j in xrange(9):
					if uttt_board[i][j] == '-':
						free_cells += 1
			return self.WIN_SCORE + free_cells if self.get_winner(temp_block) == flag else -self.WIN_SCORE - free_cells
		
		if self.is_board_full(uttt_board):
			return 0

		board_as_mini = []
		for i in xrange(9):
			board_as_mini.append(temp_block[i])

		ret = self.__assess_miniB(board_as_mini, flag) * self.BIG_BOARD_WEIGHT
		for i in xrange(9):
			if temp_block[i] == '-':
				miniB = self.get_miniBoard(uttt_board,i)
				if '-' in miniB:
					ret += self.__assess_miniB(miniB, flag)
		return ret

	def __assess_miniB(self,miniB, flag):
		if '-' not in miniB:
			return 0
		player_counter = 0
		opponent_counter = 0
		player_str = flag
		opponent_str = self.op(flag)
		miniB_as_list = copy.deepcopy(miniB)
		for seq in self.POSSIBLE_WIN_SEQUENCES:
			filtered_seq = [miniB_as_list[index] for index in seq if miniB_as_list[index] != '-']
			if player_str in filtered_seq:
				if opponent_str in filtered_seq:
					continue
				if len(filtered_seq) > 1:
					player_counter += self.APPROXIMATE_WIN_SCORE
				player_counter += 1
			elif opponent_str in filtered_seq:
				if len(filtered_seq) > 1:
					opponent_counter += self.APPROXIMATE_WIN_SCORE
				opponent_counter += 1
		return player_counter - opponent_counter

	def get_winner(self, block):
		if block[0] == block[1] and block[1] == block[2] and block[1] != '-':
			return block[0]
		elif block[3] == block[4] and block[4] == block[5] and block[4] != '-':
			return block[3]
		elif block[6] == block[7] and block[7] == block[8] and block[7] != '-':
			return block[6]
		elif block[0] == block[3] and block[3] == block[6] and block[3] != '-':
			return block[0]
		elif block[1] == block[4] and block[4] == block[7] and block[4] != '-':
			return block[1]
		elif block[2] == block[5] and block[5] == block[8] and block[5] != '-':
			return block[2]
		elif block[0] == block[4] and block[4] == block[8] and block[4] != '-':
			return block[0]
		elif block[2] == block[4] and block[4] == block[6] and block[4] != '-':
			return block[2]
		else:
			return False

	def is_board_full(self,uttt_board):
		for i in xrange(9):
			if '-' in uttt_board[i]:
				return False
		return True

	def get_miniBoard(self,state,i):
		mini = []
		for x in xrange(3):
			for y in xrange(3):
				mini.append(state[i/3 + x][i%3 + y])
		return mini

	def get_empty_of(self, gameb, blal,block_stat):
		cells = []
		for idb in blal:
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))

		if cells == []:
			for i in range(9):
				for j in range(9):
					no = (i/3)*3
					no += (j/3)
					if gameb[i][j] == '-' and block_stat[no] == '-':
						cells.append((i,j))	
		return cells


	def terminal_state_reached(self,game_board, block_stat):
		
		bs = block_stat
		if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='d') or (bs[3]!='d' and bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='d' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
			#print block_stat
			return True, 'W'

		elif (bs[0]!='d' and bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1]!='d'and bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2]!='d' and bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
			#print block_stat
			return True, 'W'

		elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='d') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='d'):
			#print block_stat
			return True, 'W'

		else:
			smfl = 0
			for i in range(9):
				for j in range(9):
					if game_board[i][j] == '-' and block_stat[(i/3)*3+(j/3)] == '-':
						smfl = 1
						break
			if smfl == 1:
				return False, 'Continue'
			
			else:
	                        point1 = 0
	                        point2 = 0
	                        for i in block_stat:
	                            if i == 'x':
	                                point1+=1
	                            elif i=='o':
	                                point2+=1
				if point1>point2:
					return True, 'P1'
				elif point2>point1:
					return True, 'P2'
				else:
	                                point1 = 0
	                                point2 = 0
	                                for i in range(len(game_board)):
	                                    for j in range(len(game_board[i])):
	                                        if i%3!=1 and j%3!=1:
	                                            if game_board[i][j] == 'x':
	                                                point1+=1
	                                            elif game_board[i][j]=='o':
	                                                point2+=1
				        if point1>point2:
					    return True, 'P1'
				        elif point2>point1:
					    return True, 'P2'
	                                else:
					    return True, 'D'

	def analyze(self, gameb, index, flag):
		id1 = index/3
		id2 = index%3
		tup = []
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				tup.append(gameb[i][j])
			loc = self.free(tup,flag)
			if loc != -1:
				return (i,(id2*3)+loc)
			tup = []
		for j in range(id2*3,id2*3+3):
			for i in range(id1*3,id1*3+3):
				tup.append(gameb[i][j])
			loc = self.free(tup,flag)
			if loc != -1:
				return ((id1*3)+loc,j)
			tup = []
		for i in xrange(3):
			tup.append(gameb[id1*3+i][id2*3+i])
		loc = self.free(tup,flag)
		if loc != -1:
			return (id1*3+loc,id2*3+loc)
		tup = []
		for i in xrange(3):
			tup.append(gameb[id1*3+i][id2*3+2-i])
		loc = self.free(tup,flag)
		if loc != -1:
			return (id1*3+loc,id2*3+2-loc)
		return (-1,-1)

	def free(self, tup,flag):
		if tup[0] == tup[1] and tup[2] == '-' and tup[0] == flag:
			return 2
		elif tup[0] == tup[2] and tup[1] == '-' and tup[0] == flag:
			return 1
		elif tup[1] == tup[2] and tup[0] == '-' and tup[1] == flag:
			return 0
		else:
			return -1