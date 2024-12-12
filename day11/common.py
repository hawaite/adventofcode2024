from functools import cache

@cache
def blink(digit, times) -> int:
    # stones labeled "0" become "1"
    if times == 0:
        return 1
    
    if digit == 0:
        return blink(1, times - 1)
    
    if len(str(digit)) % 2 == 0:
        half_ix = int(len(str(digit)) / 2)
        return blink(int(str(digit)[:half_ix]), times-1) + blink(int(str(digit)[half_ix:]), times-1)
    
    return blink(digit * 2024, times - 1)