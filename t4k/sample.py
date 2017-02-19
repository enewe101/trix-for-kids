import random

def reservoir_sample(iterator, k, allow_small_sample=False):

	sample = []

	for i, item in enumerate(iterator):
		if i < k:
			sample.append(item)
		else:
			pick = random.randint(0,i)
			if pick < k:
				sample[pick] = item

	if len(sample) < k and not allow_small_sample:
		raise ValueError('Population smaller than sample size')

	return sample



