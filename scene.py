from tkinter           import *
import time
from pair              import *
from Neron_net         import *
from numpy             import *
from class_obj         import *
from genetic_algorithm import *
from multiprocessing   import Pool
from number_max_element import *



class Scene():

    def __init__(self, sizex : int , sizey : int , name : str , c : Canvas = None ,  list_obj = []):
        self.sizex    = sizex
        self.sizey    = sizey
        self.x0       = 0
        self.y0       = 0
        self.t        = 0.1
        self.s        = 0.1
        self.name     = name
        self.list_obj = list_obj
        self.c        = c
        self.drawing  = False

    def edit_field(self , sizex , sizey , name , list_obj = []):
        self.sizex = sizex
        self.sizey = sizey
        self.name = name
        self.list_obj = list_obj

    def add_obj(self , new_obj , x : int , y : int):
        new_obj.crd = [self.s  * x , self.t * y ]
        prim = self.c.create_rectangle( x , y , x + 1 / self.s , y + 1 / self.t , fill = new_obj.color , tag = 'dinamic') # prim - примитив
        self.list_obj.append(Pair(new_obj , prim))

    def change_crd0(self , x0_new : int , y0_new : int):
        x0 = x0_new
        y0 = y0_new

    def increase_x0(self , delta_x0 : int):
        self.x0 += delta_x0

    def increase_y0(self , delta_y0 : int):
        self.y0 += delta_y0

    def get_sizex(self):
        return self.sizex

    def get_sizey(self):
        return  self.sizey

    def if_food (self , npc : NPC):
        for i in self.list_obj:
            if (type(i) == Food):
                if ( npc.crd == i.crd ):
                    npc.eat_food(i)
                    print("eat")

    def move_NPC(self, angle_step, unit_list_obj: Pair):
        new_crd    = [ 0 , 0]
        new_crd[0] = unit_list_obj.first().crd[0] + angle_step[0]
        new_crd[1] = unit_list_obj.first().crd[1] + angle_step[1]
        if (unit_list_obj.first().status == "live"):
            if (((new_crd[0] >= 0) and (new_crd[0] < self.sizex)) and ((new_crd[1] >= 0) and (new_crd[1] < self.sizey))):
                self.if_food(unit_list_obj.first())
                unit_list_obj.first().step(angle_step)

                if (self.drawing) :
                    self.c.coords(unit_list_obj.second(), (new_crd[0] - self.x0) / self.s , (new_crd[1] - self.y0) / self.t ,\
                                  (new_crd[0] + 1 - self.x0) / self.s , (new_crd[1] + 1 - self.y0) / self.t)
            else:
                unit_list_obj.first().wait()

    def move_objects(self , list_new_crd):

        def move_obj(new_x , new_y , unit_list_obj : Pair ):
            unit_list_obj.first().move([new_x, new_y])
            self.c.coords(unit_list_obj.second() , new_x , new_y , new_x + 1 / self.s , new_y + 1 / self.t  )

        j = 0
        for i in self.list_obj :
            move_obj(list_new_crd[j][0] , list_new_crd[j][1] , i)
            j += 1

    def activ_npc(self, d, unit : Pair):
        if (d == 0):
            self.move_NPC([1, 0],  unit)
        if (d == 1):
            self.move_NPC([0, -1], unit)
        if (d == 2):
            self.move_NPC([-1, 0], unit)
        if (d == 3):
            self.move_NPC([0, 1],  unit)
        if (d == 4):
            list_npc = []
            for i in self.started_list_NPC:
                list_npc.append(i.first())
            unit.first().attack_enemy(list_npc)

    def scaning(self, npc: NPC):
        result = [0, 0]
        for mm in self.started_list_NPC:
            if (mm.first() != npc):
                angle = dot( npc.vector_to(mm.first()), npc.angle)
                if (angle > 0):
                    result[0] += (angle ** 2) / (1 + npc.length_to_(mm.first()))

        for mm in self.started_list_Food:
            if (mm.first().exist):
                angle = dot( npc.vector_to(mm.first()), npc.angle)
                if (angle > 0):
                    result[1] += (angle ** 2) / (1 + npc.length_to_(mm.first()))
        return result

    def simulation(self , size_NPC : int , size_Food : int , number_step : int , number_epoh : int):


        def tensor_in_vector (tensor_3):
            vector: list[float] = []
            for i in tensor_3:
                for j in i:
                    vector += j
            return vector

        def vector_in_tensor (vector : list , example_tensor ):
            prm_tensor = []
            for i in example_tensor:
                prm_tensor.append([len(i),len(i[0])])


            list_matrix = []
            i_int = 0
            j_int = 0
            while ( i_int < len(example_tensor) ):
                new_matrix = []
                while ( len(new_matrix) != prm_tensor[i_int][0] ):
                    new_vector = []
                    while ( len(new_vector) != prm_tensor[i_int][1] ):
                        new_vector.append(vector[j_int])
                        j_int += 1
                    new_matrix.append(new_vector)
                i_int += 1
                list_matrix.append(new_matrix)

            return list_matrix

        pool = Pool()

        self.drawing = False
        import random
        random.seed()

        self.started_list_NPC : list[Pair ] = []
        self.started_list_Food: list[Pair ] = []

        def init_obj():
            i_int = 0
            self.started_list_NPC.clear()
            while (i_int < size_NPC):
                triger : bool = True
                new_crd = []
                while (triger):
                    triger = False
                    new_crd = [random.randint(0, self.sizex), random.randint(0, self.sizey)]
                    for i in self.started_list_NPC:
                        triger = (i.first().crd == new_crd)

                self.started_list_NPC.append(Pair(NPC(new_crd , [1, 0]), None))
                i_int += 1

            self.started_list_Food.clear()
            i_int = 0
            while (i_int < size_Food):
                triger: bool = True
                new_crd
                while (triger):
                    triger = False
                    new_crd = [random.randint(0, self.sizex), random.randint(0, self.sizey)]
                    for i in self.started_list_NPC:
                        triger = (i.first().crd == new_crd)
                    for i in self.started_list_Food:
                        triger = (i.first().crd == new_crd)

                self.started_list_Food.append(Pair(Food(new_crd, [1, 0]), None))
                i_int += 1



        self.list_modeley = []
        i_int = 0
        while ( i_int < size_NPC):
            self.list_modeley.append(Model(2,5))
            self.list_modeley[i_int].add_layer(Layer(10 , function_activate_name= "Relu" , prm_neuron="random"))
            self.list_modeley[i_int].add_LSTM( LSTM(10,10,10))
            self.list_modeley[i_int].add_layer(Layer(10 , function_activate_name= "Relu" , prm_neuron="random"))
            self.list_modeley[i_int].unite()
            self.list_modeley[i_int].output_layer.edit_edit_alfa_Relu_Improved(0.1)
            i_int += 1



        def act():



            time_list_ = []
            for i in self.started_list_NPC:
                time_list_.append(i.first())

            res  = pool.map( self.scaning,\
                             time_list_)

            list_pair_res_and_modeley = []
            i_int = 0
            for i in res:
                list_pair_res_and_modeley.append( Pair(i,self.list_modeley[i_int]) )
                i_int += 1


            list_result = pool.map( second_to_first ,   list_pair_res_and_modeley)


            i_int = 0
            for i in list_result:
                self.activ_npc(number_max_element(i) , self.started_list_NPC[i_int])
                i_int += 1

        def tik():
            init_obj()
            step = 0
            while (step < number_step):
                act()
                step += 1
            list_ind = []



            for ite in self.started_list_NPC:
                list_ind.append( ite.first().points )


            return list_ind

        list_individe = []
        for iterator in self.list_modeley:
            list_individe.append(Individe(\
                tensor_in_vector(\
                    iterator.get_model_weights_by_tensor()\
                    )\
                ))

        base = Genetic_algorithm(list_individes= list_individe , mutation_rate= 0.1 ,\
                                 mutation_chance= 0.3, elite_part = 0.1, number_eras=number_epoh )

        while(base.eras < base.number_eras):
            start = time.time()
            list_points = tik()
            base.start_eras(list_points)
            i_int = 0
            for i in self.list_modeley:
                i.determine_model_weights_by_tensor(vector_in_tensor(base.list_individes[i_int].gene , i.get_model_weights_by_tensor()) )
                i_int += 1
            print('time: ', time.time() - start, ' seconds.')
