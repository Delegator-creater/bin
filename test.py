from scene import *


if __name__ == '__main__':

    scena = Scene(20 , 20 , "")

    open('data.txt' , 'w')
    open('data1.txt', 'w')

    scena.simulation(100 , 50 , 100 , 10000 )


