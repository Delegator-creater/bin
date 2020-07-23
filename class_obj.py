from numpy import *

def leng( a ):
    return (dot( a , a ))**(0.5)

class Obj():

    def __init__(self, crd, angle, color):
        self.crd = crd
        self.angle = angle
        self.color = color
        self.exist = True
        self.block_vision = None

    def moves(self, new_crd):
        self.crd = new_crd

    def rotation(self, new_angle):
        self.angle = new_angle

    def length_to_(self , obj):
        other_crdx = self.crd[0] - obj.crd[0]
        other_crdy = self.crd[1] - obj.crd[1]
        return (other_crdx**2 + other_crdy**2)**(0.5)

    def length(self):
        return (self.crd[0]**2 +self.crd[1]**2)**(0.5)

    def scal(self , obj):
        return float(self.crd[0]*obj.crd[0] + self.crd[1]*obj.crd[1])

    def vector_to(self , obj):
        crd = [0,0]
        crd[0] = obj.crd[0] - self.crd[0]
        crd[1] = obj.crd[1] - self.crd[1]
        return crd

class End_obj(Obj):

    def __init__(self, crd, angle , color = 'blue'):
        super().__init__( crd, angle, color)
        self.block_vision = False

class Food(End_obj):

    def __init__(self , crd , angle):
        super().__init__(crd,angle , color= 'yellow')
        self.block_vision = True


class NPC(Obj):  # subject

    def __init__(self, crd, angle , radius_vision : float = 5 ):
        super().__init__( crd, angle, 'red')
        self.hungry        = 0
        self.energy        = 100
        self.hp            = 100
        self.status        = "live"
        self.radius_vision = radius_vision
        ###
        self.points        = 0
        self.block_vision  = True

    def up_points(self):
        self.points += 1

    def rotation(self, new_angle):
        super().rotation(new_angle)
        self.tik()

    def real_moves(self, new_crd):
        movx = self.crd[0] - new_crd[0]
        movy = self.crd[1] - new_crd[1]
        l = (movx ** 2 + movy ** 2) ** (0.5)
        self.angle = [movx/l , movy/l]
        self.moves( new_crd)

    #test : act
    def tik(self):
        if (self.hungry > 100):
            self.hungry = 100

        if ( ( self.hungry < 100 ) and ( self.hungry >= 0 ) ):
            self.hungry += 10
            if (self.hungry <= 50):
                self.energy += 10
                self.hp += 1

        if (self.hungry >= 100):
            self.hp -= 10

        if ( self.hp <= 0 ):
            self.status = "dead"
            self.exist  = False

        self.up_points()


    def step (self , angle_step): # angle_step нормированный ветор
        new_crdx = self.crd[0] + angle_step[0]
        new_crdy = self.crd[1] + angle_step[1]
        self.moves([new_crdx , new_crdy])
        self.energy -= 2
        self.tik()

    def eat_food(self, food : Food):
        food.exist = False
        self.hungry -=100
        if (self.hungry < 0) :
            self.hungry = 0
        self.energy -= 50
        self.tik()

    #test : passive
    def take_damage(self):
        self.hp -= 50
        if (self.hp <= 0):
            self.status = "dead"
            self.exist  = False


    def attack_enemy(self , list_npc):
        if (self.status != "dead"):
            self.energy -= 10
            for i in list_npc:
                if (i != self) :
                    crd = [ 0 , 0 ]
                    crd[0] = i.crd[0] - self.crd[0]
                    crd[1] = i.crd[1] - self.crd[1]
                    sk = dot( self.angle , crd ) / leng(crd)
                    if (sk == 1):
                        i.take_damage()
            self.tik()

    def wait(self):
        self.tik()

class NPC_AI(NPC):
    pass