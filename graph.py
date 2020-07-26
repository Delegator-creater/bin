import matplotlib.pyplot as plt
import math as mt

def graph(name_file : str):
    f = open(name_file , 'r')
    x = []
    y = []
    i : float = -100

    for line in f:
        data= line.split(' ')
        x.append(float(data[0]))
        y.append(float(data[1][0:-1:1]))
        i += 1

    plt.plot(x,y)
    plt.show()

def graph_func(func , start :float =0 ,  end : float = 0 , step : float = 0):

    x = []
    y = []
    i = start
    while ( i < end ):
        x.append(i)
        y.append(func(i))
        i += step

    plt.plot(x , y)
    plt.grid()
    plt.show()

#graph("test11.txt")
graph("test21.txt")#
#graph("test31.txt")
#graph("test41.txt")