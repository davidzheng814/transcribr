import numpy as np

INPUT_FILE = 'training_data_inputs.npz'
OUTPUT_FILE = 'training_data_outputs.npz'

FILENAME_BASE = 'sample'
NUM_SAMPLES = 200

if __name__ == '__main__':
	inputs = np.load(INPUT_FILE)
	outputs = np.load(OUTPUT_FILE)
	for i in range(NUM_SAMPLES):
		basename = FILENAME_BASE+"_"+str(i)
		input_num_windows = inputs[basename].shape
		output_num_windows = outputs[basename].shape
		print i, input_num_windows, output_num_windows