# Add relative directory ../Library to import path, so we can import the SpoutSDK.pyd library. Feel free to remove these if you put the SpoutSDK.pyd file in the same directory as the python scripts.
import sys
sys.path.append('../Library')

import argparse
import cv2
import SpoutSDK
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

"""parsing and configuration"""
def parse_args():
    desc = "Spout for Python webcam sender example"
    parser = argparse.ArgumentParser(description=desc)
   
    parser.add_argument('--camSize', nargs = 2, type=int, default=[640, 480], help='File path of content image (notation in the paper : x)')

    parser.add_argument('--camID', type=int, default=1, help='Webcam Device ID)')

    return parser.parse_args()


"""main"""
def main():

    # parse arguments
    args = parse_args()

    # window details
    width = args.camSize[0] 
    height = args.camSize[1] 
    display = (width,height)
    
    # window setup
    pygame.init() 
    pygame.display.set_caption('Spout for Python Webcam Sender Example')
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.gl_set_attribute(pygame.GL_ALPHA_SIZE, 8)

    # init capture & set size
    cap = cv2.VideoCapture(args.camID)
    cap.set(3, width)
    cap.set(4, height)

    # OpenGL init
    glMatrixMode(GL_PROJECTION)
    glOrtho(0,width,height,0,1,-1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glClearColor(0.0,0.0,0.0,0.0)
    glEnable(GL_TEXTURE_2D)
   
    # init spout sender
    spoutSender = SpoutSDK.SpoutSender()
    spoutSenderWidth = width
    spoutSenderHeight = height
    spoutSender.CreateSender('Spout for Python Webcam Sender Example', width, height, 0)
    
    # create texture id for use with Spout
    senderTextureID = glGenTextures(1)

    # initalise our sender texture
    glBindTexture(GL_TEXTURE_2D, senderTextureID)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glBindTexture(GL_TEXTURE_2D, 0)

    # loop 
    while(True):
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               quit()

        ret, frame = cap.read()
        frame = cv2.flip(frame, 1 )
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Copy the frame from the webcam into the sender texture
        glBindTexture(GL_TEXTURE_2D, senderTextureID)
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, frame )
      
        # Send texture to Spout
        spoutSender.SendTexture(senderTextureID, GL_TEXTURE_2D, spoutSenderWidth, spoutSenderHeight, False, 0)
       
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT )
        # reset the drawing perspective
        glLoadIdentity()
       
        # Draw texture to screen
        glBegin(GL_QUADS)

        glTexCoord(0,0)        
        glVertex2f(0,0)

        glTexCoord(1,0)
        glVertex2f(width,0)

        glTexCoord(1,1)
        glVertex2f(width,height)

        glTexCoord(0,1)
        glVertex2f(0,height)

        glEnd()

        # update window
        pygame.display.flip()             
      
        # unbind our sender texture
        glBindTexture(GL_TEXTURE_2D, 0)

if __name__ == '__main__':
    main()
