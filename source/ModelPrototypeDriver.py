# PyTorch Imports
#from IPython.core.interactiveshell import InteractiveShell
from torchvision import transforms, datasets, models
import torch
import torch.nn.functional as F
from torch import optim, cuda
from torch.utils.data import Dataset, DataLoader, sampler
import torch.nn as nn
from torchsummary import summary # Useful for examining network
from collections import Counter
# Data Science | Image Tools | MatplotLib
import numpy as np
import pandas as pd
import matplotlib
import os, sys, shutil, time, argparse, collections
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, roc_auc_score
from tqdm import tqdm
from datetime import date
# Image manipulations
from PIL import Image

# Visualizations
import matplotlib.pyplot as plt

from DiabetesModelPT import DiabetesModel
from DiabetesData import DiabeticData




t = 1
task = ([0], [4])
# task = ([0,1], (2,3,4))
batch_size=16
epochs = 15
root_dir = "data/diabetes"
# task = ([0,1,2], (3,4))

# train = pd.read_csv("data/diabetes_ad_train.csv")
# val = pd.read_csv("data/diabetes_ad_valid.csv")
# test = pd.read_csv("data/diabetes_ad_test.csv")

data = pd.read_csv("data/trainLabels.csv")

zeroes = data[data['level'] == 0]
ones = data[data['level'] == 4]
data = pd.concat([zeroes,ones])
data = data.sample(frac=1)

train, test = train_test_split(data, test_size=0.1)
train, val = train_test_split(train, test_size=0.1)

train = train.reset_index()
test = test.reset_index()
val = val.reset_index()

data = {'train': DiabeticData(df = train, transform_key="train", root_dir=root_dir, task = task),
        'valid': DiabeticData(df = val, transform_key="valid", root_dir=root_dir, task = task),
        'test': DiabeticData(df = test, transform_key="test", root_dir=root_dir, task = task),
        }

dataloaders = {
        'train': DataLoader(data['train'], batch_size=batch_size, shuffle=True),
        'valid': DataLoader(data['valid'], batch_size=batch_size, shuffle=True),
        'test': DataLoader(data['test'], batch_size=1, shuffle=True)
} 


model = DiabetesModel(measure_uncertainty=False)

model.fit(dataloaders['train'], dataloaders['valid'], n_epochs=epochs)

preds = []
trues = []

pred, true = model.predict(dataloaders['test'])
preds.append(pred)
preds = np.asarray(preds)
true = np.asarray(true)
print(preds.shape)
print(true.shape)

preds = preds[0]
labels = [int(p >= 0.5) for p in preds]


print("Accuracy: ", accuracy_score(true, labels))
print("Recall: ", recall_score(true, labels))
print("Precision: ", precision_score(true, labels))
print("F1: ", f1_score(true, labels))
print("AUC: ", roc_auc_score(true, pred))