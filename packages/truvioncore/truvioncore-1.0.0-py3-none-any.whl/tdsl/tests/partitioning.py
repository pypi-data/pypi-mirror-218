if __name__ == '__main__':

	s, e = 0, 0

	for i in range(1, 10):
		s = s + e * i
		e = s + 1000
		print(s, e)

