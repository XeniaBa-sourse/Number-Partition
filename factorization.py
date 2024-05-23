def prime_factors(n):
    factors = []
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def factorization(n):
    factors = prime_factors(n)
    factorization_dict = {}
    for factor in factors:
        if factor in factorization_dict:
            factorization_dict[factor] += 1
        else:
            factorization_dict[factor] = 1
    return factorization_dict

def print_factorization(n):
    factorization_dict = factorization(n)
    result = f"{n} = "
    for factor, power in factorization_dict.items():
        result += f"{factor}^{power} * "
    result = result[:-3]  # Убираем лишнюю звёздочку и пробел в конце
    return result
