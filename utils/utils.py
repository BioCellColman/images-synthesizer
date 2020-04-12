import random

import matplotlib.pyplot as plt
from skimage import io

from handlers import files_handler as fh
from utils.consts import *


def get_max_width(df):
    return (df["right_x"] - df["left_x"]).max()


def get_max_height(df):
    return (df["bottom_y"] - df["top_y"]).max()


def get_random_images(images_names, img_num):
    images_indexes = random.sample(range(0, len(images_names)), img_num)
    img_map = {}
    for index in images_indexes:
        img_name = images_names[index]
        img_map[img_name] = read_image(img_name)
    return img_map


def pick_random_mask(df):
    return df.sample()


def read_mask(mask_row):
    return flat_mask_img(io.imread(fh.get_mask_path(mask_row.mask_id.values[0])))


def read_mask_by_id(mask_id):
    return flat_mask_img(io.imread(fh.get_mask_path(mask_id)))


def read_image(image_name):
    return io.imread(fh.get_full_img_path(image_name))


def read_image_full_mask(image_name):
    return io.imread(fh.get_full_mask_path(image_name))


def show_image(img, title='IMAGE', save=False):
    plt.gray()
    fig, axs = plt.subplots(1, 1, figsize=(8, 8))
    axs.imshow(img)
    axs.title.set_text(title)
    if save:
        plt.savefig(fh.get_test_output_img_path(title))
    plt.show()


def extract_cell_image(left_x, right_x, top_y, bottom_y, source_img, mask):
    extracted = source_img[left_x-MASK_PADDING:right_x+MASK_PADDING, top_y-MASK_PADDING:bottom_y+MASK_PADDING]
    return extracted * mask


def flat_mask_img(mask):
    return mask[:, :, 0] / 255


def extract_sub_matrix(source, row, col, height, width):
    return source[row: row + height, col: col + width]


def get_bad_masks(df):
    bad_masks = []
    for index, row in df.iterrows():
        mask_img = read_mask_by_id(row.mask_id)
        height = row.right_x - row.left_x + 2 * MASK_PADDING
        width = row.bottom_y - row.top_y + 2 * MASK_PADDING
        if mask_img.shape[0] != height or mask_img.shape[1] != width:
            bad_masks.append(row.mask_id)
    return bad_masks


def get_random_cell_count():
    return random.randint(CELL_COUNT - CELL_COUNT_PAD, CELL_COUNT + CELL_COUNT_PAD)
