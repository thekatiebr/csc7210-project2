import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
import os
os.sys.path.insert(0, ".")
import DiabetesData

#get diabetes dataloaders
train_generator, val_generator, test_generator = DiabetesData.getDataGenerators(data_file="data/trainLabels.csv")

#generate model
base_model = keras.applications.VGG16(weights='imagenet', include_top=False)
x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
x = Dense(1024, activation='relu')(x)
# and a logistic layer -- let's say we have 200 classes
predictions = Dense(2, activation='softmax')(x)

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional VGG16 layers
for layer in base_model.layers:
    layer.trainable = False



#fit model

