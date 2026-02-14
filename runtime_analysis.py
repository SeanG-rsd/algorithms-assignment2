import pytest
import os
import sys
import time
import numpy as np
from pathlib import Path
import subprocess
import glob
import random
# print(sys.getrecursionlimit())
sys.setrecursionlimit(6000)

cost_dict = ['A', 'T', 'G', 'C']

def generate_random_input_file(length, file_name, seed):
	random.seed(seed)
	with open("runtime_test_input.txt", "w") as file:
		for i in range (0, length):
			file.write(cost_dict[int(random.random()*4)])
		file.write(",")
		for i in range (0, length):
			file.write(cost_dict[int(random.random()*4)])

def run_script_with_output(script_path, input_file):
    script_path = Path(script_path).resolve()
    script_dir = script_path.parent
    subprocess.run([sys.executable, str(script_path)], check=True, cwd=script_dir)

def runtime(algorithm, size):
	avg_runtime = 0
	for j in range (0,10):
		generate_random_input_file(size, "runtime_test_input.txt", random.random()*1000000)
		start_time = time.perf_counter()
		run_script_with_output(algorithm, "runtime_test_input.txt")
		runtime = time.perf_counter() - start_time
		print(f"{algorithm} runtime for test {j+1} size {size}: {runtime} seconds")
		avg_runtime += runtime/10
	print(f"{algorithm} runtime for size {size}: {avg_runtime} seconds")

runtime("sequence_alignment.py", 500)
runtime("sequence_alignment.py", 1000)
runtime("sequence_alignment.py", 2000)
runtime("sequence_alignment.py", 4000)
runtime("sequence_alignment.py", 5000)