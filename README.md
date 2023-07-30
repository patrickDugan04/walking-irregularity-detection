## Introduction
This project uses Machine Learning to detect if a person has an irregular gait.
Our goal is to use these classifiers as an early warning sign for Parkinson's disease.

## Data Collection
We gathered data by filming ourselves walking with irregular and regular cadences. We then processed
the data by sampling frames of the videos and passing them through ![OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose). We trained both a CNN and a SVM classifier on the dataset and compare accuracy of both.

## How to Run the Code
Run the code from run.py
