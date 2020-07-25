from tkinter import *
import time
from pair import *
from Neron_net import *
from numpy import *
from class_obj import *
from scene import *
from pickle import *


def leng( a ):
    return (dot( a , a ))**(0.5)


def grid_Scene(x0 : int , y0 : int , a : int , b : int , s : float , t : float , scene : Scene, canv : Canvas):
    x_other = x0
    y_other = y0
    x = 0
    y = 0
    # horizontal
    while y < (scene.get_sizey()- y0)/t :
        y = (y_other - y0)/t
        canv.create_line( -x0/s , y , (scene.get_sizex() - x0)/s , y , tag = "dinamic")
        y_other+=1
    #vertical
    while x < (scene.get_sizex() - x0)/s:
        x = (x_other - x0) / s
        canv.create_line( x , -y0/t , x , (scene.get_sizey()- y0)/t ,  tag = "dinamic")
        x_other += 1

def init_scene(scene_new):
    pass

triger_add = True

x_event = 0
y_event = 0

def pup( func , arg):
    def pup_one( func_one , arg_one):
        return func_one(arg_one)
    if (type(func) == list):
        result = []
        for i,j in func,arg:
            result.append( pup_one(i,j) )
        return result
    else:
        return pop_one(func,arg)

def new_window():
    '''
    Метод создает новое окно редактора.
    Через метод init_scena запрашивает у пользователя, через вспдывающее окно,
    какие параметры сцены задать.
    После отрисовывает сетку(grid_Scene) учитывая масштаб, объекты которые может добавить пользователь
    :return: void
    '''
    root = Tk()
    mainmenu = Menu(root)
    root.config(menu=mainmenu)

    a = 400
    b = 600

   #''''win_info = Toplevel(root)
    #win_info.title("Новая сцена")
    #win_info.minsize(width=200, height=100)
    #lab_info = Label(win_info, text="Введите название сцены:")
    #ent_info_1 = Entry(win_info, width=20, bd=3)
    #lab_info = Label(win_info, text="Введите высоту сцены:")
    #ent_info_2 = Entry(win_info, width=20, bd=3)
    #lab_info = Label(win_info, text="Введите ширину сцены:")
    #ent_info_3 = Entry(win_info, width=20, bd=3)
    #bot_info   = Button(win_info ,command = lambda : (  ))
    #bor_info["text"] = "Подтвердить"'''



    c = Canvas(width=b, height=a, bg='white')
    c.focus_set()
    c.pack()


    #init_scene(scena1)







    scena = Scene(int(20), int(20), 'name_scene', c)

    def save_scene():
        new_win = Toplevel(root)
        new_win.title('Сохранить...')
        new_win.minsize(width= 200 , height= 100)
        def sav ():
            scena.save_scena_in_file(entr_save.get())
            new_win.destroy()
        save_button = Button( new_win ,command = sav )

        lab_save    = Label(new_win , text = "Введите название файла")
        entr_save   = Entry(new_win , width = 20 , bd = 3)
        save_button["text"] = "Сохранить"

        lab_save   .pack()
        entr_save  .pack()
        save_button.pack()





    filemenu = Menu(mainmenu, tearoff=0)
    filemenu.add_command(label="Открыть...")
    filemenu.add_command(label="Новый"        ,command= scena.clear)
    filemenu.add_command(label="Сохранить..." ,command= save_scene )
    filemenu.add_command(label="Выход")

    helpmenu = Menu(mainmenu, tearoff=0)
    helpmenu.add_command(label="Помощь")
    helpmenu.add_command(label="О программе")

    mainmenu.add_cascade(label="Файл", menu=filemenu)
    mainmenu.add_cascade(label="Справка", menu=helpmenu)






    def popup(event):
        global x_event , y_event
        x_event = event.x
        y_event = event.y
        menu.post(event.x_root, event.y_root)


    def add_NPC():
        scena.add_obj( NPC( [ 0 , 0 ] , [ 1 , 0 ] ) , (x_event // 10)*10 , (y_event // 10) * 10 )

    def add_Object():
        scena.add_obj( End_obj( [ 0 , 0 ] , [ 1 , 0 ] ) , (x_event // 10)*10 , (y_event // 10) * 10 )

    def add_Food():
        scena.add_obj(Food([0, 0], [1, 0]), (x_event // 10) * 10, (y_event // 10) * 10)


    addmenu = Menu(tearoff = False)
    #menu.add_command(label = "" , command = metod) Шаблон
    addmenu.add_command(label="NPC", command = add_NPC)
    addmenu.add_command(label = "Object" , command = add_Object)
    addmenu.add_command(label = "Food"   , command = add_Food)

    def info():
        pass

    file = open('model_20_4' + '.bin', 'rb')
    scena.drawing = True
    menu = Menu( tearoff = 0 )
    menu.add_cascade(label = "Добавить.." ,    menu = addmenu)
    menu.add_command(label = "Свойства"   , command = info)
    menu.add_command(label = "Старт"      , command = lambda : scena.simulation(50 , 50 , 100 , 10000 , lambda x : 0.5*sin(x/50) , lambda x : 0.5*sin (x/50 + pi/4) , \
                                                                                'test' , model = load(file) ))



    def lock(event):
        pass



    #c.create_line()

    s = 0.1
    t = 0.1
    grid_Scene(0,0,400,600,s,t,scena,c)

    # Методы для биндов #
    def up(event):
        c.move('dinamic', 0, +2/scena.s)
        scena.y0 += -20 * scena.s

    def down(event):
        c.move('dinamic', 0 , -2/scena.s)
        scena.y0 +=  20 * scena.s

    def left(event):
        c.move('dinamic', 2/scena.t , 0)
        scena.x0 += -20 * scena.t

    def right(event):
        c.move('dinamic', -2/scena.t , 0)
        scena.x0 += 20 * scena.t

    # Бинды #
    c.bind("<Button-3>", popup)
    c.bind('<Up>', up)
    c.bind('<Down>', down)
    c.bind('<Left>',  left)
    c.bind('<Right>', right)
    #c.bind()

    root.mainloop()

new_window()
print("End")
