# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 14:30:31 2020

@author: MMM
"""

import tensorflow as tf
from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, UpSampling2D, Input, MaxPooling2D, Concatenate
from tensorflow.keras.models import Model
from tensorflow import keras

def conv_block(x,num_filters):
    
    x=Conv2D(num_filters,(3,3),padding='same')(x)
    x=BatchNormalization()(x)
    x=Activation('relu')(x)
    
    x=Conv2D(num_filters,(3,3),padding='same')(x)
    x=BatchNormalization()(x)
    x=Activation('relu')(x)
    return x
    

def build_model():
    size=256
    num_filters=[16,32,48,64]
    
    inputs=Input(shape=(size,size,3))
    skip_x=[]
    x=inputs
    
    #Encoder
    for f in num_filters:
        x=conv_block(x,f)
        skip_x.append(x)
        x=MaxPooling2D(2,2)(x)
        

    #bottleneck
    x=conv_block(x,num_filters[-1])
    
    num_filters.reverse()
    skip_x.reverse()
    
    #Decoder
    for i,f in enumerate(num_filters):
        x=UpSampling2D((2,2))(x)
        xs=skip_x[i]
        x=Concatenate()([x,xs])
        x=conv_block(x,f)
    #output
    x=Conv2D(1,(1,1),padding='same')(x)
    x=Activation('sigmoid')(x)
    return Model(inputs,x)

if __name__=="__main__":
    
    model=build_model()
    model.summary()
    
    
    