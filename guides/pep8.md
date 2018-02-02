## PEP8

    Beautiful is better than ugly. The Zen of Python

To make our code readable and maintanble, we need some standards, Python has a style guide called [PEP8](https://www.python.org/dev/peps/pep-0008/).[Nice guide with the basics](https://gist.github.com/sloria/7001839).

If you still skipped the guide, here are the fundamental rules:

1. Variables, functions, methods, packages and modules: `lower_case_with_underscores`
2. Classes and Exceptions: `CapWords`
3. Avoid one-letter variables, except for counters
4. Use 4 spaces, never tabs
5. Line length should be between 80 characters

However, there are tools to automatically check if your code complies with the standard. `flake8` is one of such tools, and can check for PEP8 compliance as well as other common errors:

```shell
pip install flake8
```

To check a file:

```shell
flake8 my_script.py
```

Most text editors and IDE have plugins to automatically run tools such as `flake8` when you modify a file, [here's one for Sublime Text](http://www.sublimelinter.com/en/latest/).

If you want to know more about `flake8` and similar tools, [this is a nice resource](https://blog.sideci.com/about-style-guide-of-python-and-linter-tool-pep8-pyflakes-flake8-haking-pyling-7fdbe163079d)