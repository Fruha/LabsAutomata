import random
import string
import os


class Generator:

    def __init__(self):
        self._prob1 = 0.3
        self._prob2 = 0.6
        self._prob_half = 0.5
        self._prob_noise = 0.9
        self._prob0 = 0.2

    def generateFile(self, file_name, num):
        with open(os.path.join(os.getcwd(), 'tests', file_name), 'w', encoding='utf-8') as file:
            for i in range(num):
                text = f'{self.generateStringWithNoise()}\n'
                file.write(text)

    def generateStringWithNoise(self, a=1, b=6):
        ans = ''
        ans += self.generateNoise()
        ans += self.generateCommand()
        ans += self.generateNoise()
        keys = random.randint(a, b)
        for i in range(keys):
            ans += self.generateSpaces()
            ans += self.generateNoise()
            ans += self.generateKeys()
            ans += self.generateNoise()
        ans += self.generateSpaces()
        return ans

    def generateNoise(self, a=2, b=7):
        letters = random.randint(a, b)
        if random.random() > self._prob_noise:
            return ''.join(random.choices(string.printable[:-10], k=letters))
        else:
            return ''

    def generateCommand(self, a=2, b=10):
        letters = random.randint(a, b)
        return ''.join(random.choices(string.ascii_letters + string.digits + r'./', k=letters))

    def generateKeys(self, a=1, b=5):
        letters = random.randint(a, b)
        return '-' + ''.join(random.choices(string.ascii_letters, k=letters))

    def generateSpaces(self, a=1, b=3):
        letters = random.randint(a, b)
        return ''.join(random.choices(' \t', k=letters))

if __name__ == '__main__':
    gen = Generator()
    gen.generateFile('test100000.txt', 100000)
