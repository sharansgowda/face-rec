import cv2
import tkinter as tk
from PIL import Image, ImageTk
from faceRecUtils import FaceRecognition

fr = FaceRecognition()

class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.geometry('1600x900')
        self.window.bind('<Escape>', lambda x: window.quit())
        self.window.title(window_title)
        
        self.label = tk.Label(self.window, text="Open Webcam", font=('Source Code Pro', 18), bd=4)
        self.label.pack(fill=tk.X, side=tk.TOP)

        self.button = tk.Button(self.window, text="Enable Camera", command=fr.run_recognition, cursor="hand")
        self.button.pack()

        self.window.mainloop()

if __name__ == "__main__":
    WebcamApp(tk.Tk(), "Webcam")
