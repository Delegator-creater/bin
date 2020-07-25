'''
В этом файле я пробую реализовать класс neuron и
класс layer.
'''

from pair import *
import math as mt
import numpy as np


class Neuron():
    '''
    prm может принимать следующие значения:

    random - связи(веса) входящие в нейрон определяються случайными числами.

    null   - связи(веса) входящие в нейрон определяються нулями.

    normal - связи(веса) входящие в нейрон опредяються так, чтобы при определении
             нескольких одиннаковых сетей , набор весов равномерно заполнили простравнство
             значений вессов[ Не реализованно ].

    value -

    input  - в нейрон не входят связи, значения нейрона определяется из вне.

    neuron_bias - нейрон смещения. если True, то нейрон считается как нейрон смещения
    '''
    def __init__(self , prm : str , function_activate_name : str , value = 0 , neuron_bias : bool = False):
        self.neuron_bias = neuron_bias
        self.value = value
        self.list_of_weights = []
        self.alfa_Relu_Improved = 0
        self.prm = prm
        self.function_activate = None
        self.function_activate_name = function_activate_name
        self.count = 0
        self.delta = 0

        if (neuron_bias) :
            self.count = 1
        if (function_activate_name == 'Relu'):
            self.function_activate            = self.Relu
            self.derivative_function_activate = self.derivative_Relu
        if (function_activate_name == 'Relu_Improved'):
            self.function_activate            = self.Relu_Improved
            self.derivative_function_activate = self.derivative_Relu_Improved
        if (function_activate_name == 'Sigmoid'):
            self.function_activate            = self.Sigmoid
            self.derivative_function_activate = self.derivative_Sigmoid
        if (function_activate_name == 'Tanh'):
            self.function_activate            = self.Tanh
            self.derivative_function_activate = self.derivative_Tanh

    def edit_alfa_Relu_Improved(self, value):
        self.alfa_Relu_Improved = value

    def Relu(self , x):
        return x if (x >= 0) else 0

    def derivative_Relu(self , x):
        return 1 if (x >= 0) else 0

    def Relu_Improved(self , x):
        return 0 if (x < 0) else ( self.alfa_Relu_Improved * (x-1) + 1 if (x > 1) else x )

    def derivative_Relu_Improved(self , x):
        return 0 if (x < 0) else ( self.alfa_Relu_Improved  if (x > 1) else 1 )

    def Sigmoid(self , x):
        return 1/(1 + np.exp(-x, dtype= np.float_))

    def derivative_Sigmoid(self , x):
        return  self.Sigmoid(x) * ( 1 - self.Sigmoid(x) )

    def Tanh(self, x):
        return np.tanh(x, dtype= np.float_)

    def derivative_Tanh(self , x):
        return  1 - self.Tanh(x) ** 2

    def add_relations(self , neuron , weights : float = 0 , serial_number : int = 0 ):
        if (( weights == 0 ) and ( not(self.neuron_bias) )):

            if (self.prm == 'random'):
                import random
                random.seed()
                weights = random.random()

            if (self.prm == 'null'):
                weights = 0

            if (self.prm == 'normal'):
                pass

            if (self.prm == "value"):
                weights = self.value

            self.list_of_weights.append(Pair(weights,neuron))

    def activate(self , count : float = None):
        if (not(self.neuron_bias)):
            self.count = 0
            if (self.prm == 'input'):
                self.count = count
            else:
                for i in self.list_of_weights :
                    self.count += i.first()*i.second().count
                self.argum = self.count
                self.count = self.function_activate(self.count)
        else:
            self.count = 1


    def stochastic_gradient_descent_output(self , value ):
        self.delta = value - self.count

    def stochastic_gradient_descent(self , value):
        self.delta += value

class Layer():

    def __init__(self , number_neuron : int , function_activate_name : str = "Relu" , prm_layer = 'standart' , prm_neuron = 'null' , value_weights = 0):
        if (prm_layer == 'input'):
            prm_neuron = prm_layer
        self.prm_layer = prm_layer
        self.list_neuron = []
        self.next_layer = None

        i = 0
        while (i < number_neuron):
            self.list_neuron.append( Neuron(prm_neuron , function_activate_name , value_weights) )
            i += 1

        if (self.prm_layer != "output"):
            self.list_neuron.append(Neuron(prm_neuron , function_activate_name , value_weights , neuron_bias= True))

    def edit_edit_alfa_Relu_Improved(self, value : float):
        for i in self.list_neuron:
            i.edit_alfa_Relu_Improved(value)

    def connect_layers( self , input_layer  ):
        if (self.prm_layer != 'input'):
            input_layer.next_layer = self
            for i in self.list_neuron:
                for j in input_layer.list_neuron:
                    i.add_relations(j)

    def pass_values(self , values):
        if (  len(values)  ==  len(self.list_neuron) - 1  ):
            i = 0
            while ( i < len(values) ):
                self.list_neuron[i].count = values[i]
                i += 1

    def activate(self):
        if (self.prm_layer != 'input'):
            for i in self.list_neuron:
                i.activate()
        if (self.next_layer != None):
            self.next_layer.activate()

    def get_result(self):
        result = []
        for i in self.list_neuron:
            if (i.neuron_bias):
                break
            result.append(i.count)
        return result

    def get_matrix_weights(self):
        matrix = []
        for j in self.list_neuron:
            if (not (j.neuron_bias)):
                vector = []
                for i in j.list_of_weights:
                    vector.append(i.first())
                matrix.append(vector)
        return matrix

    def determinate_layer_weights_by_tensor(self, tensor):
        j_int = 0
        for j in self.list_neuron:
            if (not (j.neuron_bias)):
                i_int = 0
                for i in j.list_of_weights:
                    i.edit_first(tensor[j_int][i_int])
                    i_int += 1
            j_int += 1

    def stochastic_gradient_descent_output(self , value : list ):
        i_int = 0
        for i in self.list_neuron:
            i.stochastic_gradient_descent_output( value[i_int] )
            i_int += 1

    def stochastic_gradient_descent(self):
        for i in self.list_neuron:
            for j in i.list_of_weights:
                if (j.second().neuron_bias):
                    continue
                j.second().stochastic_gradient_descent(j.first() * i.delta)

    def balance_correction(self , teta : float):
        for i in self.list_neuron:
            for j in i.list_of_weights:
                j.edit_first(   j.first() + teta*i.delta*i.derivative_function_activate(i.argum) * j.second().count  )

    def null_delta(self):
        for i in self.list_neuron:
            i.delta = 0

class Model():

    def __init__(self , size_input : int , size_output : int , prm_output_neuron = "random" , value_weights = 0):
        self.output_layer = Layer(size_output , 'Sigmoid' , prm_neuron =  prm_output_neuron , prm_layer= "output" , value_weights = value_weights)
        self.input_layer  = Layer(size_input  , 'Relu_Improved' , prm_layer  =  'input' )
        self.list_layer   = []
        self.list_layer.append(self.input_layer)
        self.tensor_step_count  = 0 #Кол-во возможных вариаций тензора 3-го ранга весов при использованаи заранее известного шага

    def add_layer(self , layer : Layer):
        self.list_layer.append(layer)

    def add_LSTM(self , lstm ):
        self.list_layer.append(lstm)

    def unite(self):
        self.list_layer.append(self.output_layer)
        i = 1
        while ( i < len( self.list_layer ) ):
            if (type(self.list_layer[i - 1]) == LSTM ):
                self.list_layer[ i ].connect_layers(self.list_layer[ i - 1].output)
            else:
                self.list_layer[ i ].connect_layers(self.list_layer[ i - 1 ])
            i += 1

    def get_model_weights_by_tensor(self):
        self.list_matrix = []
        for k in self.list_layer:
            if (k != self.input_layer):
                if ( type(k) != LSTM ):
                    self.list_matrix.append(k.get_matrix_weights())
                else:
                    m = k.get_tensor_weights()
                    for i in m:
                        self.list_matrix.append(i.copy())
        return self.list_matrix

    def determine_model_weights_by_tensor(self , tensor):
        k_int = 0
        for k in self.list_layer:
            if (k != self.input_layer):
                if ( type(k) != LSTM ):
                    k.determinate_layer_weights_by_tensor(tensor[k_int])
                    k_int += 1
                else:
                    new_list = []
                    l_int = 0
                    while (l_int < 5):
                        new_list.append(tensor[k_int])
                        k_int += 1
                        l_int += 1
                    k.determine_model_weights_by_tensor(new_list)

    def result(self, value):
        if ( len(self.input_layer.list_neuron) - 1 == len(value) ):
            self.input_layer.pass_values(value)
            self.input_layer.next_layer.activate()
            return self.output_layer.get_result()
    #Метод не используется!
    def get_list_tensors(self, n : int ,  r : float , base : list):
        '''
        Метод возвращает список тензоров 3-го ранга T_ijk ( i = 1 , 2 , ... I ; j = 1 , 2 , ... J ; k = 1 , 2 , ... ,K)
        таких, что набор векторов (w111, w211 , ... , w_IJK) равномерно заполняют пространство в R^(I + J + K),
        и любая компонента этих векторов w_ijk in [ base_ijk - r ; base_ijk + r ).
        для каждого полуинтервала [ base_ijk - r ; base_ijk + r ) существует "n" w_ijk принадлежащих этому отрезку,
        таких что |w_ijkl - w_ijk(l + 1)| = 2r/n , l = 1 , 2 , ... , n - 1
        :param n: n = len(list[T_ijk])/(IJK)
        :param base: T_ijk
        :param r: радиус окрестности, r > 0
        :return: list[T_ijk]
        '''
        r = abs(r)
        step : float = 2*r/n
        list_T : list = []
        base_modif = []
        k_int = 0
        while(k_int < len(base)):
            matrix = []
            j_int = 0
            while( j_int < len(base[k_int])):
                vector = []
                i_int = 0
                while(i_int < len(base[k_int][j_int])):
                    vector.append(base[k_int][j_int][i_int] - r)
                    i_int += 1
                j_int += 1
                matrix.append(vector)
            base_modif.append(matrix)
            k_int += 1

        k_int = 0
        while(k_int < len(base_modif)):
            j_int = 0
            while( j_int < len(base_modif[k_int])):
                i_int = 0
                while(i_int < len(base_modif[k_int][j_int])):
                    l: int = 0
                    while (l < n):
                        base_modif[k_int][j_int][i_int] += l * step
                        list_T.append(base.copy())
                        l += 1
                    i_int += 1
                j_int += 1
            k_int += 1

        return  list_T

    def lerning(self , teta : float , true_values : list , n_iter_LSTM : int = 1):
        self.output_layer.stochastic_gradient_descent_output( true_values )

        i_int = len( self.list_layer ) - 1
        while (i_int > 0):
            if ( type(self.list_layer[i_int]) == Layer):
                self.list_layer[i_int - 1].null_delta() if ( type(self.list_layer[i_int - 1]) == Layer ) else \
                    self.list_layer[i_int - 1].output.null_delta()
                self.list_layer[i_int].stochastic_gradient_descent()
                self.list_layer[i_int].balance_correction(teta)
            if (type(self.list_layer[i_int])  == LSTM):
                self.list_layer[i_int - 1].null_delta()
                j = 0
                while ( j < n_iter_LSTM):
                    self.list_layer[i_int].stochastic_gradient_descent(j , teta)
                    j += 1
            i_int -= 1

class LSTM():
    '''Схема:
                                                    h_t
                                                     ^
                                                     |
    С_t-1--->(x)--------------->(+)-------------v->| |  |--> C_t
              ^                  |        №2 (tanh)  |
              |         +------>(x)             V    |
              |  №1     |  №2   | №1      +--->(X)   |
          (sigmoid) (sigmoid) (tanh) (sigmoid)  \    |
    h_t-1----+----------+-------+--------+ №3   \----+----> h_t
             |
        x_t--|
    '''
    def __init__(self,  size_x : int , size_C : int , size_h : int  , prm_neuron : str = "random" , value_wights : float = 0 ):
        self.sigmoid_1 = Layer(size_C ,             function_activate_name= "Sigmoid"  , prm_neuron=prm_neuron , value_weights=value_wights)
        self.sigmoid_2 = Layer(size_C ,             function_activate_name= "Sigmoid"  , prm_neuron=prm_neuron , value_weights=value_wights)
        self.sigmoid_3 = Layer(size_h ,             function_activate_name= "Sigmoid"  , prm_neuron=prm_neuron , value_weights=value_wights)
        self.tanh_1    = Layer(size_C ,             function_activate_name= "Tanh"     , prm_neuron=prm_neuron , value_weights=value_wights)
        self.tanh_2    = Layer(size_h ,             function_activate_name= "Tanh"     , prm_neuron=prm_neuron , value_weights=value_wights)
        self.output    = Layer(size_h ,             prm_layer= "input")

        '****'
        self.erorr_C = None
        self.erorr_h = None
        '****'


        self.h = []
        i = 0
        while (i < size_h):
            self.h.append(0)
            i += 1

        self.C = []
        i = 0
        while (i < size_C):
            self.C.append(0)
            i += 1

        self.input_1 = Layer(size_h + size_x , prm_layer="input")
        self.input_2 = Layer(size_C,           prm_layer="input")

        self.sigmoid_1.connect_layers(self.input_1)
        self.sigmoid_2.connect_layers(self.input_1)
        self.sigmoid_3.connect_layers(self.input_1)
        self.tanh_1.connect_layers(   self.input_1)
        self.tanh_2.connect_layers(   self.input_2)

    def clear_memory(self):
        for i in self.C:
            i = 0
        for i in self.h:
            i = 0

    def activate(self):

        self.input_1.pass_values(self.h + self.connects_layer.get_result())
        self.sigmoid_1.activate()
        C_step_1 = []
        i_int = 0
        for i in self.C:
            C_step_1.append(i*self.sigmoid_1.list_neuron[i_int].count)
            i_int += 1
        self.sigmoid_2.activate()
        self.tanh_1.activate()
        i_int = 0
        for i in self.tanh_1.list_neuron:
            if ( i.neuron_bias ):
                break
            C_step_1[i_int] += i.count * self.sigmoid_2.list_neuron[i_int].count
            i_int += 1

        self.C =  C_step_1

        self.input_2.pass_values(self.C)
        self.tanh_2.activate()
        self.sigmoid_3.activate()

        self.h = []
        i_int = 0
        for i in self.tanh_2.list_neuron:
            if ( i.neuron_bias ):
                break
            self.h.append(i.count * self.sigmoid_3.list_neuron[i_int].count)
            i_int += 1

        self.output.pass_values(self.h)
        self.output.next_layer.activate()

    def get_result(self , input_x):
        self.activate(self.C , input_x , self.h)

    def connect_layers(self , layer : Layer):
        self.connects_layer = layer
        layer.next_layer = self

    def get_tensor_weights(self):
        tensor_weights = []

        tensor_weights.append(self.sigmoid_1.get_matrix_weights())
        tensor_weights.append(self.sigmoid_2.get_matrix_weights())
        tensor_weights.append(self.sigmoid_3.get_matrix_weights())

        tensor_weights.append(self.tanh_1.get_matrix_weights())
        tensor_weights.append(self.tanh_2.get_matrix_weights())

        return tensor_weights

    def determine_model_weights_by_tensor(self , tensor):
        if (len(tensor) == 5 ):
            self.sigmoid_1.determinate_layer_weights_by_tensor(tensor[0])
            self.sigmoid_2.determinate_layer_weights_by_tensor(tensor[1])
            self.sigmoid_3.determinate_layer_weights_by_tensor(tensor[2])
            self.tanh_1.determinate_layer_weights_by_tensor(tensor[3])
            self.tanh_2.determinate_layer_weights_by_tensor(tensor[4])
        else:
            print("Erorr, size tensor it's not format") #?

    def stochastic_gradient_descent(self , n : int  , teta : float ):
        i_int = 0
        self.sigmoid_1.null_delta()
        self.sigmoid_2.null_delta()
        self.sigmoid_3.null_delta()
        self.input_2.null_delta()
        self.input_1.null_delta()
        self.tanh_1.null_delta()
        self.tanh_2.null_delta()
        for i in self.tanh_2.list_neuron:
            if (i.neuron_bias):
                break
            i.delta = self.output.list_neuron[i_int].delta if ( n == 0) else self.erorr_h[i_int]
            self.sigmoid_3.list_neuron[i_int].delta = self.output.list_neuron[i_int].delta if ( n == 0) else self.erorr_h[i_int]
            i_int += 1


        self.tanh_2.stochastic_gradient_descent()
        erorr_tanh_2 = []


        for i in self.input_2.list_neuron:
            if (i.neuron_bias):
                break
            erorr_tanh_2 .append( i.delta)



        i_int = 0
        for i in self.tanh_1.list_neuron:
            if (i.neuron_bias):
                break
            i.delta = erorr_tanh_2[i_int]
            i_int += 1

        i_int = 0
        for i in self.sigmoid_2.list_neuron:
            if (i.neuron_bias):
                break
            i.delta = erorr_tanh_2[i_int]
            i_int += 1

        i_int = 0
        for i in self.sigmoid_1.list_neuron:
            if (i.neuron_bias):
                break
            i.delta = erorr_tanh_2[i_int]
            i_int += 1




        self.input_1  .null_delta()
        self.tanh_1   .stochastic_gradient_descent()
        self.sigmoid_3.stochastic_gradient_descent()
        self.sigmoid_2.stochastic_gradient_descent()
        self.sigmoid_1.stochastic_gradient_descent()

        self.erorr_h : list = []
        i_int = 0
        while (  i_int < len(self.h)  ):
            self.erorr_h.append(self.input_1.list_neuron[i_int].delta)
            i_int += 1

        self.connects_layer.null_delta() if (n == 0) else None

        for i in self.connects_layer.list_neuron:
            if (i.neuron_bias):
                break
            i.delta += self.input_1.list_neuron[i_int].delta
            i_int += 1

        self.tanh_1.balance_correction(teta)
        self.tanh_2.balance_correction(teta)
        self.sigmoid_3.balance_correction(teta)
        self.sigmoid_2.balance_correction(teta)
        self.sigmoid_1.balance_correction(teta)





