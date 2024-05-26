from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore
from PyQt5.uic import loadUi
import sys
import cv2
import numpy as np
import pyautogui
import time


class ScreenRecorder(QMainWindow):
    
    def __init__(self):
        
        self.output_filename = "screen_recording.avi"
        self.fps = 20
        self.recording = False
        self.pause = False

        # Load UI screen
        super(ScreenRecorder,self).__init__()
        loadUi("home.ui",self)

        # add events to btn
        self.startBtn.clicked.connect(self.start_recording)
        self.pauseResumeBtn.clicked.connect(self.pause_and_resume_recording)
        self.stopBtn.clicked.connect(self.stop_recording)

    def start_recording(self):
        self.recording = True
        print('Start Recording...')

        # Get the screen size
        screen_size = pyautogui.size()
        
        # Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(self.output_filename, fourcc, self.fps, (screen_size.width, screen_size.height))
        
        # Record the screen
        start_time = time.time()
        while self.recording:
            if not self.pause:
                # Capture the screen
                img = pyautogui.screenshot()
                
                # Convert the image to a numpy array
                frame = np.array(img)
                
                # Convert the color from RGB (pyautogui) to BGR (OpenCV)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Write the frame
                out.write(frame)

                # get elapsed time
                self.elapsed_time = int(time.time() - start_time)
                
                self.update_timer_label()

            QtCore.QCoreApplication.processEvents()

        # Release everything when done
        out.release()
    
    def pause_and_resume_recording(self):
        if not self.pause: # pause the video 
            self.pause = True
            print('Paused video...')
            self.pauseResumeBtn.setText('Resume')
        else: # Resume video
            self.pause = False
            print('Resuming video...')
            self.pauseResumeBtn.setText('Pause')

    def stop_recording(self):
        self.recording = False
        print('Stopped recording...')

    def update_timer_label(self):
        hours = self.elapsed_time // 3600
        minutes = (self.elapsed_time // 60) % 60
        seconds = self.elapsed_time % 60
        self.timerText.setText(f"{hours:02}:{minutes:02}:{seconds:02}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = ScreenRecorder()
    obj.show()
    sys.exit(app.exec())