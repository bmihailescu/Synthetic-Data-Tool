import unittest

loader = unittest.TestLoader()
suite = loader.discover('UnitTesting', pattern = '*.py')

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)
print(f"Total tests run   :   {result.testsRun}")
print(f"Tests passed      :   {result.testsRun - len(result.failures) - len(result.errors)}")
print(f"Tests failed      :   {len(result.failures)}")
print(f"Tests with errors :   {len(result.errors)}")
print("="*60)