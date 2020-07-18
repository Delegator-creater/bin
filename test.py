from scene import *


if __name__ == '__main__':

    scena = Scene(10 , 10 , "")

    open('data.txt' , 'w')

    scena.simulation(20 , 5 , 50 , 10000 )


