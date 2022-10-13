import random

array = list(map(int, input('Введите последовательность чисел через пробел: ').split()))
number = int(input('Введите число больше минимального и не превышающее максимальное из последовательности: '))

while True:
    if number not in range(min(array) + 1,max(array) + 1):
        print('Введенное число не соответствует условиям')
        number = int(input('Введите число больше минимально5го и не превышающее максимальное из последовательности: '))
    else:
        break


def sort(array, left, right):
    if left > right:
        return
    else:
        p = random.choice(array[left:right + 1])
        i, j = left, right
        while i <= j:
            while array[i] < p: i += 1
            while array[j] > p: j -= 1
            if i <= j:
                array[i], array[j] = array[j], array[i]
                i, j = i + 1, j - 1
                sort(array, left, j)
                sort(array, i, right)
        return array


print('Отсортированная последовательность', sort(array, 0, len(array) - 1))


def search(array, number, left, right):
    if left > right:
        return print('Введенное число отсутствует в последовательности')
    middle = (right + left) // 2
    if array[middle] == number:
        if middle == right:
            return middle - 1, right
        else:
            return middle - 1, middle + 1
    elif number < array[middle]:
        return search(array, number, left, middle - 1)
    else:
        return search(array, number, middle + 1, right)


if search(array, number, 0, len(array) - 1):
    result1, result2 = search(array, number, 0, len(array) - 1)
    print('Номер позиции элемента, который меньше введенного пользователем числа', result1)
    print('Номер позиции элемента, который равен или больше введенного пользователем числа', result2)
