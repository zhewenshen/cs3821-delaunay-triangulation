#!/bin/bash

num_points=30
x_min=0
x_max=1000
y_min=0
y_max=1000
algorithm="incremental"

python3 main.py $num_points $x_min $x_max $y_min $y_max --algorithm $algorithm --benchmark
