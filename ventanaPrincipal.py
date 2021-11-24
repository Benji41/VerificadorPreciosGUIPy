from PIL import ImageTk, Image
import tkinter
import mysql.connector
from mysql.connector import errorcode
import urllib.request

import io
codigo = ""

ventana = tkinter.Tk()
ventana.attributes('-fullscreen', True)
def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'


path = 'img/logo.png'
img = ImageTk.PhotoImage(Image.open(path))
logo= tkinter.Label(ventana, image = img)
logo.place(relx=0.5,rely=0.25,anchor='s')

path2 = 'img/barcode-scan.gif'
img2 = ImageTk.PhotoImage(Image.open(path2))
scan= tkinter.Label(ventana, image = img2)
scan.place(relx=0.5,rely=0.75,anchor='s')


lbSaludo1 = tkinter.Label(ventana,text="Por favor pase el codigo de barras por debajo del escaner",fg=rgbtohex(r=255, g=179, b=0),bg=rgbtohex(r=60, g=179, b=113),font=("Nunito", 30))
lbSaludo1.place(relx=0.5,rely=0.35,anchor='s')

lbSaludo2 = tkinter.Label(ventana,text="¡Busque el codigo de barra de su producto y lleveselo!",fg=rgbtohex(r=105, g=105, b=105),bg=rgbtohex(r=60, g=179, b=113),font=("Nunito", 30))
lbSaludo2.place(relx=0.5,rely=0.45,anchor='s')


def fun(event):
    global codigo
    path3 = ''
    if(event.keysym=='Return'):
        lbSaludo1.place_forget()
        lbSaludo2.place_forget()
        scan.place_forget()
        logo.place(relx=0.9,rely=0.05,anchor='ne')

        lbSaludo3 = tkinter.Label(ventana,text="¡Siga comprando más por menos!",fg=rgbtohex(r=105, g=105, b=105),bg=rgbtohex(r=60, g=179, b=113),font=("Nunito", 30))
        lbSaludo3.place(relx=0.5,rely=0.95,anchor='s')
        


        try:
            conn = mysql.connector.connect(
                        user='root', 
                        password='',
                        host='localhost',
                        database='verificador_precios2'
                    )
            cursor = conn.cursor()

            query = "SELECT * FROM productos WHERE producto_codigo = "+codigo
            cursor.execute(query)
            myresult = cursor.fetchall()
            if myresult:

                path3='img/exito.png'
                img3 = ImageTk.PhotoImage(Image.open(path3))
                imgRes= tkinter.Label(ventana, image = img3)
                imgRes.place(relx=0.15,rely=0.08,anchor='n') 

                lbS= tkinter.Label(ventana,text="¡Busqueda exitosa!",fg="green",bg=rgbtohex(r=60, g=179, b=113),font=("Nunito", 30))
                lbS .place(relx=0.5,rely=0.15,anchor='n')
                for x in myresult:
                    lbQ1= tkinter.Label(ventana,text="Nombre: "+x[1],fg=rgbtohex(r=105, g=105, b=105),bg=rgbtohex(r=60, g=179, b=113),font=("Nunito", 20))
                    lbQ1 .place(relx=0.5,rely=0.25,anchor='n')

                    lbQ2= tkinter.Label(ventana,text="Precio: $"+str(x[2]),fg=rgbtohex(r=105, g=105, b=105),bg=rgbtohex(r=60, g=179, b=113),font=("Nunito", 20))
                    lbQ2.place(relx=0.5,rely=0.35,anchor='n')

                    lbQ3= tkinter.Label(ventana,text="Unidades disponibles: "+str(x[4]),fg=rgbtohex(r=105, g=105, b=105),bg=rgbtohex(r=60, g=179, b=113),font=("Nunito", 20))
                    lbQ3 .place(relx=0.5,rely=0.45,anchor='n')

                    lbQ4= tkinter.Label(ventana,text="Descripción: \n"+x[3],fg=rgbtohex(r=105, g=105, b=105),bg=rgbtohex(r=60, g=179, b=113),font=("Nunito", 20))
                    lbQ4 .place(relx=0.5,rely=0.55,anchor='n')

                    raw_data = urllib.request.urlopen(x[5]).read()
                    im = Image.open(io.BytesIO(raw_data))
                    img4 = ImageTk.PhotoImage(im)
                    imgQ= tkinter.Label(ventana, image = img4)
                    imgQ.place(relx=0.5,rely=0.65,anchor='n')

            else:
                path3='img/error.png'
                img3 = ImageTk.PhotoImage(Image.open(path3))
                imgRes= tkinter.Label(ventana, image = img3)
                imgRes.place(relx=0.5,rely=0.05,anchor='n')
                lbError = tkinter.Label(ventana,text="¡Busqueda Fallida!",fg="red",bg=rgbtohex(r=60, g=179, b=113),font=("Nunito", 30))
                lbError .place(relx=0.5,rely=0.45,anchor='n')
                lbError2 = tkinter.Label(ventana,text="Lo sentimos, no es posible leer el codigo de su producto.\nPor favor acuda a servicio al cliente para mas información.",fg=rgbtohex(r=105, g=105, b=105),bg=rgbtohex(r=60, g=179, b=113),font=("Nunito", 30))
                lbError2 .place(relx=0.5,rely=0.55,anchor='n')

    
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")

            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                lbMan = tkinter.Label(ventana,text="¡Dispositivo en mantenimiento!",fg="yellow",bg=rgbtohex(r=60, g=179, b=113),font=("Nunito", 30))
                lbMan.place(relx=0.5,rely=0.45,anchor='n')
                lbMan2 = tkinter.Label(ventana,text="Lo sentimos, intente utilizar el dispositivo mas tarde.\nPor favor acuda a servicio al cliente para mas información.",fg=rgbtohex(r=105, g=105, b=105),bg=rgbtohex(r=60, g=179, b=113),font=("Nunito", 30))
                lbMan2 .place(relx=0.5,rely=0.55,anchor='n')
                path3='img/alerta.png'
                img3 = ImageTk.PhotoImage(Image.open(path3))
                imgRes= tkinter.Label(ventana, image = img3)
                imgRes.place(relx=0.5,rely=0.15,anchor='n')
        else:
            conn.close()
    else: 
        codigo += event.char

ventana.bind("<Key>", fun)
ventana.configure(bg=rgbtohex(r=60, g=179, b=113)) 
ventana.mainloop()