# Currency Quote

Topics covered:
- APIs and requests
- Error handling with decorator and retries

Decorator: A decorator is a design pattern in Python that allows a user to add new functionality to an existing object without modifying its structure. Decorators are often called before defining a function you want to decorate.

Below is an example of a decorator used to handle errors:

```python
def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f'Error: {e}')
    return wrapper

@error_handler
def quote(value, currency):
    response = requests.get(f'https://economia.awesomeapi.com.br/last/{currency}')
    if response:
        raw_data = response.json()
        dollar = raw_data[currency.replace('-', '')]['bid']
        return f"{value} {currency[:3]} costs {(float(dollar)*value):.2f} {currency[4:]} today."
    else:
        return "Error"
```

We use the `@error_handler` to indicate the decorator that will be applied to the `quote` function.
`error_handler` takes the `quote` function as a parameter and returns a `wrapper` function which takes the parameters of the `quote` function. `wrapper` returns the result of the `quote` function with error handling.

Why use decorators to handle errors?
Because when we define a function and it will be executed several times and inside it there are several blocks of code that can generate errors, this can be a problem for the developer. A simple `try/except` cannot handle all possible errors.

Example:
The `multi_currencies` function is called 5 times. On line 101, we pass a parameter to the function that might generate an error. 

![call_function](call_func.png)

Result using `try/except`:
![try_except_example](simple_try_except.png)

Result using `decorator`:
![decorator_example](decorator_error_handler.png)

With the decorator, the error is handled and the program continues to run. With try/except, the program is stopped and the error is handled.

Although decorator is a good option to identify and handle errors in code, when it comes to APIs we have some very specific types of errors, such as `timeout`, `connection refused`, `not found` and `permission denied`.

For that, there is a package called `backoff` that allows retrieving requests.

```python
@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException), max_tries=5)
def quote(value, currency):
    response = requests.get(f'https://economia.awesomeapi.com.br/last/{currency}')
    if response:
        raw_data = response.json()
        dollar = raw_data[currency.replace('-', '')]['bid']
        return f"{value} {currency[:3]} costs {(float(dollar)*value):.2f} {currency[4:]} today."
    else:
        return "Error"

```

We add the `@backoff.on_exception` to indicate that the `quote` function will run with retries and indicate the errors to be handled. This way, if an error occurs, the program will restart and try again in 5 attempts, instead of being interrupted by the error in the first attempt. We should apply this type of treatment depending on the type of error we receive. Timeout, for example, is a good case for establishing retries rather than stopping execution as soon as it occurs.

API used:
https://docs.awesomeapi.com.br/api-de-moedas
