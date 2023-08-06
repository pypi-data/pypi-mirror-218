#!/usr/bin/python
 
from primepackage import is_prime
 
def test_numbers():
    response = is_prime(1)
    assert response == False
 
    response = is_prime(2)
    assert response == True
