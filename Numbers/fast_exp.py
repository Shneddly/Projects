'''
Exponentiation of two integers using binary exponentiation and recursion
'''
def binary_exp(a,b):
    if b == 0:
        return 1
    res = binary_exp(a,int(b/2))
    if b%2:
        return res*res*a
    else:
        return res*res
