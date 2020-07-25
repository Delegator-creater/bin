from tkinter            import *
import time
from pair               import *
from Neron_net          import *
from class_obj          import *
from genetic_algorithm  import *
from concurrent.futures import ProcessPoolExecutor
from pickle             import *
import copy

from number_max_element import *



class Scene():

    def __init__(self, sizex : int , sizey : int , name : str , c : Canvas = None ,  list_obj = [] , matix_obj = []):
        self.sizex     = sizex
        self.sizey     = sizey
        self.x0        = 0
        self.y0        = 0
        self.t         = 0.1
        self.s         = 0.1
        self.name      = name
        self.list_obj  = list_obj
        self.matix_obj : list[list[list]] = matix_obj
        self.c         = c
        self.drawing   = False
        if (len(self.matix_obj) == 0):
            i = 0
            while (i < self.sizex):
                j = 0
                column = []
                while (j < self.sizey):
                    column.append([])
                    j += 1
                self.matix_obj.append(column)
                i += 1

    def init_matrix(self):
        new_matrix = []
        i = 0
        while (i < self.sizex):
            j = 0
            column = []
            while (j < self.sizey):
                column.append([])
                j += 1
            new_matrix.append(column)
            i += 1
        return new_matrix

    def edit_field(self , sizex , sizey , name , list_obj = []):
        self.sizex = sizex
        self.sizey = sizey
        self.name = name
        self.list_obj = list_obj

    def add_obj(self , new_obj , x : int , y : int):
        new_obj.crd = [int(self.s  * x) , int(self.t * y )]
        prim = None
        if (self.drawing):
            prim = self.c.create_rectangle( x , y , x + 1 / self.s , y + 1 / self.t , fill = new_obj.color , tag = 'dinamic') # prim - примитив
        new_pair = Pair(new_obj , prim)
        self.list_obj.append(new_pair)
        self.matix_obj[new_obj.crd[0]][new_obj.crd[1]].append(new_pair)

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
        for i in self.matix_obj[npc.crd[0]][npc.crd[1]]:
            if (i != None):
                if (type(i.first()) == Food):
                    npc.eat_food(i.first())
                    if (self.drawing):
                        self.c.delete(i.second()) if (i.second() != None) else None
                    #print("eat")

    def if_NPC (self , crd ):
        for i in self.matix_obj[crd[0]][crd[1]]:
            if (i != None):
                if (type(i.first()) == NPC):
                    return False
        return True

    def move_NPC(self, angle_step, unit_list_obj: Pair):
        if (unit_list_obj.first().exist):
            new_crd    = [ 0 , 0]
            old_crd    = unit_list_obj.first().crd
            new_crd[0] = int(unit_list_obj.first().crd[0] + angle_step[0])
            new_crd[1] = int(unit_list_obj.first().crd[1] + angle_step[1])
            if (((new_crd[0] >= 0) and (new_crd[0] < self.sizex)) and ((new_crd[1] >= 0) and (new_crd[1] < self.sizey))):
                if (self.if_NPC(new_crd)):
                    unit_list_obj.first().step(angle_step)

                    self.matix_obj[new_crd[0]][new_crd[1]].append(unit_list_obj)
                    self.matix_obj[old_crd[0]][old_crd[1]].remove(unit_list_obj)

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
        end_point : list[list[float]] = []
        end_point.append( [ npc.radius_vision , 0 ] )
        y = npc.radius_vision
        x = 0
        while (x < npc.radius_vision - 1):
            x += 1
            y = int(sqrt(npc.radius_vision ** 2 - x ** 2))
            end_point.append( [ x , y ] )
            # end_point.append( [ x , -y ] )
            # Для уменьшения вычилений воспользуемся симметрией задачи


        way = []
        for i in end_point:
            i_way         = [ [0 , 0] ]
            i_way_reverse = [ [0 , 0] ]
            k  = i[1]/i[0]
            dx = sqrt(1 / (10 * ( k**2 + 1) )  )
            dy = k * dx
            x  = dx
            y  = dy
            while ( sqrt(x**2 + y**2)<= npc.radius_vision ):
                new_x = round(x)
                new_y = round(y)
                if (i_way.count( [ new_x, new_y ] ) == 0):
                    i_way.append([ new_x, new_y ])
                    if (dy != 0):
                        i_way_reverse.append([ new_x, -new_y ])
                x += dx
                y += dy
            i_way.pop(0)
            i_way_reverse.pop(0)
            way.append(i_way)
            if (dy != 0):
                way.append(i_way_reverse)

        result = []
        for i in way:
            i_result = [0,0]
            triger   = True
            for j in i:
                if (triger):
                    crd_matrix = [ npc.crd[0] + int(j[0]*npc.angle[0] + j[1]*npc.angle[1]),\
                                   npc.crd[1] +int(-j[0]*npc.angle[1] + j[1]*npc.angle[0])]
                    if ((crd_matrix[0] < 0) or (crd_matrix[0] >= self.sizex)):
                        break
                    if ((crd_matrix[1] < 0) or (crd_matrix[1] >= self.sizey)):
                        break

                    for k in self.matix_obj[crd_matrix[0]][crd_matrix[1]]:
                        if (k != None):
                            if (k.first().exist):
                                r = i.index(j)
                                if (type(k.first()) == NPC):
                                    i_result[0] += 1 / (r + 1)

                                if (type(k.first()) == Food):
                                    i_result[1] += 1 / (r + 1)
                                triger = False
                                break
                else :
                    break
            result += i_result
        return result

    def lerning_scena(self , true_step , max_variac_step : int  ,number_step : int  , model : Model , teta):
        if ( len(model.input_layer.list_neuron) == 21 ):
            for i in self.list_obj:
                if ( type(i.first()) == NPC):
                    npc = i.first()
                    unit = i
                    break
            i_int = 0

            count = 0

            while (i_int < number_step):
                res = self.scaning(npc) + [npc.hungry/100 , npc.hp/100]
                result = model.result(res)

                step = []
                j = 0
                while (j < max_variac_step):
                    step.append(1 if (true_step[i_int] == j) else result[j])
                    j += 1

                j = 0
                count_1 = 0
                for i in result:
                    count_1 += (i - step[j] ) ** 2
                    j += 1
                #count_1 /= max(result) if (max(result) != 0) else 1
                count += count_1

                self.activ_npc(true_step[i_int] , unit)
                model.lerning(count *  teta ,step , i_int + 1 )
                i_int += 1
            return sqrt(count)

    def save_scena_in_file(self , name_file : str):
        file = open( name_file + '.bin' , 'wb')
        dump( [self.matix_obj , self.list_obj] , file )

    def load_scena_out_file(self , name_file : str):
        file = open( name_file + '.bin' , 'rb' )
        data = load(file)
        return data

    def clear(self):
        if (self.drawing):
            for i in self.list_obj:
                self.c.delete(i.second())
        self.list_obj = []
        self.matix_obj = self.init_matrix()


    '''def scaning(self, npc: NPC):
        result = [0, 0]
        for i in self.list_obj:
            if ( (i.first().exist) and (i.first() != npc) ):
                crd = [i.first().crd[0] - npc.crd[0],\
                       i.first().crd[1] - npc.crd[1]]
                r      = sqrt(dot(crd , crd))
                angle  = dot(crd , npc.angle)/r
                res    = angle  / (1 + r)
                if ( angle > 0):
                    if (type(i.first()) == Food ):
                        result[1] += res
                    if (type(i.first()) == NPC ):
                        result[0] += res
        return result'''

    def simulation(self , size_NPC : int , size_Food : int , number_step : int , number_epoh : int , function_rate_mutation,\
                   function_chance_mutation , name_file : str , model : Model = None):


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
                    self.c.delete( i.second() ) if (i.second() != None) else 0

            for i in self.matix_obj:
                for j in i:
                    j.clear()
            self.list_obj.clear()
            self.started_list_NPC.clear()
            while (i_int < size_NPC):
                triger : bool = True
                new_crd = []
                while (triger):
                    triger = False
                    new_crd    = [random.randint(self.sizex//2 ,self.sizex - 1 ),random.randint(0 , self.sizey - 1)]
                    new_anglex = random.randint(-1,1)
                    new_angley = 1 if (new_anglex == 0) else 0
                    new_angle  = [ new_anglex  , new_angley]
                    for i in self.matix_obj[new_crd[0]][new_crd[1]]:
                        if ( type(i.first()) == NPC ):
                            triger = True


                self.add_obj( NPC( [0 , 0] , new_angle) ,  new_crd[0]/self.s , new_crd[1]/self.t )
                self.started_list_NPC.append(self.list_obj[-1])
                i_int += 1

            self.started_list_Food.clear()
            i_int = 0
            while (i_int < size_Food):
                triger: bool = True
                new_crd
                while (triger):
                    triger = False
                    new_crd = [random.randint(0 ,self.sizex//2 -1 ),random.randint(0 , self.sizey - 1)]
                    for i in self.matix_obj[new_crd[0]][new_crd[1]]:
                        if (type(i.first()) == NPC):
                            triger = True
                    for i in self.matix_obj[new_crd[0]][new_crd[1]]:
                        if (type(i.first()) == Food):
                            triger = True


                self.add_obj(Food([0, 0], [1, 0]), new_crd[0] / self.s, new_crd[1] / self.t )
                self.started_list_Food.append(self.list_obj[-1])
                i_int += 1



        self.list_modeley = []
        i_int = 0
        while ( i_int < size_NPC):
            self.list_modeley.append(copy.deepcopy(model))
            i_int += 1



        def act():


            triger_life = False
            i_int = 0
            for i in self.started_list_NPC:
                if (i.first().exist):
                    triger_life = True
                    scan        = self.scaning(i.first())
                    result      = self.list_modeley[i_int].result(scan +[i.first().hungry/100 , i.first().hp/100])
                    self.activ_npc( number_max_element(result) , i )
                else:
                    self.c.delete(i.second()) if (i.second() != None) else None
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

        base = Genetic_algorithm(list_individes= list_individe , mutation_rate= 0.001 ,\
                                 mutation_chance= 0.01, elite_part = 0.05, number_eras=number_epoh )
        angle = 0

        files = [name_file + '.txt' ,\
                 name_file + '1.txt',\
                 name_file + 'model.txt']

        for i in files:
            open(i,'w')

        while(base.eras < base.number_eras):
            start = time.time()
            list_points = tik()

            base.start_eras(list_points)



            base.mutation_chance = function_chance_mutation(angle)
            base.mutation_rate   = function_rate_mutation(angle)
            angle += 1

            i_int = 0

            for i in self.list_modeley:
                i.determine_model_weights_by_tensor(vector_in_tensor(base.list_individes[i_int].gene , i.get_model_weights_by_tensor()) )
                i_int += 1

            data = []
            for i in files:
                data.append( open(i,'a') )

            data[0].write(str(base.list_individes[0].gene)+'all time: '+ str(time.time() - start) + ' seconds.\n')
            point = 0
            for i in self.started_list_NPC:
                point = i.first().points if (i.first().points > point) else point
            data[1].write( str(base.eras) + ' ' + str(point) + '\n')

            for i in data:
                i.close()

        ff = open(files[2] , 'a')
        for i in base.list_individes:
            ff.write( str( i.gene ) + '\n' )
        ff.close()