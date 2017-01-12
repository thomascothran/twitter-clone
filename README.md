# A TDD Demo

This project is a demonstration of what a test driven development style looks like, using the example of a twitter clone. It is not intended for use in production.

Selenium is used for end to end testing, and Django's built in test client performs the unit tests. A review of the commits demonstrates the "red-green-refactor" cycle. 

First, we write the end to end test, specifying exactly what behavior should show up in the browser. This should happen before any other code is written. It helps to clarify the purpose of the code, and will detect regressions for us should we make changes elsewhere. We run the functional test to ensure it fails, which helps us avoid bugs in the test itself.

Second, we write the unit test. The distinction between a unit test and an end to end test is that the unit test focuses only on a single unit of functionality. For instance, for a helper method that returns True if a number is even, we test only that helper method; we do not test its interaction with other components. We then run the unit test to make it fail.

Third, we write the code to implement the function. We know the ultimate behavior we want from the end to end test. However, the code is best written in small increments that cause the unit test to pass.

After the unit test passes, we refactor. Taking a close look at what our code does, we make it more readable and concise. Now is a good time to double check that we haven't introduced unnecessary side effects.

Then we see if our end to end test passes. If so, great! If not, we write another unit test for the next bit of functionality, and follow the process from the second step on.

Testing code has obvious benefits when it comes to detecting regressions and other unintended consequences. It also helps to clarify what it is your doing, so that you don't chase rabbit trails. Finally, but equally importantly, code that is easy to test is better code: testable code tends to emphasize purer functions and better compartmentalization.
