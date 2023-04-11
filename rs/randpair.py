#!/usr/bin/python3
import random

keywords = '''
Adversarial Attack
Adversarial Defense
AutoML
Crossentropy Loss
Defensive Distillation
Distillation
Face Identification
Face Recognition
Image Classification
Network Architecture Search
ResNet
Support Vector Machine
Tylor Expansion
'''.split('\n')
keywords = [x for x in keywords if x]

print(random.sample(keywords, 2))
