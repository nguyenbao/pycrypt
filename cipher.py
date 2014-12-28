__author__ = 'thienbao'

import os
from mcrypt import *

class Cypher(object):

    def __init__(self, key):
        self.key = key
        self.letters = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\] ^_`a bcdefghijklmnopqrstuvwxyz{|}~'
        pass

    def decrypt(self, value):
        return None

    def encrypt(self, value):
        return None

class ReverseCypher(Cypher):

    def encrypt(self, value):
        length = len(value)
        return "".join([ value[index] for index in range(length-1,-1,-1)])

    def decrypt(self, value):
        length = len(value)
        return "".join([ value[index] for index in range(length-1, -1, -1)])

class CeasarCypher(Cypher):

    def encrypt(self, value):
        message = value
        encrypted_list = []
        for c in message:
            if c not in self.letters:
                encrypted_list.append(c)
            else:
                encrypted_list.append(self.letters[(self.letters.index(c) + self.key) % len(self.letters)])

        return "".join(encrypted_list)

    def decrypt(self, value):
        encrypted_message = value
        decrypted_list = []
        for c in encrypted_message:
            if c not in self.letters:
                decrypted_list.append(c)
            else:
                decrypted_list.append(self.letters[(self.letters.index(c)-self.key) % len(self.letters)])

        return "".join(decrypted_list)

class TranspositionCypher(Cypher):

    def encrypt(self, value):
        length = len(value)
        encrypted_list = [ [] for i in range(self.key)]
        for index in range(length):
            c = value[index]
            index_list = index % self.key
            encrypted_list[index_list].append(c)
        for item in encrypted_list:
            print item
        return "".join([ "".join(item) for item in encrypted_list ])

    def decrypt(self, value):
        length = len(value)
        row = length / self.key + 1
        padding = length % self.key
        #print padding
        decrypted_list = [ [] for i in range(row) ]

        for index in range(len(value)):
            c = value[index]
            padding_check = index / row
            index_list = index % row if padding_check < padding else index % (row - 1)
            #print "%c => %d (padding_check=%d)" % (c, index_list, padding_check)
            decrypted_list[index_list].append(c)

        for item in decrypted_list:
            print item

        return "".join([ "".join(item) for item in decrypted_list ])

class AffineCypher(Cypher):

    def encrypt(self, value):
        length = len(self.letters)
        assert gcd(self.key, length) == 1, "key and length of letters is not relative prime. Please choose another key"

        encrypt_func = lambda c: self.letters[(self.letters.index(c) * self.key) % length]
        encrypted_value = [ encrypt_func(c) for c in value ]

        return "".join(encrypted_value)

    def decrypt(self, value):
        length = len(self.letters)
        inverse_key = mod_inverse(self.key, length)
        decrypt_func = lambda c: self.letters[(self.letters.index(c) * inverse_key) % length]
        decrypt_value = [ decrypt_func(c) for c in value]

        return "".join(decrypt_value)

class DetectEnglish(object):

    def __init__(self):
        self.english_words = {}
        upper_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.characters = upper_letter + upper_letter.lower() + " \t\n"

    def load_dictionary(self, filename):
        with open(filename, "r") as in_file:
            for line in in_file:
                line = line.strip()
                words = line.split()
                for word in words:
                    self.english_words[word] = 1


    def get_english_count(self, message):
        message = message.lower()
        message = self.remove_non_letters(message)
        possible_words = message.split()
        if len(possible_words) == 0:
            return 0.0

        matches = 0
        for word in possible_words:
            if word in self.english_words:
                matches += 1

        return float(matches) / len(possible_words)

    def is_english(self, message, word_percentage=20, letter_percentage=85):
        words_match = self.get_english_count(message) * 100 >= word_percentage
        num_letters = len(self.remove_non_letters(message))
        letters_match = float(num_letters) / len(message) * 100 >= letter_percentage

        return words_match and letters_match

    def remove_non_letters(self, message):
        return ''.join([ ch for ch in message if ch in self.characters])

