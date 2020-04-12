import numpy as np
import random
from skimage import io
from handlers import files_handler as fh


class ImageHandler:
	def __init__(self, img_h, img_w, max_h, max_w, noise_matrix):
		self.image = np.zeros(shape=(img_w, img_h))
		self.img_h = img_h
		self.img_w = img_w
		self.max_h = max_h
		self.max_w = max_w
		self.noise_matrix = noise_matrix
		self.std = 1
		self.mean = 0
		self.__init_std_and_mean()

	def place_cell(self, col, row, extracted_cell):
		height = extracted_cell.shape[0]
		width = extracted_cell.shape[1]
		self.image[row:row + height, col:col + width] += extracted_cell

	def save_image(self, img_name):
		io.imsave(fh.get_output_img_path(img_name), self.image)

	def add_background_noise(self):
		self.image += np.random.normal(loc=self.mean, scale=self.std, size=(self.img_h, self.img_w))

	def normalize(self):
		max_value = np.max(self.image)
		self.image /= max_value

	def get_random_col_pos(self):
		return random.randint(0, self.img_w - self.max_w)

	def get_random_row_pos(self):
		return random.randint(0, self.img_h - self.max_h)

	def __init_std_and_mean(self):
		self.mean = np.average(self.noise_matrix)
		self.std = np.std(self.noise_matrix)
