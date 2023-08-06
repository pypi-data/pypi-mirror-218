#!/usr/bin/python
 
from primepackage import is_prime

def test_is_prime():
    response = is_prime(1)
    assert response == False
