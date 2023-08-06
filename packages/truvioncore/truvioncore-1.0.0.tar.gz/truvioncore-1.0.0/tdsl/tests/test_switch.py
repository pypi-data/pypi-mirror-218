def add():
	return n+m

def subs():
	return n-m

def prod():
	return n*m

def div():
	return m/n

def rem():
	return m%n

def operations(op):
	print(f'. operations called {op}')
	switch={
		 '+': add(),
		 '-': subs(),
		 '*': prod(),
		 '/': div(),
		 '%': rem(),
		 }
	return switch.get(op,'Choose one of the following operator:+,-,*,/,%')

if __name__ == '__main__':

	n = 1
	m = 3

	print(operations('*'))
	print(operations('^'))