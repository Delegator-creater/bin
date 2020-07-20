from tkinter            import *
import time
from pair               import *
from Neron_net          import *
from numpy              import *
from class_obj          import *
from genetic_algorithm  import *
from concurrent.futures import ProcessPoolExecutor

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
        prim = None
        if (self.drawing):
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
            if (type(i.first()) == Food):
                if ( npc.crd == i.first().crd ):
                    npc.eat_food(i.first())
                    #print("eat")
    def if_NPC (self , crd ):
        for i in self.started_list_NPC:
            if (i.first().crd == crd):
                return False
        return True

    def move_NPC(self, angle_step, unit_list_obj: Pair):
        new_crd    = [ 0 , 0]
        new_crd[0] = unit_list_obj.first().crd[0] + angle_step[0]
        new_crd[1] = unit_list_obj.first().crd[1] + angle_step[1]
        if (unit_list_obj.first().status == "live"):
            if (((new_crd[0] >= 0) and (new_crd[0] < self.sizex)) and ((new_crd[1] >= 0) and (new_crd[1] < self.sizey))):
                if (self.if_NPC(new_crd)):
                    unit_list_obj.first().step(angle_step)
                    self.if_food(unit_list_obj.first())
                else:
                    unit_list_obj.first().wait()

                if (self.drawing) :
                    self.c.coords(unit_list_obj.second(), (new_crd[0] - self.x0) / self.s , (new_crd[1] - self.y0) / self.t ,\
                                  (new_crd[0] + 1 - self.x0) / self.s , (new_crd[1] + 1 - self.y0) / self.t)
            else:
                unit_list_obj.first().wait()



    def rotation_obj(self , sin_angle : float , unit_list_obj: Pair ):

        old_angle = unit_list_obj.first().angle
        new_angle = [-old_angle[1] * sin_angle,\
                      old_angle[0] * sin_angle]
        unit_list_obj.first().rotation(new_angle)

    def rotation_NPC(self , angle_step, unit_list_obj: Pair ):
        if (unit_list_obj.first().status == "live"):
            self.rotation_obj(angle_step, unit_list_obj)

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
            self.move_NPC( unit.first().angle ,  unit)
        if (d == 1):
            self.rotation_NPC( 1, unit)
        if (d == 2):
            self.rotation_NPC(-1, unit)
        if (d == 3):
            list_npc = []
            for i in self.started_list_NPC:
                list_npc.append(i.first())
            unit.first().attack_enemy(list_npc)

    def scaning(self, npc: NPC):
        result = [0, 0]
        for i in self.list_obj:
            if ( i.first().exist ):
                crd = [i.first().crd[0] - npc.crd[0],\
                       i.first().crd[1] - npc.crd[1]]
                r      = sqrt(dot(crd , crd))
                angle  = dot(crd , npc.angle)/r
                res    = angle  / (1 + r)
                if (type(i.first()) == Food ):
                    result[1] += res
                if (type(i.first()) == NPC ):
                    result[0] += res
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


        import random
        random.seed()



        self.started_list_NPC : list[Pair ] = []
        self.started_list_Food: list[Pair ] = []

        def init_obj():
            i_int = 0
            if (self.drawing):
                for i in self.list_obj:
                    self.c.delete( i.second() )
            self.list_obj.clear()
            self.started_list_NPC.clear()
            while (i_int < size_NPC):
                triger : bool = True
                new_crd = []
                while (triger):
                    triger = False
                    new_crd = [random.randint(self.sizex // 2, self.sizex - 1), random.randint(0, self.sizey - 1)]
                    for i in self.started_list_NPC:
                        triger = (i.first().crd == new_crd)


                self.add_obj( NPC( [0 , 0] , [1, 0]) ,  new_crd[0]/self.s , new_crd[1]/self.t )
                self.started_list_NPC.append(self.list_obj[-1])
                i_int += 1

            self.started_list_Food.clear()
            i_int = 0
            while (i_int < size_Food):
                triger: bool = True
                new_crd
                while (triger):
                    triger = False
                    new_crd = [random.randint(0, self.sizex // 2 - 1), random.randint(0, self.sizey - 1)]
                    for i in self.started_list_NPC:
                        triger = (i.first().crd == new_crd)
                    for i in self.started_list_Food:
                        triger = (i.first().crd == new_crd)


                self.add_obj(Food([0, 0], [1, 0]), new_crd[0] / self.s, new_crd[1] / self.t )
                self.started_list_Food.append(self.list_obj[-1])
                i_int += 1



        self.list_modeley = []
        i_int = 0
        while ( i_int < size_NPC):
            self.list_modeley.append(Model(2,4))
            self.list_modeley[i_int].add_layer(Layer(10 , function_activate_name= "Relu" , prm_neuron="random"))
            self.list_modeley[i_int].add_LSTM( LSTM(10,10,10))
            self.list_modeley[i_int].add_layer(Layer(10 , function_activate_name= "Relu" , prm_neuron="random"))
            self.list_modeley[i_int].unite()
            self.list_modeley[i_int].output_layer.edit_edit_alfa_Relu_Improved(0.1)
            i_int += 1



        def act():


            triger_life = False
            i_int = 0
            for i in self.started_list_NPC:
                if (i.first().exist):
                    triger_life = True
                    scan        = self.scaning(i.first())
                    result      = self.list_modeley[i_int].result(scan)
                    self.activ_npc( number_max_element(result) , i )
                i_int += 1

            return triger_life

        def tik():
            init_obj()
            step = 0
            start_act = time.time()
            triger_life = True
            while ((step < number_step) and (act())):
                (self.c.update()) if (self.drawing) else None
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

        base = Genetic_algorithm(list_individes= list_individe , mutation_rate= 0.02 ,\
                                 mutation_chance= 0.10, elite_part = 0.1, number_eras=number_epoh )
        angle = 0
        while(base.eras < base.number_eras):
            start = time.time()
            list_points = tik()

            base.start_eras(list_points)


            sin_ = sin( angle/20 )
            base.mutation_chance = 1 * abs(sin_)
            base.mutation_rate   = 0.5 * sqrt(1 - sin_ ** 2)
            angle += 1

            i_int = 0

            for i in self.list_modeley:
                i.determine_model_weights_by_tensor(vector_in_tensor(base.list_individes[i_int].gene , i.get_model_weights_by_tensor()) )
                i_int += 1


            f = open('data.txt' , 'a')
            f.write('all time: '+ str(time.time() - start) + ' seconds.\n')
            f.close()

        file = open('model.txt', 'w')
        for i in base.list_individes:
            file.write( str( i.gene ) + '\n' )
        file.close()