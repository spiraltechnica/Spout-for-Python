# Add relative directory ../Library to import path, so we can import the SpoutSDK.pyd library. Feel free to remove these if you put the SpoutSDK.pyd file in the same directory as the python scripts.
import sys
sys.path.append('../Library')

import tensorflow as tf
import numpy as np
import transform
import argparse
import time
import SpoutSDK
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.framebufferobjects import *
from OpenGL.GLU import *


"""parsing and configuration"""
def parse_args():
    desc = "Tensorflow implementation of 'Perceptual Losses for Real-Time Style Transfer and Super-Resolution', Spout receiver version"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--style_model', type=str, default='style/Checkpoints/saraswati.ckpt', help='location for model file (*.ckpt)')

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
    pygame.display.set_caption('Spout Neural Style Receiver')
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

    # create textures for spout receiver and spout sender 
    textureReceiveID = glGenTextures(1)
    textureStyleID = glGenTextures(1)
    
    # initalise receiver texture
    glBindTexture(GL_TEXTURE_2D, textureReceiveID)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    # copy data into texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, spoutReceiverWidth, spoutReceiverHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, None ) 
    glBindTexture(GL_TEXTURE_2D, 0)

    # initalise sender texture
    glBindTexture(GL_TEXTURE_2D, textureStyleID);
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glBindTexture(GL_TEXTURE_2D, 0)

    # open tf session
    soft_config = tf.ConfigProto(allow_soft_placement=True)
    soft_config.gpu_options.allow_growth = True # to deal with large image
    sess = tf.Session(config=soft_config)
    # build tf graph 
    style = tf.placeholder(tf.float32, shape=[spoutReceiverHeight, spoutReceiverWidth, 3], name='input')
    styleI = tf.expand_dims(style, 0) # add one dim for batch

    # result image from transform-net
    scaler = transform.Transform()
    y_hat = scaler.net(styleI/255.0)
    y_hat = tf.squeeze(y_hat) # remove one dim for batch
    y_hat = tf.clip_by_value(y_hat, 0., 255.)
    
    # initialize parameters
    sess.run(tf.global_variables_initializer())

    # load pre-trained model
    saver = tf.train.Saver()
    saver.restore(sess, args.style_model)

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
        # copy pixel byte array from received texture       
        data = glGetTexImage(GL_TEXTURE_2D, 0, GL_RGB, GL_UNSIGNED_BYTE, outputType=None)  #Using GL_RGB can use GL_RGBA 
        glBindTexture(GL_TEXTURE_2D, 0)
        # swap width and height data around due to oddness with glGetTextImage. http://permalink.gmane.org/gmane.comp.python.opengl.user/2423
        data.shape = (data.shape[1], data.shape[0], data.shape[2])
        
        # start time of the loop for FPS counter
        start_time = time.time()
        #run the graph
        output = sess.run(y_hat, feed_dict={style: data})
        # fiddle back to an image we can display. I *think* this is correct
        output = np.clip(output, 0.0, 255.0)
        output = output.astype(np.uint8)
        
        # setup the texture so we can load the stylised output into it
        glBindTexture(GL_TEXTURE_2D, textureStyleID)
        # copy style output into texture
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGB, spoutReceiverWidth, spoutReceiverHeight, 0, GL_RGB, GL_UNSIGNED_BYTE, output )
        
        # setup window to draw to screen
        glActiveTexture(GL_TEXTURE0)

        # clean start
        glClear(GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT )
        # reset drawing perspective
        glLoadIdentity()
       
        # draw texture on screen
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
                
        # update window
        pygame.display.flip()        

        # FPS = 1 / time to process loop
        print("FPS: ", 1.0 / (time.time() - start_time)) 

if __name__ == '__main__':
    main()
