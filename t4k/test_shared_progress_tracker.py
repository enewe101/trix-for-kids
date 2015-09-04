import multiprocessing
import time
import random
import t4k


def run_test():
	#tracker = t4k.ProgressTracker('test_dict')
	tracker = t4k.SharedProgressTracker('test_dict')


	p1 = multiprocessing.Process(target=rand_sleep, args=(tracker,))
	p2 = multiprocessing.Process(target=rand_sleep, args=(tracker,))

	p1.start()
	p2.start()

	p1.join()
	p2.join()

	print tracker['yo']
	tracker.close()


def rand_sleep(tracker):
	for i in range(10):
		print '.'
		time.sleep(random.random())
		if 'yo' in tracker:
			tracker['yo'] += 1
		else:
			tracker['yo'] = 1


if __name__=='__main__':
	run_test()
