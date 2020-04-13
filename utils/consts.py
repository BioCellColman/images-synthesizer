# number of images to synthesize
IMAGES_TO_CREATE = 3000
# number of original images to draw cells from each time
SRC_IMG_NUM = 5
# quantity of cells in each synthesized image
CELL_COUNT = 300
CELL_COUNT_PAD = 100
# number of attempts to place a particular cell in the image
PLACING_ATTEMPTS = 5
# image dimensions
IMAGE_HEIGHT = 572
IMAGE_WIDTH = 572
LAYERS_COUNT = 3

# layers
BACKGROUND = 0
LAYER_1 = 1
LAYER_2 = 2
BOTH = 3
INVALID_POS = 4

# define all relevant files paths
# TODO : change to your data base directory
img_src_path = 'C:\\Users\\yarde\\Documents\\BioCell\\data'
# img_src_path = '/content/drive/My Drive/BioCell/images-synthesizer'
# inputs
csv_file_name = 'filtered_cells.csv'
noise_matrix_file_name = 'noise_matrix.npy'
full_resized_img_dir = 'resized_images'
full_masks_img_dir = 'masks_images'
masks_images_dir = 'extracted_masks_images'
# outputs
output_dir = 'output'
output_img_dir = 'output_images'
test_output_img_dir = 'test_output_images'
output_labels_dir = 'output_labels'

# extras
MASK_PADDING = 3
