# %%

import random

# %%

def generate_code(n_colors : int = 6, code_length : int = 4) -> tuple[int, ...]:

    if n_colors <= 0:
        raise ValueError("n_colors must be positive")

    if code_length <= 0:
        raise ValueError("code_length must be positive")

    code = []
    for _ in range(code_length):
        code.append(random.randint(0, n_colors-1))
    return tuple(code)

# %%