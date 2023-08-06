import unittest


class Foo(object):

	def __init__(self):
		self.bar = None

	def set_bar(self):
		self.bar = True

	def __invert__(self):
		print(f'here {self.bar}')
		return self.bar

	def __pos__(self):
		print(f'__pos__ called {self.bar}')
		return self.bar is not None

	def __add__(self, other):
		print(f'__add__ called {other}')




class MyTestCase(unittest.TestCase):
	def test_something(self):

		f = Foo()

		if ~f is None:
			print('yeah')
			self.assertEqual(True, True)

		f.set_bar()
		if +f:
			print(f'yeah 2')
			self.assertEqual(True, True)

		x = Foo()
		b = x + f
		print(f'b {b}')






if __name__ == '__main__':
	unittest.main()
