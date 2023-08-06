from collections import deque


def retryloop(
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
    l = i.copy()
    if not kwargs:
        kwargs = {}
    tmplist = deque([], 1)
    maxretries_counter = 0
    listcounter = 0
    results_list = []
    while l:
        tmplist.append(g := l.pop(0))
        try:
            if results:
                if add_input:
                    results_list.append([listcounter, g, f(g, *args, **kwargs)])
                else:
                    results_list.append([listcounter, f(g, *args, **kwargs)])

            else:
                _ = f(g, *args, **kwargs)
            if maxretries_counter == 0:
                listcounter += 1
            maxretries_counter = 0
        except Exception as fe:
            maxretries_counter += 1
            if maxretries_counter == 1:
                listcounter += 1
            if verbose:
                print(f"counter: {maxretries_counter}")
                print(fe)
            if maxretries_counter < maxretries:
                l.insert(0, tmplist[0])
            else:
                maxretries_counter = 0
    return results_list
