import sys

sys.path.append('Library/3{}'.format(sys.version_info[1]))

import numpy as np
import argparse
import time
import SpoutSDK
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.framebufferobjects import *
from OpenGL.GLU import *

class Spout() :
    """
    Spout class for python wrapper
    """

    def __init__( self, silent = False, width = 1280, height = 720 ):
        """
        Initialize spout object
        Args:
            silent: boolean, hide windows, default = False
            width: window width, default = 1280
            height: window height, default = 720
        """

        self.width = width
        self.height = height
        self.silent = silent
        self.display = ( self.width, self.height )

        self.spoutReceiver = None
        self.receiverWidth = None
        self.receiverHeight = None
        self.textureReceiveID = None

        self.spoutSender = None
        self.textureSendID = None

        #window setup
        pygame.init() 
        pygame.display.set_caption( 'Spout For Python' )
        pygame.display.set_mode( self.display, DOUBLEBUF|OPENGL )

        # OpenGL init
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, 1, -1 )
        glMatrixMode( GL_MODELVIEW )
        glDisable( GL_DEPTH_TEST )
        glClearColor( 0.0, 0.0, 0.0, 0.0)
        glEnable( GL_TEXTURE_2D )

    def createReceiver( self, name = 'input', type = GL_RGB, dataType = GL_UNSIGNED_BYTE):
        """
        Initialize spout receiver
        Args:
            name: receiver name, default = 'input'
            type: texture type, default = GL_RGB, available = GL_RGBA, GL_RGB, GL_ALPHA, GL_LUMINANCE, GL_LUMINANCE_ALPHA
            dataType: texture data type, default = GL_UNSIGNED_BYTE, available = GL_UNSIGNED_BYTE, GL_FLOAT
        """

        self.receiverName = name
        self.receiverType = type
        self.receiverDataType = dataType
        
        # init spout receiver
        self.spoutReceiver = SpoutSDK.SpoutReceiver()

        self.receiverWidth = self.spoutReceiver.GetWidth( self.receiverName )
        self.receiverHeight = self.spoutReceiver.GetHeight( self.receiverName )

        # create spout receiver
	    # Its signature in c++ looks like this: bool pyCreateReceiver(const char* theName, unsigned int theWidth, unsigned int theHeight, bool bUseActive);
        self.spoutReceiver.pyCreateReceiver( self.receiverName, self.receiverWidth, self.receiverHeight, False )
        # create textures for spout receiver and spout sender 
        self.textureReceiveID = glGenTextures(1)
        
        # initalise receiver texture
        glBindTexture( GL_TEXTURE_2D, self.textureReceiveID )
        glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE )
        glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )

        # copy data into texture
        glTexImage2D( GL_TEXTURE_2D, 0, self.receiverType, self.receiverWidth, self.receiverHeight, 0, self.receiverType, self.receiverDataType, None ) 
        glBindTexture(GL_TEXTURE_2D, 0)

        return True

    def createSender(self, name = 'output', type = GL_RGB, dataType = GL_UNSIGNED_BYTE):
        """
        Initialize spout sender
        Args:
            name: receiver name, default = 'output'
            type: texture type, default = GL_RGB, available = GL_RGBA, GL_RGB, GL_ALPHA, GL_LUMINANCE, GL_LUMINANCE_ALPHA
            dataType: texture data type, default = GL_UNSIGNED_BYTE, available = GL_UNSIGNED_BYTE, GL_FLOAT
        """

        self.senderName = name
        self.senderWidth = 0
        self.senderHeight = 0
        self.senderType = type
        self.senderDataType = dataType
        # init spout sender

        self.spoutSender = SpoutSDK.SpoutSender()
	    # Its signature in c++ looks like this: bool CreateSender(const char *Sendername, unsigned int width, unsigned int height, DWORD dwFormat = 0);
        self.spoutSender.CreateSender(self.senderName, self.width, self.height, 0)
        # create textures for spout receiver and spout sender 
        self.textureSendID = glGenTextures(1)

    def receive( self ):
        """
        Receive texture
        """

        if self.spoutReceiver != None and self.textureReceiveID != None:
            # receive texture
            # Its signature in c++ looks like this: bool pyReceiveTexture(const char* theName, unsigned int theWidth, unsigned int theHeight, GLuint TextureID, GLuint TextureTarget, bool bInvert, GLuint HostFBO);
            self.spoutReceiver.pyReceiveTexture( self.receiverName, self.receiverWidth, self.receiverHeight, self.textureReceiveID.item(), GL_TEXTURE_2D, False, 0 )

            glBindTexture( GL_TEXTURE_2D, self.textureReceiveID )
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE )
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE )
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
            # copy pixel byte array from received texture   
            data = glGetTexImage( GL_TEXTURE_2D, 0, self.receiverType, self.receiverDataType, outputType=None )  #Using GL_RGB can use GL_RGBA 
            glBindTexture( GL_TEXTURE_2D, 0 )
            # swap width and height data around due to oddness with glGetTextImage. http://permalink.gmane.org/gmane.comp.python.opengl.user/2423
            data.shape = (data.shape[1], data.shape[0], data.shape[2])

            return data

        else:
            return self.empty()

    def send(self, data):
        """
        Send texture
        """

        if data.size == 0:
            data = self.empty()
        else:
            self.senderWidth = data.shape[1]
            self.senderHeight = data.shape[0]

        if self.spoutSender != None and self.textureSendID != None:

            # setup the texture so we can load the output into it
            glBindTexture( GL_TEXTURE_2D, self.textureSendID );
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE )
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE )
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
            # copy output into texture
            glTexImage2D( GL_TEXTURE_2D, 0, self.senderType, self.senderWidth, self.senderHeight, 0, self.senderType, self.senderDataType, data )
                
            # setup window to draw to screen
            glActiveTexture( GL_TEXTURE0 )
            # clean start
            glClear( GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT )
            # reset drawing perspective
            glLoadIdentity()
            # draw texture on screen
            glBegin( GL_QUADS )

            glTexCoord( 0,0 )        
            glVertex2f( 0,0 )

            glTexCoord( 1,0 )
            glVertex2f(self.width,0)

            glTexCoord(1,1)
            glVertex2f(self.width,self.height)

            glTexCoord(0,1)
            glVertex2f(0,self.height)

            glEnd()
            
            if self.silent:
                pygame.display.iconify()
                    
            # update window
            pygame.display.flip()        

            self.spoutSender.SendTexture(self.textureSendID.item(), GL_TEXTURE_2D, self.senderWidth, self.senderHeight, False, 0)

    def check(self):
        """
        Check on closed window
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.spoutReceiver.ReleaseReceiver()
                pygame.quit()
                quit()

    def empty(self):
        """
        Create empty texture
        """
        data = np.zeros((self.height,self.width,3))
        return data