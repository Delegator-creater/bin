from pair import *
import random
random.seed()

class Individe():

    def __init__(self, gene: list = []):
        self.gene = gene

    def mutation(self, mutation_rate: float, chance: float):
        new_gene = []
        for i in self.gene:
            mute = 0
            if (chance >= random.random()):
                mute = (-1) ** (random.randint(0, 1)) * mutation_rate
            new_gene.append(i + mute)
        self.gene = new_gene

    def crossing(self, other_individe, part: float):
        first_part = part * len(self.gene)
        new_gene = []
        i_int = 0
        for i in self.gene:
            if (i_int < first_part):
                new_gene.append(i)
            else:
                new_gene.append(other_individe.gene[i_int])
            i_int += 1
        return new_gene

    def crossing_mixing(self ,  other_individe, part: float):
        new_gene = []
        i_int = 0
        for i in self.gene:
            if (random.random() <= part ):
                new_gene.append( (other_individe.gene[i_int] + i ) / 2 )
            else:
                new_gene.append( i )
            i_int += 1
        return new_gene

class Genetic_algorithm():

    def __init__(self , list_individes = [] , \
                 mutation_rate : float = 0 , mutation_chance : float = 0 ,elite_part : float= 0, number_eras : int = 0  ):
        self.list_individes   = list_individes   # Список индивидуумов
        self.number_eras     = number_eras       # колличество эпох
        self.mutation_rate   = mutation_rate     # коэффициент мутаций
        self.mutation_chance = mutation_chance   # шанс мутации
        self.eras            = 0                 # текущая эпоха
        self.elite_part      = elite_part        # часть индивидов, которые считаются элитарными
        self.strat_crosing   = 'mixing'

    def mutation_popullation(self):
        for i in self.list_individes:
            i.mutation(self.mutation_rate , self.mutation_chance)

    def edit_strat_crosing(self , strat_crosing):
        self.strat_crosing = strat_crosing

    def selection_and_crossing(self , list_points):
        new_list_individes : list[Individe] = []

        i_int = 0
        part_individes = int(len(self.list_individes) * self.elite_part)

        while (i_int < part_individes):
            new_list_individes.append( list_points[i_int].second() )
            i_int += 1

        i_int -= part_individes
        i_max = len(self.list_individes) - part_individes
        while (i_int < i_max):
            if (self.strat_crosing == 'mixing'):
                new_individ = Individe( list_points[i_int].second().crossing_mixing(list_points[i_int + 1].second(), 1)   )
            if (self.strat_crosing == 'crossing'):
                new_individ = Individe( list_points[i_int].second().crossing( list_points[i_int + 1].second()    , 0.5 )  )
            new_list_individes.append( new_individ )
            i_int += 1

        return new_list_individes



    def start_eras(self , list_points_new : list ):

        f = open('data.txt' , 'a')
        ff = open('data1.txt' , 'a')
        f.write(str(sorted(list_points_new , reverse = True)))
        ff.write(str( self.eras )+ ' ' + str( max(list_points_new)) + "\n"   )

        list_points = []
        lll_int = 0

        for lll in list_points_new:
            list_points.append(Pair(lll, self.list_individes[lll_int]))
            lll_int += 1

        list_points = sorted(list_points , key = lambda unite_points : unite_points.first() , reverse= True )

        self.list_individes =  self.selection_and_crossing(list_points)

        self.mutation_popullation()

        self.eras += 1
