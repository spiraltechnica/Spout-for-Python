import sys
import os

sys.path.append('{}/Library/3{}'.format(os.getcwd(), sys.version_info[1]))

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

    def __init__( self, silent = False, width = 1280, height = 720, n_rec = 1, n_send = 1 ):
        """
        Initialize spout object
        Args:
            silent: boolean, hide windows, default = False
            width: window width, default = 1280
            height: window height, default = 720
            n_rec: number of receivers, default = 1
            n_send: number of sender, default = 1
        """

        self.n_rec = n_rec
        self.n_send = n_send

        self.width = width
        self.height = height
        self.silent = silent
        self.display = ( self.width, self.height )

        self.spoutReceiver = [None] * self.n_rec
        self.receiverWidth = [None] * self.n_rec
        self.receiverHeight = [None] * self.n_rec
        self.textureReceiveID = [None] * self.n_rec
        self.receiverName = [None] * self.n_rec
        self.receiverType = [None] * self.n_rec
        self.receiverDataType = [None] * self.n_rec

        self.spoutSender = [None] * self.n_send
        self.textureSendID = [None] * self.n_send
        self.senderWidth = [None] * self.n_send
        self.senderHeight = [None] * self.n_send
        self.senderType = [None] * self.n_send
        self.senderDataType = [None] * self.n_send
        self.senderName = [None] * self.n_send

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

    def createReceiver( self, name = 'input', type = GL_RGB, dataType = GL_UNSIGNED_BYTE , id = 0):
        """
        Initialize spout receiver
        Args:
            name: receiver name, default = 'input'
            type: texture type, default = GL_RGB, available = GL_RGBA, GL_RGB, GL_ALPHA, GL_LUMINANCE, GL_LUMINANCE_ALPHA
            dataType: texture data type, default = GL_UNSIGNED_BYTE, available = GL_UNSIGNED_BYTE, GL_FLOAT
            id: id of receiver if want multiple, default = 0
        """

        self.receiverName[id] = name
        self.receiverType[id] = type
        self.receiverDataType[id] = dataType
        
        # init spout receiver
        self.spoutReceiver[id] = SpoutSDK.SpoutReceiver()

        self.receiverWidth[id] = self.spoutReceiver[id].GetWidth( self.receiverName[id] )
        self.receiverHeight[id] = self.spoutReceiver[id].GetHeight( self.receiverName[id] )

        # create spout receiver
	    # Its signature in c++ looks like this: bool pyCreateReceiver(const char* theName, unsigned int theWidth, unsigned int theHeight, bool bUseActive);
        self.spoutReceiver[id].pyCreateReceiver( self.receiverName[id], self.receiverWidth[id], self.receiverHeight[id], False )
        # create textures for spout receiver and spout sender 
        self.textureReceiveID[id] = glGenTextures(1)
        
        # initalise receiver texture
        glBindTexture( GL_TEXTURE_2D, self.textureReceiveID[id] )
        glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE )
        glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )

        # copy data into texture
        glTexImage2D( GL_TEXTURE_2D, 0, self.receiverType[id], self.receiverWidth[id], self.receiverHeight[id], 0, self.receiverType[id], self.receiverDataType[id], None ) 
        glBindTexture(GL_TEXTURE_2D, 0)

        return True

    def createSender(self, name = 'output', type = GL_RGB, dataType = GL_UNSIGNED_BYTE, id = 0):
        """
        Initialize spout sender
        Args:
            name: receiver name, default = 'output'
            type: texture type, default = GL_RGB, available = GL_RGBA, GL_RGB, GL_ALPHA, GL_LUMINANCE, GL_LUMINANCE_ALPHA
            dataType: texture data type, default = GL_UNSIGNED_BYTE, available = GL_UNSIGNED_BYTE, GL_FLOAT
            id: id of sender if want multiple, default = 0
        """

        self.senderName[id] = name
        self.senderWidth[id] = 0
        self.senderHeight[id] = 0
        self.senderType[id] = type
        self.senderDataType[id] = dataType
        # init spout sender

        self.spoutSender[id] = SpoutSDK.SpoutSender()
	    # Its signature in c++ looks like this: bool CreateSender(const char *Sendername, unsigned int width, unsigned int height, DWORD dwFormat = 0);
        self.spoutSender[id].CreateSender(self.senderName[id], self.width, self.height, 0)
        # create textures for spout receiver and spout sender 
        self.textureSendID[id] = glGenTextures(1)

    def receive( self , id = 0):
        """
        Receive texture
        Args:
            id: id of receiver if want multiple, default = 0
        """

        # if textures sizes do not match recreate receiver
        if self.receiverWidth[id] != self.spoutReceiver[id].GetWidth(self.receiverName[id]) or self.receiverHeight[id] != self.spoutReceiver[id].GetHeight(self.receiverName[id]):

            self.receiverWidth[id] = self.spoutReceiver[id].GetWidth( self.receiverName[id] )
            self.receiverHeight[id] = self.spoutReceiver[id].GetHeight( self.receiverName[id] )
            
            self.spoutReceiver[id].pyCreateReceiver( self.receiverName[id], self.receiverWidth[id], self.receiverHeight[id], False )
            self.textureReceiveID[id] = glGenTextures(1)
            
            glBindTexture( GL_TEXTURE_2D, self.textureReceiveID[id] )
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE )
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE )
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )

            glTexImage2D( GL_TEXTURE_2D, 0, self.receiverType[id], self.receiverWidth[id], self.receiverHeight[id], 0, self.receiverType[id], self.receiverDataType[id], None ) 
            glBindTexture(GL_TEXTURE_2D, 0)

        if self.spoutReceiver[id] != None and self.textureReceiveID[id] != None:
            # receive texture
            # Its signature in c++ looks like this: bool pyReceiveTexture(const char* theName, unsigned int theWidth, unsigned int theHeight, GLuint TextureID, GLuint TextureTarget, bool bInvert, GLuint HostFBO);
            self.spoutReceiver[id].pyReceiveTexture( self.receiverName[id], self.receiverWidth[id], self.receiverHeight[id], self.textureReceiveID[id].item(), GL_TEXTURE_2D, False, 0 )

            glBindTexture( GL_TEXTURE_2D, self.textureReceiveID[id] )
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE )
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE )
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
            # copy pixel byte array from received texture   
            data = glGetTexImage( GL_TEXTURE_2D, 0, self.receiverType[id], self.receiverDataType[id], outputType=None )  #Using GL_RGB can use GL_RGBA 
            glBindTexture( GL_TEXTURE_2D, 0 )
            # swap width and height data around due to oddness with glGetTextImage. http://permalink.gmane.org/gmane.comp.python.opengl.user/2423
            data.shape = (data.shape[1], data.shape[0], data.shape[2])

            return data

        else:
            return self.empty()

    def send(self, data, id = 0):
        """
        Send texture
        Args:
            id: id of sender if want multiple, default = 0
        """

        if data.size == 0:
            data = self.empty()
        else:
            self.senderWidth[id] = data.shape[1]
            self.senderHeight[id] = data.shape[0]

        if self.spoutSender[id] != None and self.textureSendID[id] != None:

            # setup the texture so we can load the output into it
            glBindTexture( GL_TEXTURE_2D, self.textureSendID[id] );
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE )
            glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE )
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
            # copy output into texture
            glTexImage2D( GL_TEXTURE_2D, 0, self.senderType[id], self.senderWidth[id], self.senderHeight[id], 0, self.senderType[id], self.senderDataType[id], data )
                
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

            self.spoutSender[id].SendTexture(self.textureSendID[id].item(), GL_TEXTURE_2D, self.senderWidth[id], self.senderHeight[id], False, 0)

    def check(self):
        """
        Check on closed window
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for i in range(0,self.n_rec):
                    self.spoutReceiver[i].ReleaseReceiver()
                pygame.quit()
                quit()

    def empty(self):
        """
        Create empty texture
        """
        data = np.zeros((self.height,self.width,3))
        return data