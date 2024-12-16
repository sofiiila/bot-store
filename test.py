import unittest

loader = unittest.TestLoader()
tests = loader.discover('.')

suite = unittest.TestSuite()
suite.addTests(tests)

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
