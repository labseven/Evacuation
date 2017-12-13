import pandas as pd
import pickle
import numpy as np

with open("experimentdataNoBarrier.pk", "rb") as infile:
	infile.seek(0)
	results = pickle.load(infile)

print(results)

results.to_csv("experimentdataNoBarrier.csv")

print("done")
