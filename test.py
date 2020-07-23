from scene import *




if __name__ == '__main__':

    scena = Scene(10 , 10 , "")

    open('data.txt' , 'w')
    open('data1.txt', 'w')

    scena.simulation(20 , 20 , 100 , 10000 , lambda x : sin(x/50) , lambda x : sin (x/50 + pi/4))

