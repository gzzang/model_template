import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import time
import os
import pickle


class Model:
    def __init__(self):
        self.data = np.loadtxt('input/data.txt', delimiter=',')
        self.result = []

    def calculate(self):
        start = time.time()
        Xi = self.data[0]
        Yi = self.data[1]

        def func(p, x):
            k, b = p
            return k * x + b

        def error(p, x, y):
            return func(p, x) - y

        p0 = [1, 20]

        self.result = leastsq(error, p0, args=(Xi, Yi))[0]
        time.sleep(3)  # 假装计算时间较长
        print(f'calculate OK (time:{time.time() - start:.3f} seconds)')

    def backup(self):
        path = 'backup/'
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + 'model.pkl', 'wb') as f:
            pickle.dump(self, f)
        print(f'backup OK')

    def output(self):
        data = self.data
        result = self.result
        path = 'output/'

        def tabulate():
            with open(path + 'table_data.txt', "w") as f:
                for co in data.T:
                    f.write(f'{co[0]}\t{co[1]}\n')

            with open(path + 'table_result.txt', "w") as f:
                f.write(f'{result[0]}\t{result[1]}\n')

            print(f'tabulate OK ({result[0]:.3f},{result[1]:.3f})')

        def draft():
            plt.scatter(data[0], data[1], label='data')

            x = np.linspace(0, 12, 100)
            y = result[0] * x + result[1]
            plt.plot(x, y, color='tab:orange', label='result')

            plt.legend()

            plt.savefig(path + 'figure.jpg')
            plt.close()

            print('draft OK')

        if not os.path.exists(path):
            os.makedirs(path)

        tabulate()
        draft()


def calculate():
    foo = Model()
    foo.calculate()
    foo.backup()


def output():
    with open('backup/model.pkl', 'rb') as f:
        foo = pickle.load(f)
    foo.output()


# 计算和输出被分为两部分
# calculate可保存计算结果
calculate()

# 在存在计算结果时（backup/model.pkl），output可单独运行，直接输出结果
output()
