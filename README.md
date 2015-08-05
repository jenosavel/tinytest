# tinytest
A simple unit test framework that makes readable output not a complete pain in my rear.

Writing tests:

1) Import everything from tinytest.test
2) Inherit your tests from TestClass
3) Use decorators to assign your test fixtures & descriptions
4) Use the built-in logger for any debug output you need

Running tests:

1) Import tinytest.TinyTester
2) Initialize the test runner with a custom log level, if desired.
3) Call the test runner's run method, passing in all the test classes you want to run.
4) Get results in the console log as well as a local file!