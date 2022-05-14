import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import time
import os
import pickle
import json
import zipfile

class Model:
    def __init__(self,data):
        self.data=data
        self.result = []

    def calculate(self):
        Xi = self.data[0]
        Yi = self.data[1]

        def func(p, x):
            k, b = p
            return k * x + b

        def error(p, x, y):
            return func(p, x) - y

        p0 = [1, 20]

        self.result = leastsq(error, p0, args=(Xi, Yi))[0]
        time.sleep(3)
        
    def tabulate(self):
        data = self.data
        result = self.result
        result_string=""
        for co in data.T:
            result_string+=f'{co[0]:.2f}\t{co[1]:.2f}\n'
        result_string+=f'{result[0]:.2f}\t{result[1]:.2f}\n'
        return result_string
        
    def plot(self):
        data = self.data
        result = self.result
        fig=plt.figure()
        plt.scatter(data[0], data[1], label='data')

        x = np.linspace(0, 12, 100)
        y = result[0] * x + result[1]
        plt.plot(x, y, color='tab:orange', label='result')
        plt.legend()
        plt.tight_layout()
        return fig


class Result1:
    def __init__(self,example_flag) -> None:
        self.example_flag=example_flag
        example_folder=data_folder+"/"+example_flag
        input_folder=example_folder+"/input"
        output_folder=example_folder+"/output"
        pickle_folder=example_folder+"/pickle"

        with open(example_folder+"/example.json",'r') as load_f:
            dt_example=json.load(load_f)

        if dt_example["is_load"]:
            with open(pickle_folder+"/model1.pkl", 'rb') as f:
                foo = pickle.load(f)
            print(f"{example_flag} load OK")
        else:
            data = np.loadtxt(input_folder+"/data.txt", delimiter=',')
            foo=Model(data)
            start=time.time()
            foo.calculate()
            print(f"{example_flag} calculate OK (time:{time.time() - start:.3f} seconds)")

        with open(pickle_folder + "/model1.pkl", 'wb') as f:
            pickle.dump(foo, f)
        print(f"{example_flag} backup OK")

        fig=foo.plot()
        fig.savefig(output_folder + "/figure.png")
        plt.close()
        print(f"{example_flag} plot OK")

class Result2:
    def __init__(self,example_flag) -> None:
        self.example_flag=example_flag
        example_folder=data_folder+"/"+example_flag
        input_folder=example_folder+"/input"
        output_folder=example_folder+"/output"
        pickle_folder=example_folder+"/pickle"

        with open(example_folder+"/example.json",'r') as load_f:
            dt_example=json.load(load_f)

        if dt_example["is_load"]:
            with open(pickle_folder+"/model2.pkl", 'rb') as f:
                foo = pickle.load(f)
            print(f"{example_flag} load OK")
        else:
            data = np.loadtxt(input_folder+"/data.txt", delimiter=',')
            foo=Model(data)
            start=time.time()
            foo.calculate()
            print(f"{example_flag} calculate OK (time:{time.time() - start:.3f} seconds)")
        
        with open(pickle_folder + "/model2.pkl", 'wb') as f:
            pickle.dump(foo, f)
        print(f"{example_flag} backup OK")

        with open(output_folder + "/matrix.txt", "w") as f:
            f.write(foo.tabulate())
        print(f"{example_flag} tabulate OK")

if __name__=='__main__':
    data_folder="data"
    zip_folder=data_folder+"/_"
    with open(data_folder+"/data.json",'r') as load_f:
        dt_data=json.load(load_f)
    for key,value in dt_data.items():
        if value:
            example_flag=key
            example_folder=data_folder+"/"+example_flag
            pickle_folder=example_folder+"/pickle"
            output_folder=example_folder+"/output"
            
            if not os.path.exists(pickle_folder):
                os.makedirs(pickle_folder)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            with open(example_folder+"/example.json",'r') as load_f:
                dt_example=json.load(load_f)

            result_dic={
                "result1":Result1,
                "result2":Result2,
            }

            result_class_list=[result_dic[key] for key,value in dt_example["result"].items() if value]

            for result_class in result_class_list:
                result_class(example_flag)

            if dt_example["is_zip"]:            
                current_time=time.strftime('%y%m%d%H%M', time.localtime())

                f = zipfile.ZipFile(zip_folder+'/'+current_time+'_'+example_flag+'.zip','w',zipfile.ZIP_DEFLATED) 
                for dirpath, dirnames, filenames in os.walk(example_folder): 
                    for filename in filenames: 
                        f.write(os.path.join(dirpath,filename)) 
                f.close()
