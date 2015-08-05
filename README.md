# tinytest
A simple unit test framework that makes readable output not a complete pain in my rear.

Writing tests:

<ol>
<li>Import everything from tinytest.test</li>
<li>Inherit your tests from TestClass</li>
<li>Use decorators to assign your test fixtures & descriptions</li>
<li>Use the built-in logger for any debug output you need</li>
</ol>

Running tests:

<ol>
<li>Import tinytest.TinyTester</li>
<li>Initialize the test runner with a custom log level, if desired.</li>
<li>Call the test runner's run method, passing in all the test classes you want to run.</li>
<li>Get results in the console log as well as a local file!</li>
</ol>
