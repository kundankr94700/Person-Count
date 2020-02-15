import cv2
from tkinter import filedialog
from tkinter import *
import threading
import pyttsx3 as t2s
from tkinter.font import  Font
from PIL import ImageTk, Image
import os
face_cascade = cv2.CascadeClassifier('face_cas.xml')

def thread(n):
    try:
        eng = t2s.init()
        eng.setProperty('rate', 120)
        eng.setProperty('volume', .9)
        eng.say("Number Of Persons Are %s" % (n))
        eng.runAndWait()
    except:
        pass
n1=0
def image_operation(img):

    global n1
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    n=0
    for (x, y, w, h) in face:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
        n = face.shape[0]

        cv2.putText(img, 'Number Of Person : ' + str(n), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 100, 0), 1)

    if n==0:
        n1=0
    try:

        if n1!=n:
            n1 = n

            t = threading.Thread(name='child', target=thread, args=(n,))
            if not t.is_alive():
                t.start()
    except:
        pass
    return img

def from_image():
    try:
        img_path = filedialog.askopenfilename(initialdir="/", title="select file",filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        img = cv2.imread(img_path)
        height, width, depth = img.shape
        print(width,height)
        if width>height:
            img = cv2.resize(img, (1280,960))
        else:
            img = cv2.resize(img, (960, 1280))

        img = image_operation(img)
        cv2.imshow('img', img)
        cv2.waitKey(0)
    except:
        pass

def from_camera():
    def thread(n):
        try:
            eng = t2s.init()
            eng.setProperty('rate', 120)
            eng.setProperty('volume', .9)
            eng.say("Number Of Persons Are %s" % (n))
            eng.runAndWait()
        except:
            pass

    n1 = 0
    root1.destroy()
    root_PC = Tk()
    root_PC.geometry("500x400+100+30")
    app = Frame(root_PC, bg="white")
    app.place(x=1, y=1)
    lmain = Label(app)
    lmain.grid()
    camera = cv2.VideoCapture(0)

    def video_stream():
        ret, image = camera.read()
        image = cv2.flip(image, 1)
        global n1
        gray = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
        face = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
        n = 0
        for (x, y, w, h) in face:
            cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 255, 0), 2)
            n = face.shape[0]

            cv2.putText(gray, 'Number Of Person : ' + str(n), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 100, 0), 1)

        if n == 0:
            n1 = 0
        try:

            if n1 != n:
                n1 = n

                t = threading.Thread(name='child', target=thread, args=(n,))
                if not t.is_alive():
                    t.start()
        except:
            pass

        img = Image.fromarray(gray)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(1, video_stream)

    video_stream()

    root_PC.attributes("-topmost", True)
    root_PC.mainloop()


root1 = Tk()
root1.title('Person_Count_Application')
root1.geometry('600x400+410+100')
img1 = ImageTk.PhotoImage(Image.open("face_rec2.jpg"))
panel = Label(root1, image=img1).place(x=10,y=20)
f4 = Font(family="Time New Roman", size=13, weight="bold")
l3 = Label(root1, text="Machine Learning Paper II", fg='brown', font=f4).place(x=200, y=1)
b1 = Button(root1, text='Camera', command=from_camera, width=15, height=1, bg='white', font=f4).place(x=20, y=280)
b2 = Button(root1, text='Image', command=from_image, width=15, height=1, bg='green', font=f4).place(x=20, y=320)
b2 = Button(root1, text='Close', command=root1.destroy, width=10, height=1, bg='white', font=f4).place(x=480, y=360)
root1.resizable('false','false')
root1.mainloop()