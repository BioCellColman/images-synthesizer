import numpy as np
import utils.utils as utils
from utils.consts import *
from handlers import files_handler as fh


class LabelHandler:
    def __init__(self, img_h, img_w, layers_count):
        self.label = np.zeros(shape=(layers_count, img_w, img_h))
        self.label_v2 = np.zeros(shape=(layers_count + 1, img_w, img_h))
        self.img_h = img_h
        self.img_w = img_w
        self.layers_count = layers_count

    def check_position(self, col, row, mask):
        ex_lyr_1 = self.__extract_sub_matrix_from_layer(self.label, LAYER_1, row, col, mask)
        ex_lyr_2 = self.__extract_sub_matrix_from_layer(self.label, LAYER_2, row, col, mask)

        layer_1_used = np.any(ex_lyr_1 > 0)
        layer_2_used = np.any(ex_lyr_2 > 0)

        result = LAYER_1
        change_other_layer = layer_1_used or layer_2_used
        if layer_1_used and layer_2_used:
            result = INVALID_POS
            change_other_layer = False
        elif layer_1_used:
            result = LAYER_2

        return result, change_other_layer

    def place_cell(self, col, row, mask, layer_num, change_other):
        height = mask.shape[0]
        width = mask.shape[1]

        # place cell in labels v1
        if not change_other:
            self.label[layer_num, :, :][row: row + height, col: col + width] += mask * 1
        elif change_other and layer_num == LAYER_1:
            self.__place_overlap_mask_v1(LAYER_1, LAYER_2, mask, row, col, height, width)
        else:
            self.__place_overlap_mask_v1(LAYER_2, LAYER_1, mask, row, col, height, width)

        # place cell in labels v2
        if not change_other:
            self.label_v2[layer_num, :, :][row: row + height, col: col + width] += mask
        elif change_other and layer_num == LAYER_1:
            self.__place_overlap_mask_v2(LAYER_1, LAYER_2, mask, row, col, height, width)
        else:
            self.__place_overlap_mask_v2(LAYER_2, LAYER_1, mask, row, col, height, width)

    def save_label(self, img_name):
        self.__set_background()
        v1_path = fh.get_output_label_path_v1(img_name)
        v2_path = fh.get_output_label_path_v2(img_name)
        np.save(v1_path, self.label)
        np.save(v2_path, self.label_v2)

    @staticmethod
    def __extract_sub_matrix_from_layer(label, layer, row, col, mask):
        height = mask.shape[0]
        width = mask.shape[1]
        layer_matrix = label[layer, :, :]
        return utils.extract_sub_matrix(layer_matrix, row, col, height, width) * mask

    def __place_overlap_mask_v1(self, lyr_to_place, lyr_to_fix, mask, row, col, height, width):
        ex_lyr_to_fix = self.__extract_sub_matrix_from_layer(self.label, lyr_to_fix, row, col, mask)
        self.label[lyr_to_place, :, :][row: row + height, col: col + width] += mask
        self.label[lyr_to_place, :, :][row: row + height, col: col + width] -= ex_lyr_to_fix * mask * 0.5
        self.label[lyr_to_fix, :, :][row: row + height, col: col + width] -= ex_lyr_to_fix * mask * 0.5

    def __place_overlap_mask_v2(self, lyr_to_place, lyr_to_fix, mask, row, col, height, width):
        ex_layer_to_fix = self.__extract_sub_matrix_from_layer(self.label_v2, lyr_to_fix, row, col, mask)
        self.label_v2[lyr_to_place, :, :][row: row + height, col: col + width] += mask
        self.label_v2[lyr_to_place, :, :][row: row + height, col: col + width] -= ex_layer_to_fix
        self.label_v2[lyr_to_fix, :, :][row: row + height, col: col + width] -= ex_layer_to_fix
        self.label_v2[BOTH, :, :][row: row + height, col: col + width] += ex_layer_to_fix

    def __set_background(self):
        combined_v1 = self.label[LAYER_1, :, :] + self.label[LAYER_2, :, :]
        self.label[BACKGROUND, :, :] = np.where(combined_v1 > 0, 0, 1)
        combined_v2 = self.label_v2[LAYER_1, :, :] + self.label_v2[LAYER_2, :, :] + self.label_v2[BOTH, :, :]
        self.label_v2[BACKGROUND, :, :] = np.where(combined_v2 > 0, 0, 1)
