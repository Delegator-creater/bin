from scene import *
import os
from Neron_net import *
from pickle import  *
from concurrent.futures import ProcessPoolExecutor
import graph as gr


model = Model(20,4)
model.add_layer(Layer(10 , function_activate_name= "Sigmoid" ))
model.add_LSTM(LSTM(10 ,10 ,10 ))
model.add_layer(Layer(10 , function_activate_name= "Sigmoid"))
model.add_layer(Layer(10 , function_activate_name= "Sigmoid" ))
model.unite()
model.output_layer.edit_edit_alfa_Relu_Improved(0.0001)
model.list_layer[1].edit_edit_alfa_Relu_Improved(0.0001)
model.list_layer[-2].edit_edit_alfa_Relu_Improved(0.0001)
model.list_layer[-3].edit_edit_alfa_Relu_Improved(0.0001)

fiel = open("Отчет.txt" , 'w')

#list_file =
data_lsit = []
j_int = 0
max_ = 1
while (max_ > 0.1 ):
    max_ = 0
    for i in os.listdir('data_set'):
        if ( i.endswith('.bin')):

            string = i[0 : -4 :1]
            new_scena = Scene( 10 , 10 ,'')

            data = []
            time_data = new_scena.load_scena_out_file("data_set/" + string)

            new_scena.list_obj = time_data[1]
            new_scena.matix_obj= time_data[0]

            step = []
            for j in string:
                step.append( int(j) )
            new  = new_scena.lerning_scena(step , 4 , len(string) , model , 0.0001*pow(2 , j_int//100) )
            max_ = new if (new > max_) else max_

            j_int += 1
    string = str(j_int) + ' ' + str(max_)
    fiel.write(string + '\n')
    print(string)

fiel.close()
gr.graph("Отчет.txt")
dump( model , open ("model\model_20_4 v0.3.bin " , 'wb' )  )





