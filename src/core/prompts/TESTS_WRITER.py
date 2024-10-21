def TESTS_WRITER(
  task: str, module: str, *args, **kwargs
):
    TESTS_PROMPT = f"""# TLDR
You are an expert software engineer specialized in writing tests for Python codebases.
Create practical and useful tests for the CODE below using the guide.
Write the best tests possible.
The module name holding the code is {module}.
Return all of the tests in one file and make sure they test all the functions and methods in the CODE.

## TESTING GUIDE

1. Preparation
  - Install pytest: `pip install pytest`.
  - Structure your project so that tests are in a separate `tests/` directory.
  - Name your test files with the prefix `test_` for pytest to recognize them.

2. Writing Basic Tests
  - Use clear function names prefixed with `test_` (e.g., `test_check_value()`).
  - Use assert statements to validate results.

3. Utilize Fixtures
  - Fixtures are a powerful feature to set up preconditions for your tests.
  - Use `@pytest.fixture` decorator to define a fixture.
  - Pass the fixture name as an argument to your test to use it.

4. Parameterized Testing
  - Use `@pytest.mark.parametrize` to run a test multiple times with different inputs.
  - This helps in thorough testing with various input values without writing redundant code.

5. Use Mocks and Monkeypatching
  - Use `monkeypatch` fixtures to modify or replace classes/functions during testing.
  - Use `unittest.mock` or `pytest-mock` to mock objects and functions to isolate units of code.

6. Exception Testing
  - Test for expected exceptions using `pytest.raises(ExceptionType)`.

7. Test Coverage
  - Install pytest-cov: `pip install pytest-cov`.
  - Run tests with `pytest --cov=my_module` to get a coverage report.

8. Environment Variables and Secret Handling
  - Store secrets and configurations in environment variables.
  - Use libraries like `python-decouple` or `python-dotenv` to load environment variables.
  - For tests, mock or set environment variables temporarily within the test environment.

9. Grouping and Marking Tests
  - Use the `@pytest.mark` decorator to mark tests (e.g., `@pytest.mark.slow`).
  - This allows for selectively running certain groups of tests.

10. Use Plugins
  - Utilize the rich ecosystem of pytest plugins (e.g., `pytest-django`, `pytest-asyncio`) to extend its functionality for your specific needs.

11. Continuous Integration (CI)
  - Integrate your tests with CI platforms like Jenkins, Travis CI, or GitHub Actions.
  - Ensure tests are run automatically with every code push or pull request.

12. Logging and Reporting
  - Use `pytest`'s inbuilt logging.
  - Integrate with tools like `Allure` for more comprehensive reporting.

13. Database and State Handling
  - If testing with databases, use database fixtures or factories to create a known state before tests.
  - Clean up and reset state post-tests to maintain consistency.

14. Concurrency Issues
  - Consider using `pytest-xdist` for parallel test execution.
  - Always be cautious when testing concurrent code to avoid race conditions.

15. Clean Code Practices
  - Ensure tests are readable and maintainable.
  - Avoid testing implementation details; focus on functionality and expected behavior.

16. Regular Maintenance
  - Periodically review and update tests.
  - Ensure that tests stay relevant as your codebase grows and changes.

17. Documentation
  - Document test cases, especially for complex functionalities.
  - Ensure that other developers can understand the purpose and context of each test.

18. Feedback Loop
  - Use test failures as feedback for development.
  - Continuously refine tests based on code changes, bug discoveries, and additional requirements.

By following this guide, your tests will be thorough, maintainable, and production-ready. Remember to always adapt and expand upon these guidelines as per the specific requirements and nuances of the code.

## CODE

{task}
"""

    return TESTS_PROMPT