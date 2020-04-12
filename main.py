from utils.consts import *
from utils.utils import *
from handlers import image_handler
from handlers import label_handler
from handlers import files_handler as fh
import pandas as pd
import numpy as np

print("starting to synthesize images..")
print("*******************************")

# read the csv file
csv_file_data = pd.read_csv(fh.get_csv_file_path())
max_width = get_max_width(csv_file_data)
max_height = get_max_height(csv_file_data)
images_names = csv_file_data.src_img_name.unique()
bad_masks = get_bad_masks(csv_file_data)

noise_matrix = np.load(fh.get_noise_matrix_file_path())

# for IMAGES_TO_CREATE - create new image and label:
for img_index in range(IMAGES_TO_CREATE):
    print(f"creating image no. {img_index + 1}")
    # choose SRC_IMG_NUM images to draw cells from + read images
    images_map = get_random_images(images_names, SRC_IMG_NUM)
    # filter the csv table to only images masks
    masks_csv_data = csv_file_data[(csv_file_data.src_img_name.isin(list(images_map.keys())))&(~csv_file_data.mask_id.isin(bad_masks))]

    # create plain label matrix + plain image matrix
    img_handler = image_handler.ImageHandler(IMAGE_HEIGHT, IMAGE_WIDTH, max_height, max_width, noise_matrix)
    lbl_handler = label_handler.LabelHandler(IMAGE_HEIGHT, IMAGE_WIDTH, LAYERS_COUNT)

    for cell_index in range(get_random_cell_count()):
        try:
            # pick a mask + extract its image matrix
            mask_row = pick_random_mask(masks_csv_data)
            mask_img = read_mask(mask_row)
            extracted_cell = extract_cell_image(mask_row.left_x.values[0],
                                                mask_row.right_x.values[0],
                                                mask_row.top_y.values[0],
                                                mask_row.bottom_y.values[0],
                                                images_map[mask_row.src_img_name.values[0]],
                                                mask_img)

            # for PLACING_ATTEMPTS - try to place the cell
            placed = False
            for attempt in range(PLACING_ATTEMPTS):
                # randomly pick a position
                col = img_handler.get_random_col_pos()
                row = img_handler.get_random_row_pos()
                # check position validity
                result_layer, change_other = lbl_handler.check_position(col, row, mask_img)

                if not result_layer == INVALID_POS:
                    img_handler.place_cell(col, row, extracted_cell)
                    lbl_handler.place_cell(col, row, mask_img, result_layer, change_other)
                    placed = True
                    break

            if not placed:
                print(f"failed to place cell..")
        except:
            print("bad mask..")

    # add noise to background and normalized
    img_handler.add_background_noise()
    img_handler.normalize()

    # save the image + label giving them a UUID to identify
    img_name = fh.generate_img_file_name()
    img_handler.save_image(img_name)
    lbl_handler.save_label(img_name)

print("*******************************")
print("Done.")
