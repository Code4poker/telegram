# -*- coding: utf-8 -*-
def search_procedure(file, number):
    numbers = []
    for n in range(10):
        numbers.append(str(n))

    with open(file, encoding='utf-8') as f:
        data = f.read().splitlines()

    for element in data:
        element = element.split(':')
        if element[0] == number:
            return element[1]
