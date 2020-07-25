from scene import *
from concurrent.futures import ProcessPoolExecutor

def f1_sin (x):
    return 0.5 * sin(x)

def f2_sin (x):
    return 0.2 * sin(x)

def f3_sin (x):
    return 0.2 * sin(x + pi/4)

def f1_exp (x):
    return exp(x/50)

def test (file_name : str , sizex : int , sizey : int , function_rate_mutation,\
                   function_chance_mutation , model):


    scena = Scene(sizex , sizey , "" )
    scena.simulation(20 , 20 , 100 , 10000 , function_rate_mutation , function_chance_mutation , file_name ,model=model)


if __name__ == '__main__':
    pool = ProcessPoolExecutor(max_workers = 4)
    a = []
    file = open('model_20_4' + '.bin', 'rb')
    data = load(file)
    file.close()
    a.append(pool.submit(test , 'test1' , 10 , 10 , f1_sin , f2_sin , data))
    a.append(pool.submit(test , 'test2' , 10 , 10 , f1_sin , f3_sin , data))
    a.append(pool.submit(test , 'test3' , 10 , 10 , f1_exp , f2_sin , data))
    a.append(pool.submit(test , 'test4' , 10,  10 , sin    , f1_exp , data))

    for i in a:
        i.result()


