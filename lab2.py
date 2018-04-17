#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This is implementation of

Розробити програму в якій:
а) реалізовано  пошук 20 слів у невідсортованому масиві.  Оцінити час пошуку (пропорційний кількості порівнянь).
б) відсортувати масив та оцінити час сортування (пропорційний кількості порівнянь та перестановок).
в) реалізовано метод логарифмічного пошуку 20 слів у впорядкованому масиві. Оцінити та вивести час пошуку (пропорційний кількості порівнянь).
г) добавити в масив 10 нових ідентифікаторів не порушуючи впорядкованості. Оцінити час вставки (пропорційний кількості порівнянь та перестановок при вставці).

Масив має розмірність 1000 елементів, заповнений на 90 %.
Вхідними даними можуть бути окремі слова з будь-якого файлу,
рахуючи що всі вони є ідентифікаторами.
Введення елементів масиву та виконання кожного завдання виконується
пунктами меню. Виведення результатів в окремому вікні.
Для кожного випадку підрахувати кількість порівнянь при пошуку,
кількість перестановок при вставці елементів.
Підрахувати середню кількість порівнянь та перестановок.
"""
import os
import random as r
import sys
import time

import loremipsum as lorem



def main():
    """Main function to complete task."""
    AMOUNT_OF_WORDS = 20
    list_of_sentences = []
    while len(list_of_sentences) < AMOUNT_OF_WORDS:
        list_of_sentences += lorem.generate_sentence()[2].split(' ')
    list_of_sentences = list_of_sentences[:AMOUNT_OF_WORDS]
    print("Here is generated list:\n%s" % (list_of_sentences, ))
    searched_word = input("Enter word to search: ")
    amount_of_checks = 0
    start_time = float(time.time())
    print(start_time)

    for n, elem in enumerate(list_of_sentences):
        amount_of_checks += 1
        if elem == searched_word:
            print("You word has %s position." % ((n+1), ))
            break
    else:
        print("There is no such word in list")

    unsorted_search_time  = float(time.time()) - start_time
    print(float(time.time()))
    print(unsorted_search_time)
    time_per_check = unsorted_search_time / amount_of_checks

    print("Unsorted search time: %s" % (unsorted_search_time, ))
    print("Amount of checks: %s" % (amount_of_checks, ))
    print("Time per check: %s" % (time_per_check, ))
    print("*" * 80)

    sorted_list = sorted(list_of_sentences)
    searched_word = input("List was sorted, enter new word to search [old word]: ") or searched_word
    amount_of_checks_sorted = 0
    start_time = float(time.time())

    for n, elem in enumerate(sorted_list):
        amount_of_checks_sorted += 1
        if elem == searched_word:
            print("You word has %s position." % ((n+1), ))
            break
    else:
        print("There is no such word in list")
    sorted_search_time = float(time.time() - start_time)
    sorted_time_per_check = sorted_search_time / amount_of_checks_sorted
    print("Sorted search time: %s" % (sorted_search_time, ))
    print("Amount of checks: %s" % (amount_of_checks_sorted, ))
    print("Time per check: %s" % (sorted_time_per_check, ))
    print("*" * 80)

    search_checks = 0
    def binary_search(seq, t):
        nonlocal search_checks
        min = 0
        max = len(seq) - 1
        while True:
            search_checks += 1
            if max < min:
                return -1
            m = (min + max) // 2
            if seq[m] < t:
                min = m + 1
            elif seq[m] > t:
                max = m - 1
            else:
                return m

    start_time = float(time.time())

    binary_search(sorted_list, searched_word)


    log_search_time = float(time.time() - start_time)
    log_time_per_check = log_search_time / search_checks
    print("Sorted log search time: %s" % (log_search_time, ))
    print("Amount of checks: %s" % (search_checks, ))
    print("Time per check: %s" % (log_time_per_check, ))
    print("*" * 80)


if __name__ == "__main__":
    sys.exit(main())
