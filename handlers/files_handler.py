from uuid import *

from utils.consts import *


def get_csv_file_path():
	return img_src_path + '/' + csv_file_name


def get_noise_matrix_file_path():
	return img_src_path + '/' + noise_matrix_file_name


def get_full_img_path(img_name):
	return img_src_path + '/' + full_resized_img_dir + '/' + img_name


def get_full_mask_path(img_name):
	return img_src_path + '/' + full_masks_img_dir + '/' + img_name


def get_mask_path(mask_name):
	return img_src_path + '/' + masks_images_dir + '/' + mask_name + '.png'


def get_output_img_path(img_name):
	return img_src_path + '/' + output_dir + '/' + output_img_dir + '/' + img_name + '.png'


def get_test_output_img_path(img_name):
	return img_src_path + '/' + output_dir + '/' + test_output_img_dir + '/' + img_name + '.tiff'


def get_output_label_path_v1(img_name):
	return img_src_path + '/' + output_dir + '/' + output_labels_dir + '/v1/' + img_name + '.npy'


def get_output_label_path_v2(img_name):
	return img_src_path + '/' + output_dir + '/' + output_labels_dir + '/v2/' + img_name + '.npy'


def generate_img_file_name():
	return str(uuid4())
