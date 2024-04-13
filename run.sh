#!/bin/bash

num_points=50
x_min=0
x_max=10000
y_min=0
y_max=10000
algorithm="divide"

python3 main.py $num_points $x_min $x_max $y_min $y_max --algorithm $algorithm
