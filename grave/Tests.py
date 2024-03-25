"""test your objects using the tester"""

from collections.abc import Callable

from .Core import Thing

class GraveTester(Thing):
    """Automatically test every single method in a class that inherits from GraveTester"""
    def __init__(
        self,
        ):
        """Initialize a GraveTester"""
        super().__init__()

        self._results : list[bool] = []

        self._tests = [
            getattr(self, func)
            for func in dir(self)
            if (
                callable(getattr(self, func))
                and not func.startswith("__")
                and func not in {"run_tests"}
                )
        ]

    def run_tests(self) -> str:
        """Run each test in the class"""
        self._results = [test() for test in self._tests]

        all_true : bool = all(result for result in self._results)
        all_tests_run : bool = len(self._tests) == len(self._results)

        if not all_tests_run:
            raise ValueError

        result = "All Tests Ran:\n=================\n"

        for _test, _result in list(zip(self._tests, self._results)):
            result += f"{_test.__name__}: {'passed' if _result else 'failed'}" + '\n'

        result += "\n=================\n"
        result += "Some tests failed." if not all_true else "All tests passed!"
        result += "\n=================\n"

        return result

    def __call__(self) -> str:
        """Alias for run_tests()"""
        return self.run_tests()

    def __str__(self):
        """Alias for run_tests() for use when printing report"""
        return self.run_tests()

class GraveTesterTester(GraveTester):
    """Test a GraveTester"""

    def test_tester(self):
        """Test if the a_test method is in the dictionary"""
        return "test_tester" in dir(self)
