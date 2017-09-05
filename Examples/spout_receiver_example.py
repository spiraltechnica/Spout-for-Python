# Add relative directory ../Library to import path, so we can import the SpoutSDK.pyd library. Feel free to remove these if you put the SpoutSDK.pyd file in the same directory as the python scripts.
import sys
sys.path.append('../Library')

import argparse
import SpoutSDK
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


"""parsing and configuration"""
def parse_args():
    desc = "Spout for Python texture receiving example"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--spout_size', nargs = 2, type=int, default=[640, 480], help='Width and height of the spout receiver')   

    parser.add_argument('--spout_name', type=str, default='Composition - Resolume Arena', help='Spout receiving name - the name of the sender you want to receive')  

    parser.add_argument('--window_size', nargs = 2, type=int, default=[640, 480], help='Width and height of the window')    

    return parser.parse_args()


"""main"""
def main():

    # parse arguments
    args = parse_args()
    
    # window details
    width = args.window_size[0] 
    height = args.window_size[1] 
    display = (width,height)
    
    # window setup
    pygame.init() 
    pygame.display.set_caption('Spout Receiver')
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    # OpenGL init
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,width,height,0,1,-1)
    glMatrixMode(GL_MODELVIEW)
    glDisable(GL_DEPTH_TEST)
    glClearColor(0.0,0.0,0.0,0.0)
    glEnable(GL_TEXTURE_2D)

    # init spout receiver
    receiverName = args.spout_name 
    spoutReceiverWidth = args.spout_size[0]
    spoutReceiverHeight = args.spout_size[1]
    # create spout receiver
    spoutReceiver = SpoutSDK.SpoutReceiver()

	# Its signature in c++ looks like this: bool pyCreateReceiver(const char* theName, unsigned int theWidth, unsigned int theHeight, bool bUseActive);
    spoutReceiver.pyCreateReceiver(receiverName,spoutReceiverWidth,spoutReceiverHeight, False)

    # create texture for spout receiver
    textureReceiveID = glGenTextures(1)    
    
    # initalise receiver texture
    glBindTexture(GL_TEXTURE_2D, textureReceiveID)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    # copy data into texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, spoutReceiverWidth, spoutReceiverHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, None ) 
    glBindTexture(GL_TEXTURE_2D, 0)

    # loop for graph frame by frame
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                spoutReceiver.ReleaseReceiver()
                pygame.quit()
                quit()
        
        # receive texture
        # Its signature in c++ looks like this: bool pyReceiveTexture(const char* theName, unsigned int theWidth, unsigned int theHeight, GLuint TextureID, GLuint TextureTarget, bool bInvert, GLuint HostFBO);
        spoutReceiver.pyReceiveTexture(receiverName, spoutReceiverWidth, spoutReceiverHeight, textureReceiveID, GL_TEXTURE_2D, False, 0)
       
        glBindTexture(GL_TEXTURE_2D, textureReceiveID)

        # copy pixel byte array from received texture - this example doesn't use it, but may be useful for those who do want pixel info      
        # data = glGetTexImage(GL_TEXTURE_2D, 0, GL_RGB, GL_UNSIGNED_BYTE, outputType=None)  #Using GL_RGB can use GL_RGBA 
        
        # swap width and height data around due to oddness with glGetTextImage. http://permalink.gmane.org/gmane.comp.python.opengl.user/2423
        # data.shape = (data.shape[1], data.shape[0], data.shape[2])
        
        # setup window to draw to screen
        glActiveTexture(GL_TEXTURE0)

        # clean start
        glClear(GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT )
        # reset drawing perspective
        glLoadIdentity()
       
        # draw texture on screen
        # glPushMatrix() use these lines if you want to scale your received texture
        # glScale(0.3, 0.3, 0.3)
        glBegin(GL_QUADS)

        glTexCoord(0,0)        
        glVertex2f(0,0)

        glTexCoord(1,0)
        glVertex2f(spoutReceiverWidth,0)

        glTexCoord(1,1)
        glVertex2f(spoutReceiverWidth,spoutReceiverHeight)

        glTexCoord(0,1)
        glVertex2f(0,spoutReceiverHeight)
        
        glEnd()
        # glPopMatrix() make sure to pop your matrix if you're doing a scale        
        # update window
        pygame.display.flip()        

if __name__ == '__main__':
    main()
