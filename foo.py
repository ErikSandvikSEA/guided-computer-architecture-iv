"""
Stack Frames

When you call, push the return address on the stack, jump to the function
When you return, pop the return address off the stack, set the PC to it

Stack

699: a: 2                        |
698: b: ??                       | main's stack frame
697: return address 1      |

696: x: 2                         |
695: y: 7                         |
694: z: ??                        | mult2's stack frame
693: return address 2       |

__________
return value: 14
"""


def mult2(x, y):
    z = x * y
    return z


def main():
    a = 2

    # return address 2 is the equal sign
    b = mult2(a, 7)

    print(b)  # 14


main()

# return address 1

