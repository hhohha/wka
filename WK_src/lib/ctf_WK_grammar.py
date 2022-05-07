#!/usr/bin/python3

from itertools import combinations
from typing import Dict, List, Tuple, Set, Union, Optional, TypeVar, Any, Callable
from queue import PriorityQueue
from copy import deepcopy
import time
import re
import threading

DEBUG = 0
def debug(s):
	if DEBUG:
		print(s)

tNonTerm = str
tTerm = str
tTermLetter = Tuple[List[tTerm], List[tTerm]]
tLetter = TypeVar('tLetter')
tWord = List[tLetter]
tRelation = Tuple[tTerm, tTerm]

t4DInt = Tuple[int, int, int, int]

def hashTerminal(letter: tTermLetter) -> int:
	return hash(str(letter)) # TODO: improve this


def get_all_combinations(l):
	for i in range(len(l) + 1):
		yield from combinations(l, i)

def is_nonterm(letter: tLetter) -> bool:
	return not isinstance(letter, tuple)

def is_term(letter: tLetter) -> bool:
	return isinstance(letter, tuple)

def wordToStr(word: tWord) -> str:
	rs = []
	for symbol in word:
		if is_term(symbol):
			e1 = ''.join(symbol[0]) if len(symbol[0]) > 0 else 'λ'
			e2 = ''.join(symbol[1]) if len(symbol[1]) > 0 else 'λ'
			rs.append(e1 + '/' + e2)
		else:
			rs.append(symbol)

	return(f'{" ".join(rs)}')

class cTreeNode:
	def __init__(self, word: tWord, upperStrLen: int, lowerStrLen: int, ntLen: int, parent: Optional['cTreeNode'], precedence: int) -> None:
		self.word = word
		self.upperStrLen = upperStrLen
		self.lowerStrLen = lowerStrLen
		self.ntLen = ntLen
		self.parent = parent
		self.hashNo = hash(str(word))
		self.precedence = precedence

	def __hash__(self) -> int:
		return self.hashNo

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, cTreeNode):
			return NotImplemented
		return self.hashNo == other.hashNo # TODO - check if this shouldn't be self.precedence

	def __lt__(self, other: 'cTreeNode') -> bool:
		return self.precedence < other.precedence

class cRule:
	#makes rules compact: A -> (a lambda)(lambda a) == A -> (a a)
	def compactize(self, word: tWord) -> tWord:
		i = 0
		while i < len(word) - 1:
			syllable1 = word[i]
			syllable2 = word[i+1]
			if is_term(syllable1) and is_term(syllable2):
				newSyllable = (syllable1[0] + syllable2[0], syllable1[1] + syllable2[1])
				word[i:i+2] = [newSyllable]
			else:
				i += 1
		return word

	def __init__(self, lhs: tNonTerm, rhs: tWord) -> None:
		self.lhs = lhs
		self.rhs = self.compactize(rhs)
		self.ntsLen = 0
		self.upperCnt = 0
		self.lowerCnt = 0

		self.calculate_cnts()

	def calculate_cnts(self):
		self.ntsLen = 0
		self.upperCnt = 0
		self.lowerCnt = 0
		for letter in self.rhs:
			if is_term(letter):
				self.upperCnt += len(letter[0])
				self.lowerCnt += len(letter[1])
			else:
				self.ntsLen += 1


	def __eq__(self, other):
		return self.rhs == other.rhs and self.lhs == other.lhs

	def __str__(self) -> str:
		return f'{self.lhs} -> {wordToStr(self.rhs)}'

	__repr__ = __str__

	def __hash__(self) -> int:
		return hash((self.lhs, str(self.rhs)))


class cWK_CFG:
	def __init__(self, nts: List[tNonTerm], ts: List[tTerm], startSymbol: tNonTerm, rules: List[cRule], relation: List[tRelation]) -> None:
		self.nts = set(nts)
		self.ts = set(ts)
		self.startSymbol = startSymbol
		self.rules = set(rules)
		self.relation = set(relation)
		self.erasableNts: Set[tNonTerm] = set()
		self.lastCreatedNonTerm = 0
		self.timeLimit = 10
		self.pruneCnts: Dict[Callable, int] = {
			self.prune_check_strands_len: 0,
			self.prune_check_total_len: 0,
			self.prune_check_word_start: 0,
			self.prune_check_relation: 0,
			self.prune_check_regex: 0,
			#self.prune_check_lower_regex: 0
		}

		self.pruningOptions: Dict[Callable, bool] = {
			self.prune_check_strands_len: True,
			self.prune_check_total_len: True,
			self.prune_check_word_start: True,
			self.prune_check_relation: True,
			self.prune_check_regex: True,
			#self.prune_check_lower_regex: True
		}

		self.currentNodePrecedence = 6
		self.nodePrecedenceList = [
			('NTA', self.compute_distance_NTA),
			('WNTA', self.compute_distance_WNTA),
			('TM1', self.compute_distance_TM1),
			('TM2', self.compute_distance_TM2),
			('TM3', self.compute_distance_TM3),
			('NTA+TM1', self.compute_distance_NTA_TM1),
			('NTA+TM2', self.compute_distance_NTA_TM2),
			('NTA+TM3', self.compute_distance_NTA_TM3),
			('WNTA+TM1', self.compute_distance_WNTA_TM1),
			('WNTA+TM2', self.compute_distance_WNTA_TM2),
			('WNTA+TM3', self.compute_distance_WNTA_TM3),
			('no heuristic', self.compute_distance_no_heuristic)
		]

		if not self.is_consistent():
			raise ValueError

		self.generate_rule_dict()
		self.generate_relation_dict()
		self.find_erasable_nts()
		self.calc_nt_distances()
		self.calc_min_terms_from_nt()
		self.calc_rules_nt_lens()

	def generate_relation_dict(self) -> None:
		self.relDict: Dict[tTerm, str] = {}
		for t in self.ts:
			self.relDict[t] = ''

		for a, b in self.relation:
			self.relDict[a] += b

	def calc_rules_nt_lens(self) -> None:
		for rule in self.rules:
			rule.ntsLen = -self.termsFromNts[rule.lhs]
			for letter in rule.rhs:
				if is_nonterm(letter):
					rule.ntsLen += self.termsFromNts[letter]

	def restore(self) -> None:
		self.rules = self.rulesBackup
		self.nts = self.ntsBackup
		self.ts = self.tsBackup
		self.generate_rule_dict()
		self.calc_nt_distances()
		self.calc_min_terms_from_nt()
		self.find_erasable_nts()

	def backup(self) -> None:
		self.rulesBackup = deepcopy(self.rules)
		self.ntsBackup = self.nts.copy()
		self.tsBackup = self.ts.copy()

	def calc_word_distance(self, word: tWord) -> int:
		maxVal = 0
		for letter in word:
			if is_nonterm(letter):
				maxVal = max(maxVal, self.ntDistances[letter])
		return maxVal

	def calc_nt_distances(self) -> None:
		MAX_DIST = 20
		self.ntDistances: Dict[tNonTerm, int] = {}
		for nt in self.nts:
			self.ntDistances[nt] = MAX_DIST

		loop = True
		while loop:
			loop = False
			for rule in self.rules:
				d = self.calc_word_distance(rule.rhs) + 1
				if d < self.ntDistances[rule.lhs]:
					self.ntDistances[rule.lhs] = d
					loop = True

	def calc_terms_cnt(self, word: tWord) -> int:
		retVal = 0
		for letter in word:
			if is_term(letter):
				retVal += len(letter[0]) + len(letter[1])
			else:
				retVal += self.termsFromNts[letter]
		return retVal

	def calc_min_terms_from_nt(self):
		MAX_TERMS = 20
		self.termsFromNts: Dict[tNonTerm, int] = {}
		for nt in self.nts:
			self.termsFromNts[nt] = MAX_TERMS

		loop = True
		while loop:
			loop = False
			for rule in self.rules:
				d = self.calc_terms_cnt(rule.rhs)
				if d < self.termsFromNts[rule.lhs]:
					self.termsFromNts[rule.lhs] = d
					loop = True


	def compute_distance(self, word: tWord, goalStr: str) -> int:
		return self.nodePrecedenceList[self.currentNodePrecedence][1](word, goalStr)


	def compute_distance_no_heuristic(self, word: tWord, goal: str) -> int:
		return 0


	def compute_distance_NTA(self, word: tWord, goal: str) -> int:
		distance = 0
		for letter in word:
			if is_nonterm(letter):
				distance += 1
		return distance

	def compute_distance_WNTA(self, word: tWord, goal: str) -> int:
		distance = 0
		for letter in word:
			if is_nonterm(letter):
				distance += self.ntDistances[letter]
		return distance


	# look only at terminals with some upper strands
	# if symbol in upper strand match goal -> priority increases
	# once you find one that doesn't, finish
	def compute_distance_TM1(self, word: tWord, goal: str) -> int:
		goalIdx, distance = 0, 0

		for letter in word:
			if is_term(letter):
				for symbol in letter[0]:
					if len(goal) > goalIdx and symbol == goal[goalIdx]:
						distance -= 1
						goalIdx += 1
					else:
						return distance
		return distance


	# look at terminals with some upper strands only
	# if symbol in upper strand match goal -> priority increases
	# but unlike previous case, if you find one that doesn't match input, just descrease priority and continue
	def compute_distance_TM2(self, word: tWord, goal: str) -> int:
		goalIdx, distance = 0, 0

		for letter in word:
			if is_term(letter):
				for symbol in letter[0]:
					if len(goal) > goalIdx and symbol == goal[goalIdx]:
						distance -= 1
						goalIdx += 1
					else:
						distance += 1
						goalIdx += 1
		return distance

	# look at first letter
	# if it is terminal and has upper strand - check how it matches goal - increase priority
	# else do nothing
	def compute_distance_TM3(self, word: tWord, goal: str) -> int:
		goalIdx, distance = 0, 0

		if len(word) > 0 and is_term(word[0]):
			for symbol in word[0][0]:
				if len(goal) > goalIdx and symbol == goal[goalIdx]:
					distance -= 1
					goalIdx += 1
				else:
					return distance
		return distance
	#
	def compute_distance_NTA_TM3(self, word: tWord, goal: str) -> int:
		goalIdx, distance = 0, 0

		for letter in word:
			if is_nonterm(letter):
				distance += 1

		if len(word) > 0 and is_term(word[0]):
			for symbol in word[0][0]:
				if len(goal) > goalIdx and symbol == goal[goalIdx]:
					distance -= 10
					goalIdx += 1
				else:
					return distance
		return distance

	# 2+5
	def compute_distance_WNTA_TM3(self, word: tWord, goal: str) -> int:
		goalIdx, distance = 0, 0

		for letter in word:
			if is_nonterm(letter):
				distance += self.ntDistances[letter]

		if len(word) > 0 and is_term(word[0]):
			for symbol in word[0][0]:
				if len(goal) > goalIdx and symbol == goal[goalIdx]:
					distance -= 10
					goalIdx += 1
				else:
					return distance
		return distance


	# combination of previous heuristic and nt aversion
	def compute_distance_NTA_TM2(self, word: tWord, goal: str) -> int:
		goalIdx, distance = 0, 0

		for letter in word:
			if is_term(letter):
				for symbol in letter[0]:
					if len(goal) > goalIdx and symbol == goal[goalIdx]:
						distance -= 10
						goalIdx += 1
					else:
						distance += 10
						goalIdx += 1

			else:
				distance += 1
		return distance

	def compute_distance_WNTA_TM2(self, word: tWord, goal: str) -> int:
		goalIdx, distance = 0, 0

		for letter in word:
			if is_term(letter):
				for symbol in letter[0]:
					if len(goal) > goalIdx and symbol == goal[goalIdx]:
						distance -= 10
						goalIdx += 1
					else:
						distance += 10
						goalIdx += 1

			else:
				distance += self.ntDistances[letter]
		return distance


	def compute_distance_NTA_TM1(self, word: tWord, goal: str) -> int:
		goalIdx, distance = 0, 0

		for letter in word:
			if is_term(letter):
				for symbol in letter[0]:
					if len(goal) > goalIdx and symbol == goal[goalIdx]:
						distance -= 10
						goalIdx += 1
					else:
						return distance

			else:
				distance += 1
		return distance

	def compute_distance_WNTA_TM1(self, word: tWord, goal: str) -> int:
		goalIdx, distance = 0, 0

		for letter in word:
			if is_term(letter):
				for symbol in letter[0]:
					if len(goal) > goalIdx and symbol == goal[goalIdx]:
						distance -= 10
						goalIdx += 1
					else:
						return distance

			else:
				distance += self.ntDistances[letter]
		return distance

	def find_erasable_nts(self) -> None:
		self.erasableNts = set()
		loop = True
		while loop:
			loop = False
			for rule in self.rules:
				if self.is_word_erasable(rule.rhs) and rule.lhs not in self.erasableNts:
					loop = True
					self.erasableNts.add(rule.lhs)


	def generate_rule_dict(self) -> None:
		self.ruleDict: Dict[tNonTerm, List[cRule]] = {}
		for nt in self.nts:
			self.ruleDict[nt] = []
		for rule in self.rules:
			self.ruleDict[rule.lhs].append(rule)


	def remove_lambda_rules(self) -> None:
		newRules: Set[cRule] = set()

		for rule in self.rules:
			erasableIdxs: List[int] = []
			for idx, letter in enumerate(rule.rhs):
				if is_nonterm(letter) and letter in self.erasableNts:
					erasableIdxs.append(idx)

			for idxLst in get_all_combinations(erasableIdxs):
				newRuleRhs = []
				for idx, letter in enumerate(rule.rhs):
					if idx not in erasableIdxs or idx in idxLst:
						newRuleRhs.append(deepcopy(letter))

				newRule = cRule(rule.lhs, newRuleRhs)
				if newRule.rhs != [([], [])] and newRule.rhs != [] and newRule not in newRules:
					newRules.add(newRule)

		self.rules = newRules
		self.generate_rule_dict()


	def remove_unit_rules(self) -> None:

		simpleRules: Dict[tNonTerm, List[tNonTerm]] = {}
		for nt in self.nts:
			simpleRules[nt] = [nt]

		loop = True
		while loop:
			loop = False
			for rule in self.rules:
				if len(rule.rhs) == 1 and is_nonterm(rule.rhs[0]) and rule.lhs != rule.rhs:
					# find all non terminals which have lhs in their N but no rhs
					for k, v in simpleRules.items():
						if rule.lhs in v and rule.rhs[0] not in v:
							simpleRules[k].append(rule.rhs[0])
							loop = True

		newRules: Set[cRule] = set()
		for rule in self.rules:
			if len(rule.rhs) != 1 or is_term(rule.rhs[0]):
				for k, v in simpleRules.items():
					if rule.lhs in v:
						newRules.add(cRule(k, deepcopy(rule.rhs)))

		self.rules = newRules
		self.generate_rule_dict()


	def remove_unterminatable_symbols(self) -> None:
		non_empty_nts: Set[tNonTerm] = set()

		loop = True
		while loop:
			loop = False
			for rule in self.rules:
				if len(list(filter(lambda letter: is_nonterm(letter) and letter not in non_empty_nts, rule.rhs))) == 0:
					if rule.lhs not in non_empty_nts:
						non_empty_nts.add(rule.lhs)
						loop = True


		newRules: Set[cRule] = set()
		for rule in self.rules:
			if rule.lhs in non_empty_nts and all(map(lambda letter: is_term(letter) or letter in non_empty_nts, rule.rhs)):
				newRules.add(rule)

		self.nts = self.nts.intersection(non_empty_nts)
		self.rules = newRules
		self.generate_rule_dict()


	def remove_unreachable_symbols(self) -> None:
		reachableNts: Set[tNonTerm] = set(self.startSymbol)
		reachableTs: Set[tTerm] = set()

		loop = True
		while loop:
			loop = False
			for rule in self.rules:
				if rule.lhs in reachableNts:
					for letter in rule.rhs:
						if is_nonterm(letter):
							if letter not in reachableNts:
								reachableNts.add(letter)
								loop = True
						else:
							for terminal in letter[0] + letter[1]:
								if terminal not in reachableTs:
									reachableTs.add(terminal)
									loop = True

		newRules: Set[cRule] = set()
		for rule in self.rules:
			if rule not in newRules and rule.lhs in reachableNts and all(map(lambda letter: is_term(letter) or letter in reachableNts, rule.rhs)):
				newRules.add(rule)

		self.nts = self.nts.intersection(reachableNts)
		self.ts = self.ts.intersection(reachableTs)
		self.rules = newRules
		self.generate_rule_dict()



	def dismantle_rule(self, rule: cRule) -> List[cRule]:
		newRules: List[cRule] = []

		for idx, letter in enumerate(rule.rhs):
			if is_term(letter):
				newNt = self.createNewNt()
				newRules.append(cRule(newNt, [letter]))
				rule.rhs[idx] = newNt
				self.nts.add(newNt)

		currentNt: tNonTerm = rule.lhs

		while len(rule.rhs) > 2:
			newNt = self.createNewNt()
			self.nts.add(newNt)
			newRules.append(cRule(currentNt, [rule.rhs.pop(0), newNt]))
			currentNt = newNt

		newRules.append(cRule(currentNt, rule.rhs))
		return newRules

	def pop_term_from_letter(self, letter: tTermLetter) -> tTermLetter:
		if len(letter[0]) > len(letter[1]):
			t = letter[0].pop(0)
			return ([t], [])
		else:
			t = letter[1].pop(0)
			return ([], [t])

	def printDebug(self):
		print('rules:')
		for rule in self.rules:
			print('   ', rule)
		#print('ts: ', self.nts)
		#print('nts', self.ts)

	def dismantle_term_letters(self) -> None:
		newRules: List[cRule] = []

		for rule in self.rules:
			if len(rule.rhs) == 1 and is_term(rule.rhs[0]) and len(rule.rhs[0][0]) + len(rule.rhs[0][1]) == 1:
				continue
			for idx, letter in enumerate(rule.rhs):
				if is_term(letter):
					newNt = self.createNewNt()
					self.nts.add(newNt)
					rule.rhs[idx] = newNt

					if len(rule.rhs) == 1:
						rule.rhs.insert(0, self.pop_term_from_letter(letter))

					currentNt = newNt
					while len(letter[0]) + len(letter[1]) > 1:
						t = self.pop_term_from_letter(letter)
						newNt = self.createNewNt()
						self.nts.add(newNt)
						newRules.append(cRule(currentNt, [t, newNt]))
						currentNt = newNt

					newRules.append(cRule(currentNt, [letter]))
			rule.calculate_cnts()

		self.rules.update(newRules)
		self.generate_rule_dict()

	def transform_to_wk_cnf_form(self) -> None:
		newRules: Set[cRule] = set()

		for rule in self.rules:
			if len(rule.rhs) == 1 and is_term(rule.rhs[0]) or len(rule.rhs) == 2 and is_nonterm(rule.rhs[0]) and is_nonterm(rule.rhs[1]):
				newRules.add(rule)

			# swap terminal letters for respective non-terminals and break down words longer than 2
			elif len(rule.rhs) >= 2:
				newRules.update(self.dismantle_rule(rule))

		self.rules = newRules
		self.generate_rule_dict()

	def to_wk_cnf(self) -> None:
		#print('\nSTART    -----------------------------')
		#self.printDebug()
		#print('--------------------------------------')

		self.remove_lambda_rules()

		#print('\nLAMBDA RULES REMOVED  --------------')
		#self.printDebug()
		#print('--------------------------------------')

		self.remove_unit_rules()

		#print('\nUNIT RULES REMOVED  ----------------')
		#self.printDebug()
		#print('--------------------------------------')

		self.remove_unterminatable_symbols()

		#print('\nUSELESS RULES REMOVED  -------------')
		#self.printDebug()
		#print('--------------------------------------')

		self.remove_unreachable_symbols()

		#print('\nUNRCH SYMBS REMOVED  ---------------')
		#self.printDebug()
		#print('--------------------------------------')

		self.dismantle_term_letters()

		#print('\nTERMS DISMANLETED  -----------------')
		#self.printDebug()
		#print('--------------------------------------')

		self.transform_to_wk_cnf_form()

		#print('\nDONE  ------------------------------')
		#self.printDebug()
		#print('--------------------------------------')

		# possible TODO - optimize terminal covering non-terms

		self.calc_nt_distances()
		self.calc_min_terms_from_nt()
		self.erasableNts.clear()
		self.calc_rules_nt_lens()


	def addToX(self, idx: t4DInt, nt: tNonTerm) -> None:
		if idx not in self.X:
			self.X[idx] = []

		self.X[idx].append(nt)


	def checkRules(self, idx1: t4DInt, idx2: t4DInt, target: t4DInt) -> None:
		if idx1 not in self.X or idx2 not in self.X:
			return
		for rule in self.rules:
			if rule.rhs[0] in self.X[idx1] and rule.rhs[1] in self.X[idx2]:
				self.addToX(target, rule.lhs)

	def computeSet(self, i: int, j: int, k: int ,l: int) -> None:
		if i == 0 and j == 0:
			for t in range(k, l):
				self.checkRules((0, 0, k, t), (0, 0 ,t+1, l), (i, j, k, l))

		elif k == 0 and l == 0:
			for s in range(i, j):
				self.checkRules((i, s, 0, 0), (s+1, j ,0 , 0), (i, j, k, l))

		else:
			self.checkRules((i, j, 0, 0), (0, 0, k, l), (i, j, k, l))
			self.checkRules((0, 0, k, l), (i, j, 0, 0), (i, j, k, l))

			for s in range(i, j):
				for t in range(k, l):
					self.checkRules((i, s, k, t), (s+1, j, t+1, l), (i, j, k, l))

			for s in range(i, j):
				self.checkRules((i, s, k, l), (s+1, j, 0, 0), (i, j, k, l))
				self.checkRules((i, s, 0, 0), (s+1, j, k, l), (i, j, k, l))

			for t in range(k, l):
				self.checkRules((i, j, k, t), (0, 0, t+1, l), (i, j, k, l))
				self.checkRules((0, 0, k, t), (i, j, t+1, l), (i, j, k, l))


	def run_wk_cyk(self, goalStr: str) -> Optional[bool]:
		start_time = time.time()
		n = len(goalStr)
		self.X: Dict[t4DInt, List[tNonTerm]] = {}

		for i, word in enumerate(goalStr):
			current_time = time.time()
			if current_time - start_time > self.timeLimit:
				return None

			for rule in self.rules:
				if len(rule.rhs) == 1 and is_term(rule.rhs[0]):
					letter = rule.rhs[0]
					if len(letter[0]) == 1 and letter[0][0] == word:
						self.addToX((i+1, i+1, 0, 0), rule.lhs)
					elif len(letter[1]) == 1 and letter[1][0] == word:
						self.addToX((0, 0, i+1, i+1), rule.lhs)

		#print('*********************************************')
		#print(self.X)
		#print('*********************************************')

		for y in range(2, 2*n+1):
			current_time = time.time()
			if current_time - start_time > self.timeLimit:
				return None

			for beta in range(max(y - n, 0), min(n, y)+1):
			#for beta in range(0, n+1):
				alpha = y - beta

				if alpha == 0:
					i = j = 0
					for k in range(1, n-y+2):
						l = k + y - 1
						self.computeSet(i, j, k, l)

				elif beta == 0:
					k = l = 0
					for i in range(1, n - y + 2):
						j = i + y - 1
						self.computeSet(i, j, k, l)

				else:
					for i in range(1, n - alpha + 2):
						for k in range(1, n - beta + 2):
							j = i + alpha - 1
							l = k + beta - 1
							self.computeSet(i, j, k, l)

		return (1, n, 1, n) in self.X and self.startSymbol in self.X[(1, n, 1, n)]


	def createNewNt(self, prefix: str = 'N') -> tNonTerm:
		self.lastCreatedNonTerm += 1
		while prefix + str(self.lastCreatedNonTerm) in self.nts:
			self.lastCreatedNonTerm += 1
		return prefix + str(self.lastCreatedNonTerm)


	def is_word_erasable(self, word: tWord) -> bool:
		for letter in word:
			if is_term(letter):
				if letter == ([], []):
					continue
				else:
					return False

			if letter not in self.erasableNts:
				return False

		return True


	def is_consistent(self) -> bool:
		if self.startSymbol not in self.nts:
			print(f'the starting symbol {self.startSymbol} not found among non-terminals')
			return False

		for t in self.ts:
			if t in self.nts:
				print(f'terminal {t} found among non-terminals')
				return False

		for rule in self.rules:
			if rule.lhs not in self.nts:
				print(f'rule left-hand side {rule.lhs} not found among non-terminals')
				return False
			#TODO - finish this
			#for symbol in rule.lhs:
				#if symbol not in self.nts and symbol not in self.ts:
					#return False

		for r in self.relation:
			if r[0] not in self.ts or r[1] not in self.ts:
				print(f'relation {r} is invalid')
				return False

		return True


	def printPath(self, node: cTreeNode) -> None:
		currentNode: Optional[cTreeNode] = node
		while currentNode:
			debug(f' >>> {wordToStr(currentNode.word)}')
			currentNode = currentNode.parent


	def can_generate(self, upperStr: str) -> Tuple[int, int, List[Tuple[str, int]], Optional[bool]]:
		for key in self.pruneCnts:
			self.pruneCnts[key] = 0
		distance = self.compute_distance([self.startSymbol], upperStr)
		initNode = cTreeNode([self.startSymbol], 0, 0, self.termsFromNts[self.startSymbol], None, distance)
		openQueue: Any = PriorityQueue()
		openQueue.put(initNode)
		openQueueLen, openQueueMaxLen = 1, 1
		allStates: Set[int] = set()
		allStates.add(initNode.hashNo)

		startTime = time.time()
		while not openQueue.empty():

			currentTime = time.time()
			if currentTime - startTime > self.timeLimit:
				return openQueueMaxLen, len(allStates), list(map(lambda key: (key.__name__, self.pruneCnts[key]), self.pruneCnts.keys())), None

			currentNode = openQueue.get()
			openQueueLen -= 1
			for nextNode in self.get_all_successors(currentNode, upperStr):
				if self.is_result(nextNode.word, upperStr):
					self.printPath(nextNode)
					return openQueueMaxLen, len(allStates), list(map(lambda key: (key.__name__, self.pruneCnts[key]), self.pruneCnts.keys())), True
				if nextNode.hashNo not in allStates:
					openQueueLen += 1
					openQueueMaxLen = max(openQueueMaxLen, openQueueLen)
					openQueue.put(nextNode)
					allStates.add(nextNode.hashNo)

		return openQueueMaxLen, len(allStates), list(map(lambda key: (key.__name__, self.pruneCnts[key]), self.pruneCnts.keys())), False


	def is_result(self, word: tWord, goal: str) -> bool:
		# word lenght must be 1
		# word must be terminal
		# upper and lower strands must have the same length
		# upper and lower strands must fulfil compl. relation
		# upper strand must equal goal string
		#return False

		if len(word) != 1:
			return False

		if isinstance(word[0], tNonTerm):
			return False

		if len(word[0][0]) != len(word[0][1]):
			return False

		for symbol1, symbol2 in zip(word[0][0], word[0][1]):
			if (symbol1, symbol2) not in self.relation:
				return False

		if ''.join(word[0][0]) != goal:
			return False

		return True


	def word_to_regex(self, word: tWord) -> str:
		if is_nonterm(word[0]):
			regex = ''
		else:
			regex = '^'

		for idx, letter in enumerate(word):
			if is_nonterm(letter) and idx > 0 and is_term(word[idx-1]):
				regex += '.*'
			elif is_term(letter):
				regex += ''.join(letter[0])

		if is_term(word[-1]):
			regex += '$'

		return regex

	#def word_to_regex_lower(self, word: tWord) -> str:
		#if is_nonterm(word[0]):
			#regex = ''
		#else:
			#regex = '^'

		#for idx, letter in enumerate(word):
			#if is_nonterm(letter) and idx > 0 and is_term(word[idx-1]):
				#regex += '.*'
			#elif is_term(letter):
				#for symbol in letter[1]:
					#regex += '[' + self.relDict[symbol] + ']'

		#if is_term(word[-1]):
			#regex += '$'

		#return regex

	def prune_check_strands_len(self, node: cTreeNode, goalStr: str) -> bool:
		return max(node.upperStrLen, node.lowerStrLen) <= len(goalStr)

	def prune_check_total_len(self, node: cTreeNode, goalStr: str) -> bool:
		return node.upperStrLen + node.lowerStrLen + node.ntLen <= 2 * len(goalStr)

	def prune_check_word_start(self, node: cTreeNode, goalStr: str) -> bool:
		return is_nonterm(node.word[0]) or goalStr.startswith(''.join(node.word[0][0]))

	def prune_check_relation(self, node: cTreeNode, goalStr: str) -> bool:
		if is_nonterm(node.word[0]):
			return True
		shorterStrand = min(len(node.word[0][0]), len(node.word[0][1]))
		for idx in range(shorterStrand):
			if (node.word[0][0][idx], node.word[0][1][idx]) not in self.relation:
				return False
		return True

	def prune_check_regex(self, node: cTreeNode, goalStr: str) -> bool:
		regex = self.word_to_regex(node.word)
		return re.compile(regex).search(goalStr) is not None

	def prune_check_lower_regex(self, node: cTreeNode, goalStr: str) -> bool:
		regex = self.word_to_regex_lower(node.word)
		#print(f'   >>>      checking lower regex of {wordToStr(node.word)},   regex: {regex}')
		return re.compile(regex).search(goalStr) is not None

	def is_word_feasible(self, node: cTreeNode, goalStr: str) -> bool:
		for pruningFunc, pruningOptActive in self.pruningOptions.items():
			if pruningOptActive and not pruningFunc(node, goalStr):
				debug(f'not feasible - check failed in {pruningFunc.__name__}')
				self.pruneCnts[pruningFunc] += 1
				return False
		return True

	# TODO - make this a generator
	def get_all_successors(self, node: cTreeNode, goalStr: str) -> List[cTreeNode]:
		retLst: List[cTreeNode] = []
		for ntIdx, symbol in enumerate(node.word):
			if is_nonterm(symbol):
				for rule in self.ruleDict[symbol]:
					newWord = self.apply_rule(node.word, ntIdx, rule.rhs)
					newNode = cTreeNode(newWord, node.upperStrLen + rule.upperCnt, node.lowerStrLen + rule.lowerCnt, node.ntLen + rule.ntsLen, node, 0)
					if self.is_word_feasible(newNode, goalStr):
						newNode.distance = self.compute_distance(newWord, goalStr)
						retLst.append(newNode)
				break
		return retLst


	def apply_rule(self, word: tWord, ntIdx: int, ruleRhs: tWord) -> tWord:
		if DEBUG:
			debug(f'\nword: {wordToStr(word)}')
			debug(f'ntIdx: {ntIdx}')
			debug(f'rule: {word[ntIdx] + " -> " + wordToStr(ruleRhs)}')

		mergePrev = ntIdx > 0 and is_term(word[ntIdx - 1]) # can we merge with the previous terminal
		mergeNext = ntIdx < len(word) - 1 and is_term(word[ntIdx + 1]) # can we merge with the next terminal

		if len(ruleRhs) == 1 and is_term(ruleRhs[0]):    # rule right side is just a terminal pair
			if mergePrev and mergeNext:
				mergedUpper = word[ntIdx - 1][0] + ruleRhs[0][0] + word[ntIdx + 1][0]
				mergedLower = word[ntIdx - 1][1] + ruleRhs[0][1] + word[ntIdx + 1][1]
				retval = word[:ntIdx - 1] + [(mergedUpper, mergedLower)] + word[ntIdx + 2:]

			elif mergePrev:
				mergedUpper = word[ntIdx - 1][0] + ruleRhs[0][0]
				mergedLower = word[ntIdx - 1][1] + ruleRhs[0][1]
				retval = word[:ntIdx - 1] + [(mergedUpper, mergedLower)] + word[ntIdx + 1:]

			elif mergeNext:
				mergedUpper = ruleRhs[0][0] + word[ntIdx + 1][0]
				mergedLower = ruleRhs[0][1] + word[ntIdx + 1][1]
				retval = word[:ntIdx] + [(mergedUpper, mergedLower)] + word[ntIdx + 2:]

			else:
				retval = word[:ntIdx] + [ruleRhs[0]] + word[ntIdx + 1:]
		else:
			mergePrev = mergePrev and is_term(ruleRhs[0])
			mergeNext = mergeNext and is_term(ruleRhs[-1])

			if ntIdx > 0 and mergePrev and mergeNext:
				mergedUpperPrev = word[ntIdx - 1][0] + ruleRhs[0][0]
				mergedLowerPrev = word[ntIdx - 1][1] + ruleRhs[0][1]
				mergedUpperNext = ruleRhs[-1][0] + word[ntIdx + 1][0]
				mergedLowerNext = ruleRhs[-1][1] + word[ntIdx + 1][1]
				retval = word[:ntIdx - 1] + [(mergedUpperPrev, mergedLowerPrev)] + ruleRhs[1:-1] + [(mergedUpperNext, mergedLowerNext)] + word[ntIdx + 2:]
			elif mergePrev:
				mergedUpperPrev = word[ntIdx - 1][0] + ruleRhs[0][0]
				mergedLowerPrev = word[ntIdx - 1][1] + ruleRhs[0][1]
				retval = word[:ntIdx - 1] + [(mergedUpperPrev, mergedLowerPrev)] + ruleRhs[1:] + word[ntIdx + 1:]
			elif mergeNext:
				mergedUpperNext = ruleRhs[-1][0] + word[ntIdx + 1][0]
				mergedLowerNext = ruleRhs[-1][1] + word[ntIdx + 1][1]
				retval = word[:ntIdx] + ruleRhs[:-1] + [(mergedUpperNext, mergedLowerNext)] + word[ntIdx + 2:]
			else:
				retval = word[:ntIdx] + ruleRhs + word[ntIdx + 1:]

		debug(f'result: {wordToStr(retval)}')
		return retval
