import argparse
import cv2
import os
import time

start_time = time.time()
print('\n\n')
print('start time:', time.ctime())

parser = argparse.ArgumentParser(description="This is a in-home script developed by Raiman (ruiwenchen@um.edu.mo) for cut plate test photo.\n\
(more description updation)",\
formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument("-photo_folder", help="Folder path to store plate test images"
                                        "Make sure there are only plate test images in the folder. \n\n"
                                        )

parser.add_argument("-top_cut", type = float,  help = "Before detecting the edges of the plate, crop n*100%% of the photo's length from the top."
                                        "Set to a value between 0 and 0.5, default=0\n\n", default=0.0)

parser.add_argument("-bottom_cut", type = float,  help = "Before detecting the edges of the plate, crop n*100%% of the photo's length from the bottom."
                                        "Set to a value between 0 and 0.5, default=0\n\n", default=0.0)

parser.add_argument("-left_cut", type = float,  help = "Before detecting the edges of the plate, crop n*100%% of the photo's length from the left."
                                        "Set to a value between 0 and 0.5, default=0\n\n", default=0.0)

parser.add_argument("-right_cut", type = float,  help = "Before detecting the edges of the plate, crop n*100%% of the photo's length from the right."
                                        "Set to a value between 0 and 0.5, default=0\n\n", default=0.0)

parser.add_argument("-canny_down", type = int,  help = "Pixels with gradient values below this threshold are not considered as edges.\n\n", default=30)

parser.add_argument("-canny_up", type = int,  help = "Pixels with gradient values above this threshold are considered as strong edges\n\n", default=50)

parser.add_argument("-noise_threshold", type = int,  help = "Parameters that control noise.\n\
                     If the number of pixels considered to be edges in a row is less than noise_t, this row will be considered not to be the row where the plate is located (non-plate rows).\n\
                    It should be an integer and greater or equal than 1.\n\n", default=5)

parser.add_argument("-pass_height_length_ratio", type = float,  help = "Whether the height / length (or length / heigth, depending on which one is smaller) ratio of the image after cropping is less than pass_height_length_ratio.\n\
                     If it is less than this parameter, the cropping will be considered failed. default=0.98\n\n", default=0.98)

parser.add_argument("-output_path",  help = "output folder. default=./output\n\n", default="./output")



args = parser.parse_args()
folder_path = args.photo_folder
output_folder =args.output_path


top_cut = args.top_cut
bottom_cut = args.bottom_cut
left_cut = args.left_cut
right_cut = args.right_cut

canny_down = args.canny_down
canny_up = args.canny_up
noise_t = args.noise_threshold
pass_hl_ratio = args.pass_height_length_ratio


photos = os.listdir(folder_path)
pass_folder = os.path.join(output_folder, "pass")
fail_folder = os.path.join(output_folder, "fail")
fail_original_folder = os.path.join(output_folder, "fail", "original")
try:
    os.mkdir(output_folder)
except:
    pass

try:
    os.mkdir(pass_folder)
except:
    pass

try:
    os.mkdir(fail_folder)
except:
    pass

try:
    os.mkdir(fail_original_folder)
except:
    pass


fail_photos = []
for photo in photos:
    print("processing %s"%photo)
    photo_path = os.path.join(folder_path, photo)
    image = cv2.imread(photo_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height = image.shape[0]
    length = image.shape[1]

    top_border = int(height*top_cut)
    bottom_border = int(height - height*bottom_cut)
    left_border = int(length * left_cut)
    right_border = int(length - length*right_cut)
    image2 = image[top_border:bottom_border, left_border:right_border, :]

    # Convert the image to grayscale
    gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform edge detection using the Canny algorithm
    edges = cv2.Canny(blurred, canny_down, canny_up)
    
    edges = edges /255

    y=edges.sum(axis=1)
    x=edges.sum(axis=0)
    x_len = len(x)
    y_len = len(y)
    x_middle = int(x_len/2)
    y_middle = int(y_len/2)
    
    
    y_0_indices = [i for i, val in enumerate(y) if val <noise_t]
    y_top_list = [top for top in y_0_indices if top < y_middle]
    if(len(y_top_list)!=0):
        y_top = y_top_list[-1]
    else:
        y_top = 0

    y_bottom_list = [bottom for bottom in y_0_indices if bottom > y_middle]
    if(len(y_bottom_list)!=0):
        y_bottom = y_bottom_list[0]
    else:
        y_bottom = y_len
    

    image3 = image2[y_top:y_bottom,:,:]

    gray = cv2.cvtColor(image3, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform edge detection using the Canny algorithm
    edges = cv2.Canny(blurred, canny_down, canny_up)
    
    edges = edges /255

    y=edges.sum(axis=1)
    x=edges.sum(axis=0)
    x_len = len(x)
    y_len = len(y)
    x_middle = int(x_len/2)
    y_middle = int(y_len/2)

    x_0_indices = [i for i, val in enumerate(x) if val <noise_t]
    x_left_list =[left for left in x_0_indices if left < x_middle]
    if(len(x_left_list)!=0):
        x_left = x_left_list[-1]
    else:
        x_left = 0

    x_right_list =[right for right in x_0_indices if right > x_middle]
    if(len(x_right_list)!=0):
        x_right = x_right_list[0]
    else:
        x_right = x_len

    image_out = image3[:, x_left:x_right, :]

    o_height, o_length, _ = image_out.shape
    if(o_height/o_length>pass_hl_ratio and o_length/o_height>pass_hl_ratio):
        print("%s process successfully"%photo)
        output_photo_path = os.path.join(pass_folder, photo)
        cv2.imwrite(output_photo_path, image_out)
    else:
        print("%s do not pass height/length test"%photo)
        output_photo_path = os.path.join(fail_folder, photo)
        cv2.imwrite(output_photo_path, image_out)
        o_original_path = os.path.join(fail_original_folder, photo)
        cv2.imwrite(o_original_path, image)

    print()

elapsed_time = time.time() - start_time
print('end time:', time.ctime())
print('running time = %.2fs'%elapsed_time)
print('end')
