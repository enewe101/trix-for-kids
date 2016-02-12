def invert_dict(dictionary):
	new_dict = {}
	for key in dictionary:
		new_dict[dictionary[key]] = key

	return new_dict
