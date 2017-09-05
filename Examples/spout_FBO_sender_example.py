# Add relative directory ../Library to import path, so we can import the SpoutSDK.pyd library. Feel free to remove these if you put the SpoutSDK.pyd file in the same directory as the python scripts.
import sys
sys.path.append('../Library')

import SpoutSDK
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )


def Cube():
    glBegin(GL_LINES)    
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def main():

    # window details
    width = 800 
    height = 600 
    display = (width,height)
    
    # window setup
    pygame.init() 
    pygame.display.set_caption('Spout Python Sender')
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.gl_set_attribute(pygame.GL_ALPHA_SIZE, 8)

    # OpenGL init
    # setup OpenGL perspective
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    # setup default colours, blending modes, rotation and translation parameters
    glMatrixMode(GL_MODELVIEW)
    # reset the drawing perspective
    glLoadIdentity()
    # can disable depth buffer because we aren't dealing with multiple geometry in our scene
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_ALPHA_TEST)
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glClearColor(0.0,0.0,0.0,0.0)
    glColor4f(1.0, 1.0, 1.0, 1.0);   
    glTranslatef(0,0, -5)
    glRotatef(25, 2, 1, 0)

    # init spout sender
    spoutSender = SpoutSDK.SpoutSender()
    spoutSenderWidth = width
    spoutSenderHeight = height
    # Its signature in C++ looks like this: bool CreateSender(const char *Sendername, unsigned int width, unsigned int height, DWORD dwFormat = 0);
    spoutSender.CreateSender('Spout Python Sender', spoutSenderWidth, spoutSenderHeight, 0)

    # init spout sender texture ID
    senderTextureID = glGenTextures(1)

    # initialise texture
    glBindTexture(GL_TEXTURE_2D, senderTextureID)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    # fill texture with blank data
    glCopyTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,0,0,spoutSenderWidth,spoutSenderHeight,0);
    glBindTexture(GL_TEXTURE_2D, 0)

    # create fbo and connect it to our senderTexture
    fbo = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, senderTextureID, 0)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # setup frame
        glActiveTexture(GL_TEXTURE0)
        glClearColor(0.0,0.0,0.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # bind our fbo and render some content to it - by using an FBO we will get alpha transparency sent with Spout
        glBindFramebuffer(GL_FRAMEBUFFER, fbo)
        #Start fbo frame afresh by setting clear color and performing a clear operation
        glClearColor(0.0,0.0,0.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Perform a rotation and since we aren't resetting our perspective with glLoadIdentity, then each frame will perform a successive rotation on top of what we already see
        glRotatef(1, 3, 1, 1)
        
        # draw cube
        Cube()

        # back to the default framebuffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # read the FBO and then use Blit to copy into the backbuffer.
        # A faster approach may be to render the fbo to a textured quad, but this will do for now.
        glBindFramebuffer (GL_READ_FRAMEBUFFER, fbo);
        glBlitFramebuffer (0,0, spoutSenderWidth,spoutSenderHeight, 0,0, spoutSenderWidth,spoutSenderHeight, GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT, GL_NEAREST)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        
        # send texture to Spout
        # Its signature in C++ looks like this: bool SendTexture(GLuint TextureID, GLuint TextureTarget, unsigned int width, unsigned int height, bool bInvert=true, GLuint HostFBO = 0);
        spoutSender.SendTexture(senderTextureID, GL_TEXTURE_2D, spoutSenderWidth, spoutSenderHeight, True, 0)
       
        # update display 
        pygame.display.flip()

        pygame.time.wait(10)

main()





