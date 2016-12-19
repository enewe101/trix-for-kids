from safe import safe_min, safe_lte
from grouper import trim


def string_distance(s1, s2):
	return SA.string_distance(s1, s2)

def string_align(s1, s2):
	distance, path = SA.string_alignment(s1, s2)
	return distance, path

def string_align_masks(s1, s2):
	mask1, mask2 = SA.get_string_alignment_masks(s1, s2)
	return 

def string_align_path(s1, s2):
	return SA.get_string_alignment_path(s1, s2)

def substring_alignment_score(s1, s2):
	return SA.substring_alignment_score(s1, s2)

class StringAligner(object):

	UP = 1
	LEFT = 2
	DIAG = 3

	DELETE = 'd'
	INSERT = 'i'
	MATCH = 'm'
	SUBSTITUTE = 's'

	def string_alignment(self, name1, name2, substring_mode=False):
		distance = [
			[None for j in range(len(name2)+1)] for i in range(len(name1)+1)
		]
		path = [
			[None for j in range(len(name2)+1)] for i in range(len(name1)+1)
		]

		for i in range(len(name1) + 1):
			for j in range(len(name2) + 1):

				# The word boundary matches
				if i == 0 and j == 0:
					distance[i][j] = 0
					path[i][j] = self.DIAG
					continue

				# match character i and j
				match_dist = None
				if i > 0 and j > 0:
					if name1[i-1] == name2[j-1]:
						match_dist = distance[i-1][j-1]

					# substitute character i by char j
					else:
						match_dist = distance[i-1][j-1] + 2

				# Delete one char from name1
				del_dist = None
				if i > 0:

					# In substring mode, leading and trailing deletions
					# from name1 are penalty-free
					if substring_mode and (j == 0 or j == len(name2)):
						del_dist = distance[i-1][j]

					# Otherwise the deletion penalty of 1 is applied
					else:
						del_dist = distance[i-1][j] + 1

				# Insert one char from name2
				insert_dist = None
				if j > 0:
					insert_dist = distance[i][j-1] + 1

				distance[i][j] = safe_min(
					match_dist, del_dist, insert_dist)

				if safe_lte(match_dist, del_dist):
					if safe_lte(match_dist, insert_dist):
						path[i][j] = self.DIAG
					else:
						path[i][j] = self.LEFT

				elif safe_lte(del_dist, insert_dist):
					path[i][j] = self.UP

				else:
					path[i][j] = self.LEFT

		return distance, path


	def substring_alignment_score(self, reference_string, substring):
		alignment1, alignment2 = self.get_string_alignment_masks(
			reference_string, substring, True)
		
		alignment_1 = trim(alignment1)
		mismatches = sum([not x for x in alignment_1 + alignment2])
		matches = sum(alignment_1)

		return matches - mismatches


	def string_distance(self, name1, name2, substring_mode=False):
		distance, path = self.string_alignment(name1, name2, substring_mode)
		return distance[-1][-1]



	def get_string_alignment_masks(
		self,
		name1,
		name2,
		substring_mode=False
	):
		distance, path = self.string_alignment(name1, name2, substring_mode)

		alignment1 = [None for p in range(len(name1))]
		alignment2 = [None for q in range(len(name2))]
		i = len(name1)
		j = len(name2)
		while i > 0 or j > 0:
			if path[i][j] == self.UP:
				i -= 1
				alignment1[i] = 0
				continue

			if path[i][j] == self.LEFT:
				j -= 1
				alignment2[j] = 0
				continue

			if path[i][j] == self.DIAG:
				i -= 1
				j -= 1
				if distance[i][j] == distance[i+1][j+1]:
					alignment1[i] = 1
					alignment2[j] = 1
				else:
					alignment1[i] = 0
					alignment2[j] = 0

		return alignment1, alignment2


	def get_string_alignment_path(self, name1, name2, substring_mode=False):
		distance, path = self.string_alignment(name1, name2, substring_mode)

		linear_path = []
		i = len(name1)
		j = len(name2)
		while i > 0 or j > 0:
			if path[i][j] == self.UP:
				i -= 1
				linear_path.append(self.DELETE)
				continue

			if path[i][j] == self.LEFT:
				j -= 1
				linear_path.append(self.INSERT)
				continue

			if path[i][j] == self.DIAG:
				i -= 1
				j -= 1
				if distance[i][j] == distance[i+1][j+1]:
					linear_path.append(self.MATCH)
				else:
					linear_path.append(self.SUBSTITUTE)

		linear_path.reverse()
		return linear_path


	def display_string_alignment(self, name1, name2, substring_mode=False):
		alignment1, alignment2 = self.get_string_alignment_masks(
			name1, name2, substring_mode
		)

		i = 0
		j = 0
		display1 = []
		display2 = []
		display = []
		while i < len(name1) or j < len(name2):

			if i >= len(name1):
				display1.append('-')
				display2.append(name2[j])
				display.append(' ')
				j += 1
				continue

			if j >= len(name2):
				display1.append(name1[i])
				display2.append('-')
				display.append(' ')
				i += 1
				continue

			if alignment1[i]:
				if alignment2[j]:
					display1.append(name1[i])
					display2.append(name2[j])
					display.append('|')
					i += 1
					j += 1

				else:
					display1.append('-')
					display2.append(name2[j])
					display.append(' ')
					j += 1

			else:
				if alignment2[j]:
					display1.append(name1[i])
					display2.append('-')
					display.append(' ')
					i += 1

				else:

					# In substring mode, we favor deletion from the 
					# reference string (name1) until at least one match
					# is seen
					if substring_mode and j==0:
						display1.append(name1[i])
						display2.append('-')
						display.append(' ')
						i += 1

					# But normally this would be interpreted as a 
					# substitution
					else:
						display1.append(name1[i])
						display2.append(name2[j])
						display.append(' ')
						i += 1
						j += 1

		return '\n'.join([
			''.join(display1),
			''.join(display),
			''.join(display2)
		])

SA = StringAligner()
