def obrat(x):
    output = 0
    while x > 0:
        output += x % 10
        x //= 10
        output *= 10
    return output // 10

print(obrat(435))