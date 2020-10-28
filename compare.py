from PIL import Image, ImageGrab, ImageChops
import win32gui
import ctypes
import time
import os.path
from os import path
import keyboard
imgRefPath = '../ref'
vote_countdown = 5
voted_bbox = meeting_bbox = startGame_bbox = endGame_bbox = []

application_name = 'Among Us'
#main_application = win32gui.FindWindow(None, application_name)
user32 = ctypes.windll.user32
user32.SetProcessDPIAware(2)

# while True:
#     if win32gui.GetForegroundWindow() == main_application:
#         bbox = win32gui.GetWindowRect(main_application)
#         #bbox = win32gui.GetClientRect(main_application)
#         resolution = [bbox[2]-bbox[0], bbox[3]-bbox[1]]
#         break
#     print("can't see app")
#     time.sleep(1)

# if bbox[0]+bbox[1] != 0:
#     print("application not full screened")
    
# #win32gui.SetForegroundWindow(main_application) #used when you want to take an image for comparison
# print(str(bbox[2]-bbox[0]) +" "+ str(bbox[3]-bbox[1]))
# print(str(bbox[2]) +" "+ str(bbox[3]))
# #bbox = [bbox[0], int(bbox[3] * 0.40), int(bbox[2] * 0.30), int(bbox[3] * 0.60)] #screenshot on meeting call or report
# bbox = [int(bbox[2] * 0.15), int(bbox[3] * 0.825), int(bbox[2] * 0.20), int(bbox[3] * 0.90)] #screenshot to compare when votes go out
# #print(bbox)
# #img = ImageGrab.grab(bbox)
# img = Image.open('skip.png')
# img = img.crop(bbox)

# #img.save(str(resolution[0]) + '_' + str(resolution[1]) + '_meeting.png')
# img.save(str(resolution[0]) + '_' + str(resolution[1]) + '_voted.png')
# img.show()

def compareImg(bbox, fname):

    if win32gui.GetForegroundWindow() == main_application:
        refImg = Image.open(imgRefPath + str(resolution[0]) + '_' + str(resolution[1]) + '_'+ fname + '.png')
        diff = ImageChops.difference(refImg, ImageGrab.grab(bbox))

        if diff.getbbox():
            print("images are different")
        else:
            print("images are the same")
            return True

    return False

def create_reference_img(bbox, fname, resolution):

        while True:

            keyboard.wait('p')
            if win32gui.GetForegroundWindow() == main_application:
                img = ImageGrab.grab(bbox)
                img.save(imgRefPath + str(resolution[0]) + '_' + str(resolution[1]) + '_'+ fname + '.png')
                print('Reference image has been created')
                return
            else:
                print('Ensure that ' + application_name + ' is in the foreground')

if __name__ == "__main__":

    while win32gui.FindWindow(None, application_name) is 0:
        print("Waiting for game to start")
        time.sleep(5)
    
    main_application = win32gui.FindWindow(None, application_name)
    bbox = win32gui.GetWindowRect(main_application)

    startGame_bbox = [bbox[0], int(bbox[3] * 0.40), int(bbox[2] * 0.30), int(bbox[3] * 0.60)] #fix values
    meeting_bbox = [bbox[0], int(bbox[3] * 0.40), int(bbox[2] * 0.30), int(bbox[3] * 0.60)]
    voted_bbox = [int(bbox[2] * 0.15), int(bbox[3] * 0.825), int(bbox[2] * 0.20), int(bbox[3] * 0.90)]
    endGame_bbox = [int(bbox[2] * 0.80), int(bbox[3] * 0.15), int(bbox[2] * 0.90), int(bbox[3] * 0.20)] #fix values

    resolution = [bbox[2]-bbox[0], bbox[3]-bbox[1]] #may be important to track if window is dragged around
    res_string = str(resolution[0]) + '_' + str(resolution[1])

    #check if image exists for the current resolution

    if not path.exists(imgRefPath + res_string + '_startGame.png'):
        print("Press p when 'shh' appears on the screen")
        create_reference_img(startGame_bbox, '_startGame.png', resolution)

    if not path.exists(imgRefPath + res_string + '_meeting.png'):
        print('Press p when a body has been reported or a meeting has been called')
        create_reference_img(meeting_bbox, '_meeting.png', resolution)

    if not path.exists(imgRefPath + res_string + '_voted.png'):
        print('Press p when all votes have been cast or a meeting timer goes to 0')
        create_reference_img(voted_bbox, '_voted.png', resolution)
        create_reference_img(endGame_bbox, '_endGame.png', resolution)

    while True:
        while compareImg(meeting_bbox,'meeting'):
            pass
        time.sleep(5)

        while compareImg(voted_bbox,'voted'):
            pass
        time.sleep(vote_countdown+5)

        if not compareImg(endGame_bbox, 'endGame'):
            pass
        else:
            pass #mute