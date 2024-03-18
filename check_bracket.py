from collections import deque

def check_bracket(s: str)->str:
    """check the bracket of a string whether it is valid or not

    Args:
        s (str): a string with brackets

    Returns:
        str: return a string with the same length as the input string indicating the validity of the brackets
    """
    stack = deque()
    result = [" "] * len(s)
    for index, char in enumerate(s):
        if char == '(':
            stack.append(index)
        elif char == ')':
            if not stack:
                result[index] = "?"
            else:
                stack.pop()
    while stack:
        result[stack.pop()] = "x"
    return "".join(result)


if __name__ == "__main__":
    assert check_bracket("bge)))))))))") == "   ?????????", "Test case 1 failed"
    assert check_bracket("((IIII))))))") == "        ????", "Test case 2 failed"
    assert check_bracket("()()()()(uuu") == "        x   ", "Test case 3 failed"
    assert check_bracket("))))UUUU((()") == "????    xx  ", "Test case 4 failed"
    print("All test cases passed!")