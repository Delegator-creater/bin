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

    def crossing_merger(self ,  other_individe, part: float):
        pass

class Genetic_algorithm():

    def __init__(self , list_individes = [] , \
                 mutation_rate : float = 0 , mutation_chance : float = 0 ,elite_part : float= 0, number_eras : int = 0  ):
        self.list_individes   = list_individes   # Список индивидуумов
        '''
        ф-ция приспособленности дожна вернуть список из величин приспособленности индивида

        '''
        self.number_eras     = number_eras       # колличество эпох
        self.mutation_rate   = mutation_rate     # коэффициент мутаций
        self.mutation_chance = mutation_chance   # шанс мутации
        self.eras            = 0                 # текущая эпоха
        self.elite_part      = elite_part        # часть индивидов, которые считаются элитарными

    def start_eras(self , list_points_new : list ):


        print(max(list_points_new))

        list_points = []
        lll_int = 0

        for lll in list_points_new:
            list_points.append(Pair(lll, self.list_individes[lll_int]))
            lll_int += 1

        list_points = sorted(list_points , key = lambda list_points : list_points.first() , reverse= True )
        new_list_individes : list[Individe] = []

        i_int = 0
        part_individes = len(self.list_individes) * self.elite_part

        while (i_int < part_individes):
            new_list_individes.append( list_points[i_int].second() )
            i_int += 1

        i_int -= 1
        i_max = len(self.list_individes) - 1
        while (i_int < i_max):
            new_list_individes.append( \
                Individe(list_points[i_int].second().crossing(list_points[ i_int + 1].second() , 0.5 )))
            i_int += 1

        for i in new_list_individes:
            i.mutation(self.mutation_rate , self.mutation_chance )

        self.list_individes = new_list_individes

        self.eras += 1