# allows you to execute a given function on each element of an iterable, with the ability to retry failed attempts a specified number of times

## pip install retryloop 

The retryloop function is a utility function that allows you to execute a given function 
on each element of an iterable, with the ability to retry failed attempts a specified number of times. 
It provides error resilience and flexibility in handling exceptions during function execution.


### Error Resilience: 

The function allows you to retry the execution of a given function on a collection 
of elements, providing resilience in the face of potential errors or exceptions. 
It retries failed attempts a specified number of times (maxretries), which can be 
helpful when dealing with intermittent errors or unreliable external resources.

### Customizable Retry Behavior: 

You can control the number of retries (maxretries) for each failed attempt. This 
flexibility enables you to fine-tune the retry behavior based on the specific 
requirements of your application.

### Input and Result Tracking:

By setting add_input to True, the function keeps track of the input elements along 
with their corresponding results. This can be valuable for debugging purposes or for 
analyzing the behavior of the function on different inputs.

### Result Collection: 

If results is set to True, the function collects and returns the results in a list. 
This simplifies the process of aggregating and processing the outcomes of the function executions.


## Example Usage

```python
from retryloop import retryloop
from random import randint
def devidefunction(no, multi, plus):
    return 10 / no * multi + plus
i = [randint(0, 2) for _ in range(10)] # [2, 2, 1, 2, 2, 0, 2, 2, 1, 1]
results = retryloop(devidefunction, i, args=(5,), kwargs={'plus': 10}, maxretries=3, verbose=True)
print(results)
counter: 1
division by zero
counter: 2
division by zero
counter: 3
division by zero
[[0, 2, 35.0],
 [1, 2, 35.0],
 [2, 1, 60.0],
 [3, 2, 35.0],
 [4, 2, 35.0],
 [6, 2, 35.0],
 [7, 2, 35.0],
 [8, 1, 60.0],
 [9, 1, 60.0]]
 
##############################
 
from retryloop import retryloop
from random import randint
def devidefunction(no, multi, plus):
    return 10 / no * multi + plus
i = [randint(0, 2) for _ in range(10)] # [2, 1, 2, 2, 2, 2, 2, 2, 2, 0]
results = retryloop(devidefunction, i, args=(5,), kwargs={'plus': 10}, maxretries=3, verbose=True, add_input=False, results=True)
print(results)
counter: 1
division by zero
counter: 2
division by zero
counter: 3
division by zero
[[0, 35.0], [1, 60.0], [2, 35.0], [3, 35.0], [4, 35.0], [5, 35.0], [6, 35.0], [7, 35.0], [8, 35.0]]




retryloop(
    f,
    i: list,
    args: tuple = (),
    kwargs: dict | None = None,
    maxretries: int = 5,
    add_input: bool = True,
    results: bool = True,
    verbose: bool = True,
):
    """
    Execute the given function on each element of the iterable, retrying failed attempts a specified number of times.

    Args:
        f (callable): The function to be executed on each element of the iterable.
        i (list): The iterable containing the elements on which the function is applied.
        args (tuple, optional): The positional arguments to be passed to the function `f`. Defaults to ().
        kwargs (dict, optional): The keyword arguments to be passed to the function `f`. Defaults to None.
        maxretries (int, optional): The maximum number of retries for each failed attempt. Defaults to 5.
        add_input (bool, optional): Whether to include the input element along with the result in the results list.
                                   Defaults to True.
        results (bool, optional): Whether to collect and return the results in a list. Defaults to True.
        verbose (bool, optional): Whether to print error messages and retry counter. Defaults to True.

    Returns:
        list: A list of results, where each result is a list [index, input_element, function_result] if `add_input` is True,
              or [index, function_result] if `add_input` is False. If `results` is False, an empty list is returned.
    """
```