![An Introduction to Python Exceptions](https://files.realpython.com/media/Python_Exceptions_Watermark.47f814fbeced.jpg)

# Python Exceptions: An Introduction

by [Said van de Klundert](https://realpython.com/python-exceptions/#author) UpdatedDec 01, 2024Reading time estimate 24m


[35 Comments](https://realpython.com/python-exceptions/#reader-comments)[basics](https://realpython.com/tutorials/basics/) [python](https://realpython.com/tutorials/python/)
Mark as CompletedShare

Table of Contents

- [Understanding Exceptions and Syntax Errors](https://realpython.com/python-exceptions/#understanding-exceptions-and-syntax-errors)
- [Raising an Exception in Python](https://realpython.com/python-exceptions/#raising-an-exception-in-python)
- [Debugging During Development With assert](https://realpython.com/python-exceptions/#debugging-during-development-with-assert)
- [Handling Exceptions With the try and except Block](https://realpython.com/python-exceptions/#handling-exceptions-with-the-try-and-except-block)
- [Proceeding After a Successful Try With else](https://realpython.com/python-exceptions/#proceeding-after-a-successful-try-with-else)
- [Cleaning Up After Execution With finally](https://realpython.com/python-exceptions/#cleaning-up-after-execution-with-finally)
- [Creating Custom Exceptions in Python](https://realpython.com/python-exceptions/#creating-custom-exceptions-in-python)
- [Conclusion](https://realpython.com/python-exceptions/#conclusion)
- [Frequently Asked Questions](https://realpython.com/python-exceptions/#frequently-asked-questions)

[Remove ads](https://realpython.com/account/join/)

Recommended Courses

[Raising and Handling Python Exceptions](https://realpython.com/courses/raising-handling-exceptions/)(1h 2m)

1 more course

- [Introduction to Python Exceptions](https://realpython.com/courses/introduction-python-exceptions/)(13m)

Python exceptions provide a mechanism for handling errors that occur during the execution of a program. Unlike syntax errors, which are detected by the parser, Python raises exceptions when an error occurs in syntactically correct code. Knowing how to raise, catch, and handle exceptions effectively helps to ensure your program behaves as expected, even when encountering errors.

**By the end of this tutorial, you’ll understand that:**

- Exceptions in Python occur when **syntactically correct code** results in an **error**.
- **The `try` … `except` block** lets you execute code and handle exceptions that arise.
- You can use the `else`, and `finally` **keywords** for more refined **exception handling**.
- It’s **bad practice** to **catch all exceptions** at once using `except Exception` or the bare `except` clause.
- Combining `try`, `except`, and `pass` allows your program to **continue silently** without handling the exception.

In this tutorial, you’ll get to know Python exceptions and all relevant keywords for exception handling by walking through a practical example of handling a platform-related exception. Finally, you’ll also learn how to create your own custom Python exceptions.

**Get Your Code:** [Click here to download the free sample code](https://realpython.com/bonus/python-exceptions-code/) that shows you how exceptions work in Python.

**Take the Quiz:** Test your knowledge with our interactive “Python Exceptions: An Introduction” quiz. You’ll receive a score upon completion to help you track your learning progress:

* * *

[![An Introduction to Python Exceptions](https://files.realpython.com/media/Python_Exceptions_Watermark.47f814fbeced.jpg)](https://realpython.com/quizzes/python-exceptions/)

**Interactive Quiz**

[Python Exceptions: An Introduction](https://realpython.com/quizzes/python-exceptions/)

In this quiz, you'll test your understanding of Python exceptions. You'll cover the difference between syntax errors and exceptions and learn how to raise exceptions, make assertions, and use the try and except block.

## Understanding Exceptions and Syntax Errors [Permanent link](https://realpython.com/python-exceptions/\#understanding-exceptions-and-syntax-errors "Permanent link")

[Syntax errors](https://realpython.com/invalid-syntax-python/) occur when the parser detects an incorrect statement. Observe the following example:

Language: Python Traceback

```
>>> print(0 / 0))
  File "<stdin>", line 1
    print(0 / 0))
                ^
SyntaxError: unmatched ')'
```

Copied!

The arrow indicates where the parser ran into the **syntax error**. Additionally, the error message gives you a hint about what went wrong. In this example, there was one bracket too many. Remove it and run your code again:

Language: Python

```
>>> print(0 / 0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero
```

Copied!

This time, you ran into an **exception error**. This type of error occurs whenever syntactically correct Python code results in an error. The last line of the message indicates what type of exception error you ran into.

Instead of just writing _exception error_, Python details what _type_ of exception error it encountered. In this case, it was a `ZeroDivisionError`. Python comes with [various built-in exceptions](https://docs.python.org/3/library/exceptions.html) as well as the possibility to create user-defined exceptions.

[Remove ads](https://realpython.com/account/join/)

## Raising an Exception in Python [Permanent link](https://realpython.com/python-exceptions/\#raising-an-exception-in-python "Permanent link")

There are scenarios where you might want to stop your program by raising an exception if a condition occurs. You can do this with the [`raise`](https://realpython.com/python-raise-exception/) keyword:

![Illustration of  raise statement usage](https://files.realpython.com/media/raise.3931e8819e08.png)

You can even complement the statement with a custom message. Assume that you’re writing a tiny toy program that expects only numbers up to `5`. You can raise an error when an unwanted condition occurs:

Language: PythonFilename: `low.py`

```
number = 10
if number > 5:
    raise Exception(f"The number should not exceed 5. ({number=})")
print(number)
```

Copied!

In this example, you raised an `Exception` object and passed it an informative custom message. You built the message using an [f-string](https://realpython.com/python-f-strings/) and a [self-documenting expression](https://realpython.com/python-f-strings/#self-documenting-expressions-for-debugging).

When you run `low.py`, you’ll get the following output:

Language: Python Traceback

```
Traceback (most recent call last):
  File "./low.py", line 3, in <module>
    raise Exception(f"The number should not exceed 5. ({number=})")
Exception: The number should not exceed 5. (number=10)
```

Copied!

The program comes to a halt and displays the exception to your [terminal](https://realpython.com/terminal-commands/) or [REPL](https://realpython.com/python-repl/), offering you helpful clues about what went wrong. Note that the final call to [`print()`](https://realpython.com/python-print/) never executed, because Python raised the exception before it got to that line of code.

With the `raise` keyword, you can raise any exception object in Python and stop your program when an unwanted condition occurs.

## Debugging During Development With `assert` [Permanent link](https://realpython.com/python-exceptions/\#debugging-during-development-with-assert "Permanent link")

Before moving on to the most common way of working with exceptions in Python using [the `try` … `except` block](https://realpython.com/python-exceptions/#handling-exceptions-with-the-try-and-except-block), you’ll take a quick look at an exception that’s a bit different than the others.

Python offers a specific exception type that you should only use when debugging your program during development. This exception is the `AssertionError`. The `AssertionError` is special because you shouldn’t ever raise it yourself using `raise`.

Instead, you use [the `assert` keyword](https://dbader.org/blog/python-assert-tutorial) to check whether a condition is met and let Python raise the `AssertionError` if the condition isn’t met.

The idea of an assertion is that your program should only attempt to run if certain conditions are in place. If Python checks your assertion and finds that the condition is `True`, then that is excellent! The program can continue. If the condition turns out to be `False`, then your program raises an `AssertionError` exception and stops right away:

![Python assert statement](https://files.realpython.com/media/assert.f6d344f0c0b4.png)

Revisit your tiny script, `low.py`, from [the previous section](https://realpython.com/python-exceptions/#raising-an-exception-in-python). Currently, you’re explicitly raising an exception when a certain condition isn’t met:

Language: PythonFilename: `low.py`

```
number = 1
if number > 5:
    raise Exception(f"The number should not exceed 5. ({number=})")
print(number)
```

Copied!

Assuming that you’ll handle this constraint safely for your production system, you could replace this [conditional statement](https://realpython.com/python-conditional-statements/) with an assertion for a quick way to retain this sanity check during development:

Language: PythonFilename: `low.py`

```
number = 1
assert (number < 5), f"The number should not exceed 5. ({number=})"
print(number)
```

Copied!

If the `number` in your program is below `5`, then the assertion passes and your script continues with the next line of code. However, if you set `number` to a value higher than `5`—for example, `10`—then the outcome of the assertion will be `False`:

Language: PythonFilename: `low.py`

```
number = 10
assert (number < 5), f"The number should not exceed 5. ({number=})"
print(number)
```

Copied!

In that case, Python raises an `AssertionError` that includes the message you passed, and ends the program execution:

Language: Shell

```
$ python low.py
Traceback (most recent call last):
  File "./low.py", line 2, in <module>
    assert (number < 5), f"The number should not exceed 5. ({number=})"
            ^^^^^^^^^^
AssertionError: The number should not exceed 5. (number=10)
```

Copied!

In this example, raising an `AssertionError` exception is the last thing that the program will do. The program will then come to halt and won’t continue. The call to `print()` that follows the assertion won’t execute.

Using assertions in this way can be helpful when you’re debugging your program during development because it can be quite a fast and straightforward to add assertions into your code.

However, you shouldn’t rely on assertions for catching crucial run conditions of your program in production. That’s because Python globally disables assertions when you run it in optimized mode using the [`-O` and `-OO` command line options](https://docs.python.org/3/using/cmdline.html#cmdoption-O):

Language: Shell

```
$ python -O low.py
10
```

Copied!

In this run of your program, you used the `-O` command line option, which removes all `assert` statements. Therefore, your script ran all the way to the end and displayed a number that is _dreadfully_ high!

**Note:** Alternatively, you can also disable assertions through the [`PYTHONOPTIMIZE` environment variable](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONOPTIMIZE).

In production, your Python code may run using this optimized mode, which means that assertions aren’t a reliable way to handle runtime errors in production code. They can be quick and useful helpers when your debugging your code, but you should never use assertions to set crucial constraints for your program.

If `low.py` should reliably fail when `number` is above `5`, then it’s best to stick with [raising an exception](https://realpython.com/python-exceptions/#raising-an-exception-in-python). However, sometimes you might not want your program to fail when it encounters an exception, so how should you handle those situations?

[Remove ads](https://realpython.com/account/join/)

## Handling Exceptions With the `try` and `except` Block [Permanent link](https://realpython.com/python-exceptions/\#handling-exceptions-with-the-try-and-except-block "Permanent link")

In Python, you use the `try` and `except` block to catch and handle exceptions. Python executes code following the `try` statement as a normal part of the program. The code that follows the `except` statement is the program’s response to any exceptions in the preceding `try` clause:

![Diagram showing try and except statements](https://files.realpython.com/media/try_except.c94eabed2c59.png)

As you saw earlier, when syntactically correct code runs into an error, Python will raise an exception error. This exception error will crash the program if you don’t handle it. In the `except` clause, you can determine how your program should respond to exceptions.

The following function can help you understand the `try` and `except` block:

Language: PythonFilename: `linux_interaction.py`

```
def linux_interaction():
    import sys
    if "linux" not in sys.platform:
        raise RuntimeError("Function can only run on Linux systems.")
    print("Doing Linux things.")
```

Copied!

The `linux_interaction()` can only run on a Linux system. Python will raise a `RuntimeError` exception if you call it on an operating system other then Linux.

**Note:** Picking the right exception type can sometimes be tricky. Python comes with [many built-in exceptions](https://docs.python.org/3/library/exceptions.html#concrete-exceptions) that are [hierarchically related](https://docs.python.org/3/library/exceptions.html#exception-hierarchy), so if you browse the documentation, you’re likely to find a fitting one.

Python even groups some of the exceptions into categories, such as [warnings](https://docs.python.org/3/library/exceptions.html#warnings) that you should use to indicate warning conditions, and [OS exceptions](https://docs.python.org/3/library/exceptions.html#os-exceptions) that Python raises depending on system error codes.

If you still didn’t find a fitting exception, then you can [create a custom exception](https://realpython.com/python-exceptions/#creating-custom-exceptions-in-python).

You can give the function a `try` by adding the following code:

Language: PythonFilename: `linux_interaction.py`

```
# ...

try:
    linux_interaction()
except:
    pass
```

Copied!

The way you handled the error here is by handing out a `pass`. If you run this code on a macOS or Windows machine, then you get the following output:

Language: Shell

```
$ python linux_interaction.py
```

Copied!

You got nothing in response. The good thing here is that your program didn’t crash. But letting an exception that occurred pass silently is bad practice. You should always at least know about and [log](https://realpython.com/python-logging/) if some type of exception occurred when you ran your code.

To this end, you can change `pass` into something that generates an informative message:

Language: PythonFilename: `linux_interaction.py`

```
# ...

try:
    linux_interaction()
except:
    print("Linux function wasn't executed.")
```

Copied!

When you now execute this code on a macOS or Windows machine, you’ll see the message from your `except` block printed to the console:

Language: Shell

```
$ python linux_interaction.py
Linux function wasn't executed.
```

Copied!

When an exception occurs in a program that runs this function, then the program will continue as well as inform you about the fact that the function call wasn’t successful.

What you didn’t get to see was the type of error that Python raised as a result of the function call. In order to see exactly what went wrong, you’d need to catch the error that the function raised.

The following code is an example where you capture the `RuntimeError` and output that message to your screen:

Language: PythonFilename: `linux_interaction.py`

```
# ...

try:
    linux_interaction()
except RuntimeError as error:
    print(error)
    print("The linux_interaction() function wasn't executed.")
```

Copied!

In the `except` clause, you assign the `RuntimeError` to the temporary variable `error`—often also called `err`—so that you can access the exception object in the indented block. In this case, you’re printing the object’s string representation, which corresponds to the error message attached to the object.

Running this function on a macOS or Windows machine outputs the following:

Language: Shell

```
$ python linux_interaction.py
Function can only run on Linux systems.
The linux_interaction() function wasn't executed.
```

Copied!

The first message is the `RuntimeError`, informing you that Python can only execute the function on a Linux machine. The second message tells you which function wasn’t executed.

In the example above, you called a function that you wrote yourself. When you executed the function, you caught the `RuntimeError` exception and printed it to your screen.

Here’s another example where you open a file and use a built-in exception:

Language: PythonFilename: `open_file.py`

```
try:
    with open("file.log") as file:
        read_data = file.read()
except:
    print("Couldn't open file.log")
```

Copied!

If `file.log` doesn’t exist, then this block of code will output the following:

Language: Shell

```
$ python open_file.py
Couldn't open file.log
```

Copied!

This is an informative message, and your program will still continue to run. However, your `except` block will currently catch _any_ exception, whether that’s related to not being able to open the file or not. You could lead yourself onto a confusing path if you see this message even when Python raises a completely unrelated exception.

Therefore, it’s always best to be _specific_ when you’re handling an exception.

In the [Python docs](https://docs.python.org/3/library/exceptions.html), you can see that there are a couple of built-in exceptions that you could raise in such a situation, for example:

> _exception_`FileNotFoundError`
>
> Raised when a file or directory is requested but doesn’t exist. Corresponds to errno ENOENT. ( [Source](https://docs.python.org/3/library/exceptions.html#FileNotFoundError))

You want to handle the situation when Python can’t find the requested file. To catch this type of exception and print it to screen, you could use the following code:

Language: PythonFilename: `open_file.py`

```
try:
    with open("file.log") as file:
        read_data = file.read()
except FileNotFoundError as fnf_error:
    print(fnf_error)
```

Copied!

In this case, if `file.log` doesn’t exist, then the output will be the following:

Language: Shell

```
$ python open_file.py
[Errno 2] No such file or directory: 'file.log'
```

Copied!

You can have more than one function call in your `try` clause and anticipate catching various exceptions. Something to note here is that the code in the `try` clause will stop as soon as it encounters any one exception.

**Warning:** When you use a bare `except` clause, then Python catches any exception that inherits from `Exception`—which are most built-in exceptions! Catching the parent class, `Exception`, hides all errors—even those which you didn’t expect at all. This is why you should avoid bare `except` clauses in your Python programs.

Instead, you’ll want to refer to _specific exception classes_ that you want to catch and handle. You can learn more about why this is a good idea [in this tutorial](https://realpython.com/the-most-diabolical-python-antipattern/).

Look at the following code. Here, you first call `linux_interaction()` and then try to open a file:

Language: PythonFilename: `linux_interaction.py`

```
# ...

try:
    linux_interaction()
    with open("file.log") as file:
        read_data = file.read()
except FileNotFoundError as fnf_error:
    print(fnf_error)
except RuntimeError as error:
    print(error)
    print("Linux linux_interaction() function wasn't executed.")
```

Copied!

If you run this code on a macOS or Windows machine, then you’ll see the following:

Language: Shell

```
$ python linux_interaction.py
Function can only run on Linux systems.
Linux linux_interaction() function wasn't executed
```

Copied!

Inside the `try` clause, you ran into an exception immediately and didn’t get to the part where you attempt to open `file.log`. Now look at what happens when you run the code on a Linux machine if the file doesn’t exist:

Language: Shell

```
$ python linux_interaction.py
[Errno 2] No such file or directory: 'file.log'
```

Copied!

Note that if you’re handling specific exceptions as you did above, then the order of the `except` clauses doesn’t matter too much. It’s all about which of the exceptions Python raises first. As soon as Python raises an exception, it checks the except clauses from top to bottom and executes the first matching one that it finds.

Here are the key takeaways about using Python’s `try` … `except` statements:

- Python executes a `try` clause up until the point where it encounters the first exception.
- Inside the `except` clause—the exception handler—you determine how the program responds to the exception.
- You can anticipate [multiple exceptions](https://realpython.com/python-catch-multiple-exceptions/) and differentiate how the program should respond to them.
- [Avoid using bare `except` clauses](https://realpython.com/the-most-diabolical-python-antipattern/), because they can hide unexpected exceptions.

While using `try` together with `except` is probably the most common error handling that you’ll encounter, there’s more that you can do to fine-tune your program’s response to exceptions.

[Remove ads](https://realpython.com/account/join/)

## Proceeding After a Successful Try With `else` [Permanent link](https://realpython.com/python-exceptions/\#proceeding-after-a-successful-try-with-else "Permanent link")

You can use Python’s `else` statement to instruct a program to execute a certain block of code only in the absence of exceptions:

![Diagram of try, except, and else statements in Python](https://files.realpython.com/media/try_except_else.703aaeeb63d3.png)

Look at the following example:

Language: PythonFilename: `linux_interaction.py`

```
# ...

try:
    linux_interaction()
except RuntimeError as error:
    print(error)
else:
    print("Doing even more Linux things.")
```

Copied!

If you were to run this code on a Linux system, then the output would be the following:

Language: Shell

```
$ python linux_interaction.py
Doing Linux things.
Doing even more Linux things.
```

Copied!

Because the program didn’t run into _any_ exceptions, Python executed the code in the `else` clause. However, if you run this code on a macOS or Windows system, then you get a different output:

Language: Shell

```
$ python linux_interaction.py
Function can only run on Linux systems.
```

Copied!

The `linux_interaction()` function raised a `RuntimeError`. You’ve handled the exception, so your program doesn’t crash, and instead prints the exception message to the console. The code nested under the `else` clause, however, doesn’t execute, because Python encountered an exception during execution.

Note that structuring your code like this is different from just adding the call to `print()` outside of the context of the `try` … `except` block:

Language: PythonFilename: `linux_interaction.py`

```
# ...

try:
    linux_interaction()
except RuntimeError as error:
    print(error)
print("Doing even more Linux things.")
```

Copied!

If you don’t nest the `print()` call under the `else` clause, then it’ll execute even if Python encounters the `RuntimeError` that you handle in the `except` block above. On a Linux system, the output would be the same, but on macOS or Windows, you’d get the following output:

Language: Shell

```
$ python linux_interaction.py
Function can only run on Linux systems.
Doing even more Linux things.
```

Copied!

Nesting code under the `else` clause assures that it’ll only run when Python doesn’t encounter any exception when executing the `try` … `except` block.

You can also create a nested `try` … `except` block inside the `else` clause and catch possible exceptions there as well:

Language: PythonFilename: `linux_interaction.py`

```
# ...

try:
    linux_interaction()
except RuntimeError as error:
    print(error)
else:
    try:
        with open("file.log") as file:
            read_data = file.read()
    except FileNotFoundError as fnf_error:
        print(fnf_error)
```

Copied!

If you were to execute this code on a Linux machine, then you’d get the following result:

Language: Shell

```
$ python linux_interaction.py
Doing Linux things.
[Errno 2] No such file or directory: 'file.log'
```

Copied!

From the output, you can see that `linux_interaction()` ran. Because Python encountered no exceptions, it attempted to open `file.log`. That file didn’t exist, but instead of letting the program crash, you caught the `FileNotFoundError` exception and printed a message to the console.

[Remove ads](https://realpython.com/account/join/)

## Cleaning Up After Execution With `finally` [Permanent link](https://realpython.com/python-exceptions/\#cleaning-up-after-execution-with-finally "Permanent link")

Imagine that you always had to implement some sort of action to clean up after executing your code. Python enables you to do so using the `finally` clause:

![Diagram explaining try except else finally statements](https://files.realpython.com/media/try_except_else_finally.a7fac6c36c55.png)

Have a look at the following example:

Language: PythonFilename: `linux_interaction.py`

```
# ...

try:
    linux_interaction()
except RuntimeError as error:
    print(error)
else:
    try:
        with open("file.log") as file:
            read_data = file.read()
    except FileNotFoundError as fnf_error:
        print(fnf_error)
finally:
    print("Cleaning up, irrespective of any exceptions.")
```

Copied!

In this code, Python will execute everything in the `finally` clause. It doesn’t matter if you encounter an exception somewhere in any of the `try` … `except` blocks. Running the code on a macOS or Windows machine will output the following:

Language: Shell

```
$ python linux_interaction.py
Function can only run on Linux systems.
Cleaning up, irrespective of any exceptions.
```

Copied!

Note that the code inside the `finally` block will execute regardless of whether or not you’re handling the exceptions:

Language: PythonFilename: `linux_interaction.py`

```
# ...

try:
    linux_interaction()
finally:
    print("Cleaning up, irrespective of any exceptions.")
```

Copied!

You simplified the example code from above, but `linux_interaction()` still raises an exception on a macOS or Windows system. If you now run this code on an operating system other than Linux, then you’ll get the following output:

Language: Shell

```
$ python linux_interaction.py
Cleaning up, irrespective of any exceptions.
Traceback (most recent call last):
  ...
RuntimeError: Function can only run on Linux systems.
```

Copied!

Despite the fact that Python raised the `RuntimeError`, the code in the `finally` clause still executed and printed the message to your console.

This can be helpful because even code outside of a `try`… `except` block won’t necessarily execute if your script encounters an unhandled exception. In that case, your program will terminate and the code _after_ the `try` … `except` block will never run. However, Python will still execute the code inside of the `finally` clause. This helps you make sure that resources like [file handles](https://realpython.com/why-close-file-python/) and [database connections](https://realpython.com/python-sql-libraries/) are cleaned up properly.

## Creating Custom Exceptions in Python [Permanent link](https://realpython.com/python-exceptions/\#creating-custom-exceptions-in-python "Permanent link")

With the large number of built-in exceptions that Python offers, you’ll likely find a fitting type when deciding which exception to raise. However, sometimes your code won’t fit the mold.

Python makes it straightforward to create custom exception types by inheriting from a built-in exception. Think back to your `linux_interaction()` function:

Language: PythonFilename: `linux_interaction.py`

```
def linux_interaction():
    import sys
    if "linux" not in sys.platform:
        raise RuntimeError("Function can only run on Linux systems.")
    print("Doing Linux things.")

# ...
```

Copied!

Using a [`RuntimeError`](https://docs.python.org/3/library/exceptions.html#RuntimeError) isn’t a bad choice in this situation, but it would be nice if your exception name was a bit more specific. For this, you can create a custom exception:

Language: PythonFilename: `linux_interaction.py`

```
class PlatformException(Exception):
    """Incompatible platform."""

# ...
```

Copied!

You generally create a custom exception in Python by inheriting from `Exception`, which is the base class for most built-in Python exceptions as well. You could also inherit from a different exception, but choosing `Exception` is usually the best choice.

That’s really all that you need to do. In the code snippet above, you also added a [docstring](https://realpython.com/documenting-python-code/) that describes the exception type and serves as the class body.

**Note:** Python requires some indented code in the body of your class. Alternatively to using the docstring, you could’ve also used [`pass`](https://realpython.com/python-pass/) or [the ellipsis (`...`)](https://realpython.com/python-ellipsis/). However, adding a descriptive docstring adds the most value to your custom exception. To learn how to write effective docstrings, check out [How to Write Docstrings in Python](https://realpython.com/how-to-write-docstrings-in-python/).

While you can customize your exception object, you don’t need to do that. It’s often enough to give your custom Python exceptions a descriptive name, so you’ll know what happened when Python raises this exception in your code.

Now that you’ve defined the custom exception, you can raise it like any other Python exception:

Language: PythonFilename: `linux_interaction.py`

```
class PlatformException(Exception):
    """Incompatible platform."""

def linux_interaction():
    import sys
    if "linux" not in sys.platform:
        raise PlatformException("Function can only run on Linux systems.")
    print("Doing Linux things.")

# ...
```

Copied!

If you now call `linux_interaction()` on macOS or Windows, then you’ll see that Python raises your custom exception:

Language: Shell

```
$ python linux_interaction.py
Traceback (most recent call last):
  ...
PlatformException: Function can only run on Linux systems.
```

Copied!

You could even use your custom `PlatformException` as a parent class for other custom exceptions that you could descriptively name for each of the platforms that users may run your code on.

[Remove ads](https://realpython.com/account/join/)

## Conclusion [Permanent link](https://realpython.com/python-exceptions/\#conclusion "Permanent link")

At this point, you’re familiar with the basics of using Python exceptions. After seeing the difference between syntax errors and exceptions, you learned about various ways to raise, catch, and handle exceptions in Python. You also learned how you can create your own custom exceptions.

In this article, you gained experience working with the following exception-related keywords:

- `raise` allows you to raise an exception at any time.
- `assert` enables you to verify if a certain condition is met and raises an exception if it isn’t.
- In the `try` clause, all statements are executed until an exception is encountered.
- `except` allows you to catch and handle the exception or exceptions that Python encountered in the `try` clause.
- `else` lets you code sections that should run only when Python encounters no exceptions in the `try` clause.
- `finally` enables you to execute sections of code that should always run, whether or not Python encountered any exceptions.

**Get Your Code:** [Click here to download the free sample code](https://realpython.com/bonus/python-exceptions-code/) that shows you how exceptions work in Python.

You now understand the basic tools that Python offers for dealing with exceptions. If you’re curious about the topic and want to dive deeper, then take a look at the following tutorials:

- [Python’s Built-in Exceptions: A Walkthrough With Examples](https://realpython.com/python-built-in-exceptions/)
- [Exception Groups and `except*`](https://realpython.com/python311-exception-groups/#exception-groups-and-except-in-python-311)
- [Python `raise`: Effectively Raising Exceptions in Your Code](https://realpython.com/python-raise-exception/)
- [How to Catch Multiple Exception in Python](https://realpython.com/python-catch-multiple-exceptions/)
- [Understanding the Python Traceback](https://realpython.com/python-traceback/)
- [LBYL vs EAFP: Preventing or Handling Errors in Python](https://realpython.com/python-lbyl-vs-eafp/)

What’s your favorite aspect of exception handling in Python? Share your thoughts in the comments below.

## Frequently Asked Questions [Permanent link](https://realpython.com/python-exceptions/\#frequently-asked-questions "Permanent link")

Now that you have some experience with Python exceptions, you can use the questions and answers below to check your understanding and recap what you’ve learned.

These FAQs are related to the most important concepts you’ve covered in this tutorial. Click the _Show/Hide_ toggle beside each question to reveal the answer.

**What are exceptions in Python?**Show/Hide

Exceptions in Python are errors that occur during the execution of a program, disrupting the normal flow of the program.

**How are exceptions handled in Python?**Show/Hide

You handle exceptions in Python using a `try` … `except` block. Python executes the code in the `try` block and if an exception occurs, it switches to executing the code in the `except` block to handle the exception. However, only the exceptions that are explicitly specified in the `except` block will be handled. If an exception is not caught, it’ll propagate up the call stack and may result in the termination of your program.

**How do you catch all exceptions in Python?**Show/Hide

To catch all exceptions in Python, you can use a bare `except` clause or write `except Exception`, but it’s recommended to catch specific exceptions to avoid masking unexpected errors.

**How does `try` … `except` in Python work?**Show/Hide

In a `try` … `except` block, Python executes the code under `try` and if an exception occurs, it immediately jumps to the `except` block to handle it, allowing the program to continue running.

**What does `try` … `except``pass` do in Python?**Show/Hide

Using `try` … `except` with `pass` allows the program to ignore the exception and continue execution without taking any specific action in response to the error. However, this practice can hide potential issues, making it harder to debug and maintain the code, so use it with caution. It’s generally better to either handle the exception explicitly or log it for debugging purposes.

**How do you raise an exception in Python?**Show/Hide

You raise an exception in Python using the `raise` keyword followed by an exception object, which can include a custom message.

**What is the purpose of using `assert` in Python?**Show/Hide

You can use the `assert` keyword to check if a condition is true during development. If the condition is false, it raises an `AssertionError`, which can help with debugging. Note that assertions can be disabled by running Python with the `-O` (optimize) flag. Therefore, you shouldn’t rely on assertions for critical checks in production code, as they may be ignored.

**What is the role of the `finally` clause in exception handling?**Show/Hide

The `finally` clause contains code that will always execute after a `try` block, regardless of whether an exception was raised or not, ensuring necessary cleanup actions occur.

**Take the Quiz:** Test your knowledge with our interactive “Python Exceptions: An Introduction” quiz. You’ll receive a score upon completion to help you track your learning progress:

* * *

[![An Introduction to Python Exceptions](https://files.realpython.com/media/Python_Exceptions_Watermark.47f814fbeced.jpg)](https://realpython.com/quizzes/python-exceptions/)

**Interactive Quiz**

[Python Exceptions: An Introduction](https://realpython.com/quizzes/python-exceptions/)

In this quiz, you'll test your understanding of Python exceptions. You'll cover the difference between syntax errors and exceptions and learn how to raise exceptions, make assertions, and use the try and except block.

Mark as Completed

[Liked it](https://realpython.com/feedback/survey/article/python-exceptions/liked/?from=article-footer "Liked it")[Disliked it](https://realpython.com/feedback/survey/article/python-exceptions/disliked/?from=article-footer "Disliked it")

Share

Recommended Courses

[Raising and Handling Python Exceptions](https://realpython.com/courses/raising-handling-exceptions/)(1h 2m)

1 more course

- [Introduction to Python Exceptions](https://realpython.com/courses/introduction-python-exceptions/)(13m)

🐍 Python Tricks 💌

Get a short & sweet **Python Trick** delivered to your inbox every couple of days. No spam ever. Unsubscribe any time. Curated by the Real Python team.

![Python Tricks Dictionary Merge](https://realpython.com/static/pytrick-dict-merge.4201a0125a5e.png)

Send Me Python Tricks »

About **Said van de Klundert**

[![Said van de Klundert](https://realpython.com/cdn-cgi/image/width=335,height=335,fit=crop,gravity=auto,format=auto/https://files.realpython.com/media/AAEAAQAAAAAAAAQiAAAAJGJmOGNlMzMzLTg1MmEtNGQwYy1hZDkyLTEwYzI0MjRjNTZkOA_2.8aa7cc5bf1f9.jpg)![Said van de Klundert](https://realpython.com/cdn-cgi/image/width=335,height=335,fit=crop,gravity=auto,format=auto/https://files.realpython.com/media/AAEAAQAAAAAAAAQiAAAAJGJmOGNlMzMzLTg1MmEtNGQwYy1hZDkyLTEwYzI0MjRjNTZkOA_2.8aa7cc5bf1f9.jpg)](https://realpython.com/team/svdklundert/)

Said is a network engineer, Python enthusiast, and a guest author at Real Python.

[» More about Said](https://realpython.com/team/svdklundert/)

* * *

_Each tutorial at Real Python is created by a team of developers so that it meets our high quality standards. The team members who worked on this tutorial are:_

[![Adriana Cutenco](https://realpython.com/cdn-cgi/image/width=900,height=900,fit=crop,gravity=auto,format=auto/https://files.realpython.com/media/acutenco.676e4197c133.jpg)](https://realpython.com/team/acutenco/)

[Adriana](https://realpython.com/team/acutenco/)

[![Brenda Weleschuk](https://realpython.com/cdn-cgi/image/width=320,height=320,fit=crop,gravity=auto,format=auto/https://files.realpython.com/media/IMG_3324_1.50b309355fc1.jpg)](https://realpython.com/team/bweleschuk/)

[Brenda](https://realpython.com/team/bweleschuk/)

[![Bartosz Zaczyński](https://realpython.com/cdn-cgi/image/width=1694,height=1694,fit=crop,gravity=auto,format=auto/https://files.realpython.com/media/coders_lab_2109368.259b1599fbee.jpg)](https://realpython.com/team/bzaczynski/)

[Bartosz](https://realpython.com/team/bzaczynski/)

[![Geir Arne Hjelle](https://realpython.com/cdn-cgi/image/width=800,height=800,fit=crop,gravity=auto,format=auto/https://files.realpython.com/media/gahjelle.470149ee709e.jpg)](https://realpython.com/team/gahjelle/)

[Geir Arne](https://realpython.com/team/gahjelle/)

[![Joanna Jablonski](https://realpython.com/cdn-cgi/image/width=800,height=800,fit=crop,gravity=auto,format=auto/https://files.realpython.com/media/jjablonksi-avatar.e37c4f83308e.jpg)](https://realpython.com/team/jjablonski/)

[Joanna](https://realpython.com/team/jjablonski/)

[![Kate Finegan](https://realpython.com/cdn-cgi/image/width=400,height=400,fit=crop,gravity=auto,format=auto/https://files.realpython.com/media/VZxEtUor_400x400.7169c68e3950.jpg)](https://realpython.com/team/kfinegan/)

[Kate](https://realpython.com/team/kfinegan/)

[![Martin Breuss](https://realpython.com/cdn-cgi/image/width=456,height=456,fit=crop,gravity=auto,format=auto/https://files.realpython.com/media/martin_breuss_python_square.efb2b07faf9f.jpg)](https://realpython.com/team/mbreuss/)

[Martin](https://realpython.com/team/mbreuss/)

Master Real-World Python Skills With Unlimited Access to Real Python

![Locked learning resources](https://realpython.com/static/videos/lesson-locked.f5105cfd26db.svg)

**Join us and get access to thousands of tutorials, hands-on video courses, and a community of expert Pythonistas:**

[Level Up Your Python Skills »](https://realpython.com/account/join/?utm_source=rp_article_footer&utm_content=python-exceptions)

Master Real-World Python Skills

With Unlimited Access to Real Python

![Locked learning resources](https://realpython.com/static/videos/lesson-locked.f5105cfd26db.svg)

**Join us and get access to thousands of tutorials, hands-on video courses, and a community of expert Pythonistas:**

[Level Up Your Python Skills »](https://realpython.com/account/join/?utm_source=rp_article_footer&utm_content=python-exceptions)

What Do You Think?

**Rate this article:**

[Liked it](https://realpython.com/feedback/survey/article/python-exceptions/liked/?from=article-comments "Liked it")[Disliked it](https://realpython.com/feedback/survey/article/python-exceptions/disliked/?from=article-comments "Disliked it")

[LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Frealpython.com%2Fpython-exceptions%2F) [Twitter](https://twitter.com/intent/tweet/?text=Interesting%20Python%20article%20on%20%40realpython%3A%20Python%20Exceptions%3A%20An%20Introduction&url=https%3A%2F%2Frealpython.com%2Fpython-exceptions%2F) [Bluesky](https://bsky.app/intent/compose?text=Interesting%20Python%20article%20on%20%40realpython.com%3A%20Python%20Exceptions%3A%20An%20Introduction%20https%3A%2F%2Frealpython.com%2Fpython-exceptions%2F) [Facebook](https://facebook.com/sharer/sharer.php?u=https%3A%2F%2Frealpython.com%2Fpython-exceptions%2F) [Email](mailto:?subject=Python%20article%20for%20you&body=Python%20Exceptions%3A%20An%20Introduction%20on%20Real%20Python%0A%0Ahttps%3A%2F%2Frealpython.com%2Fpython-exceptions%2F%0A)

What’s your #1 takeaway or favorite thing you learned? How are you going to put your newfound skills to use? Leave a comment below and let us know.

**Commenting Tips:** The most useful comments are those written with the goal of learning from or helping out other students. [Get tips for asking good questions](https://realpython.com/python-beginner-tips/#tip-9-ask-good-questions) and [get answers to common questions in our support portal](https://support.realpython.com/).

* * *

Looking for a real-time conversation? Visit the [Real Python Community Chat](https://realpython.com/community/) or join the next [“Office Hours” Live Q&A Session](https://realpython.com/office-hours/). Happy Pythoning!

Keep Learning

Related Topics:


[basics](https://realpython.com/tutorials/basics/) [python](https://realpython.com/tutorials/python/)

Related Learning Paths:

- [Exceptions, Logging, and Debugging](https://realpython.com/learning-paths/exception-handling-logging-debugging/?utm_source=realpython&utm_medium=web&utm_campaign=related-learning-path&utm_content=python-exceptions)
- [Revisit Python Fundamentals](https://realpython.com/learning-paths/python3-introduction/?utm_source=realpython&utm_medium=web&utm_campaign=related-learning-path&utm_content=python-exceptions)

Related Courses:

- [Raising and Handling Python Exceptions](https://realpython.com/courses/raising-handling-exceptions/?utm_source=realpython&utm_medium=web&utm_campaign=related-course&utm_content=python-exceptions)
- [Introduction to Python Exceptions](https://realpython.com/courses/introduction-python-exceptions/?utm_source=realpython&utm_medium=web&utm_campaign=related-course&utm_content=python-exceptions)

Related Tutorials:

- [Defining Your Own Python Function](https://realpython.com/defining-your-own-python-function/?utm_source=realpython&utm_medium=web&utm_campaign=related-post&utm_content=python-exceptions)
- [Python's raise: Effectively Raising Exceptions in Your Code](https://realpython.com/python-raise-exception/?utm_source=realpython&utm_medium=web&utm_campaign=related-post&utm_content=python-exceptions)
- [Object-Oriented Programming (OOP) in Python](https://realpython.com/python3-object-oriented-programming/?utm_source=realpython&utm_medium=web&utm_campaign=related-post&utm_content=python-exceptions)
- [Python Modules and Packages – An Introduction](https://realpython.com/python-modules-packages/?utm_source=realpython&utm_medium=web&utm_campaign=related-post&utm_content=python-exceptions)
- [Python's Built-in Exceptions: A Walkthrough With Examples](https://realpython.com/python-built-in-exceptions/?utm_source=realpython&utm_medium=web&utm_campaign=related-post&utm_content=python-exceptions)

Free Bonus: **Python Cheat Sheet** ×

Get a **Python Cheat Sheet (PDF)** and learn the basics of Python, like working with data types, dictionaries, lists, and Python functions:

![Python Cheat Sheet](https://realpython.com/python-exceptions/)

Send My Python Cheat Sheet »