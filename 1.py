from tkinter import *
import time
from pair import *
from Neron_net import *
from numpy import *
from class_obj import *
from scene import *


def leng( a ):
    return (dot( a , a ))**(0.5)

class FigureWindow:

    def __init__(self, main_window, w_h_array):  # Создаём окно
        self.main = main_window
        self.window = Toplevel(main_window.master)
        w, h = w_h_array[0], w_h_array[1]
        self.window.geometry("190x165+{}+{}".format(510 + w, h))  # Формируем окно
        self.window.title("Фигура")
        self.window.resizable(False, False)

        self.typeVar = IntVar()  # Переменная
        self.typeVar.set(0)

        self.colors = ["black", "white", "snow", "linen", "lavender", "misty rose", "gray", "blue", "cyan", "yellow",
                       "gold",
                       "coral", "red", "purple", "khaki", "thistle", "indian red"]
        self.outline_color, self.fill_color = self.colors[0], self.colors[1]  # Цвета

        frames, elements = self.window_content(self.window)  # Контект окна
        self.pack_content(frames, elements)  # Упаковка окна
        self.bind_events(elements)  # Подсоединение событий

    def window_content(self, window):  # Заполняем окно
        frame_global = Frame(window)
        frame_dot_one, frame_dot_two, frame_figure, \
        frame_fill_color, frame_outline_color = (Frame(frame_global) for i in range(5))

        x1, y1 = Label(frame_dot_one, text="x1"), Label(frame_dot_one, text="y1")
        x2, y2 = Label(frame_dot_two, text="x2"), Label(frame_dot_two, text="y2")
        self.x1_entry, self.y1_entry = Entry(frame_dot_one, width=5), Entry(frame_dot_one, width=5)
        self.x2_entry, self.y2_entry = Entry(frame_dot_two, width=5), Entry(frame_dot_two, width=5)

        square = Radiobutton(frame_figure, text="Прямоугольник", variable=self.typeVar, value=0)
        oval = Radiobutton(frame_figure, text="Овал", variable=self.typeVar, value=1)

        fill_label = Label(frame_fill_color, text="Заливка: ")
        outline_label = Label(frame_outline_color, text="Грани:     ")
        self.color_fill = Listbox(frame_fill_color, width=210, height=1)
        self.color_outline = Listbox(frame_outline_color, width=210, height=1)
        for i in self.colors:
            self.color_outline.insert(END, i)
            if i == "white":
                self.color_fill.insert(0, i)
            else:
                self.color_fill.insert(END, i)

        draw_button = Button(frame_global, text="Нарисовать фиругу",
                             command=lambda: self.create_figure(
                                 (self.x1_entry, self.y1_entry, self.x2_entry, self.y2_entry)))

        return ((frame_dot_one, frame_dot_two, frame_figure, frame_fill_color, frame_outline_color, frame_global),
                ((x1, self.x1_entry, y1, self.y1_entry), (x2, self.x2_entry, y2, self.y2_entry),
                 (square, oval), (fill_label, self.color_fill), (outline_label, self.color_outline), draw_button))

    def pack_content(self, frames, elements):  # Упаковываем окно
        for i in frames: i.pack()
        for i in range(len(elements)):
            if isinstance(elements[i], tuple):
                length = len(elements[i])
            else:
                length = 1
            for j in range(length):
                if length == 1:
                    elements[i].pack(anchor=N)
                elif i == 2:
                    elements[i][j].pack(anchor=W)
                else:
                    elements[i][j].pack(side=LEFT)

    def bind_events(self, elements):  # Подсоединяем события
        self.color_fill.bind("<FocusIn>", lambda event: self.list_select(self.color_fill))
        self.color_outline.bind("<FocusIn>", lambda event: self.list_select(self.color_outline))
        self.color_fill.bind("<Return>", lambda event: self.list_change_item(self.color_fill))
        self.color_outline.bind("<Return>", lambda event: self.list_change_item(self.color_outline))
        self.color_fill.bind("<FocusOut>", lambda event: self.list_deselect(listbox=self.color_fill))
        self.color_outline.bind("<FocusOut>", lambda event: self.list_deselect(listbox=self.color_outline))
        for i in range(len(elements)):
            if i == len(elements) - 1:
                elements[i].bind("<FocusOut>", lambda event: self.list_deselect(Listbox()))
            elif i == 3 or i == 4:
                pass
            else:
                for j in range(len(elements[i])):
                    elements[i][j].bind("<Button-1>", lambda event: self.list_deselect(Listbox()))

    def list_select(self, listbox):
        listbox["height"] = len(self.colors)
        self.window.geometry("190x{}".format(165 + len(self.colors) * 15))

    def list_deselect(self, listbox):
        if listbox != self.color_fill and listbox != self.color_outline:
            self.color_fill["height"] = 1
            self.color_outline["height"] = 1
        else:
            listbox["height"] = 1
        self.window.geometry("190x165")

    def list_change_item(self, listbox):
        if listbox == self.color_fill:
            self.fill_color = listbox.get(listbox.curselection())
        elif listbox == self.color_outline:
            self.outline_color = listbox.get(listbox.curselection())
        listbox.insert(0, listbox.get(listbox.curselection()))
        listbox.delete(listbox.curselection())
        self.list_deselect(listbox)

    def create_figure(self, elements):
        x1, y1, x2, y2 = (elements[i].get() for i in range(4))
        if self.typeVar.get():
            self.main.canvas.create_oval((x1, y1), (x2, y2), fill=self.color_fill.get(0),
                                         outline=self.color_outline.get(0))
        else:
            self.main.canvas.create_rectangle((x1, y1), (x2, y2), fill=self.color_fill.get(0),
                                              outline=self.color_outline.get(0))
        self.window.destroy()


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

def new_window():
    '''
    Метод создает новое окно редактора.
    Через метод init_scena запрашивает у пользователя, через вспдывающее окно,
    какие параметры сцены задать.
    После отрисовывает сетку(grid_Scene) учитывая масштаб, объекты которые может добавить пользователь
    :return: void
    '''
    a = 400
    b = 600



    #init_scene(scena1)

    root = Tk()
    mainmenu = Menu(root)
    root.config(menu=mainmenu)

    filemenu = Menu(mainmenu, tearoff=0)
    filemenu.add_command(label="Открыть...")
    filemenu.add_command(label="Новый", command=new_window)
    filemenu.add_command(label="Сохранить...")
    filemenu.add_command(label="Выход")

    helpmenu = Menu(mainmenu, tearoff=0)
    helpmenu.add_command(label="Помощь")
    helpmenu.add_command(label="О программе")

    mainmenu.add_cascade(label="Файл", menu=filemenu)
    mainmenu.add_cascade(label="Справка", menu=helpmenu)


    c = Canvas(width=b, height=a, bg='white')
    c.focus_set()
    c.pack()

    scena = Scene(int(20), int(20), 'name_scene', c)



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





    scena.drawing = True
    menu = Menu( tearoff = 0 )
    menu.add_cascade(label = "Добавить.." ,    menu = addmenu)
    menu.add_command(label = "Свойства"   , command = info)
    menu.add_command(label = "Старт"      , command = lambda : scena.simulation(100 , 50 , 100 , 10000 ))



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
