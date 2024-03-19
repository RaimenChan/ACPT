# ACPT
Auto Crop Plate Test Images

# install the required packages
```
conda create -n plate_test
conda activate plate_test
pip install opencv-python 
pip install matplotlib
```


# parameters
A more detailed introduction is in the introduction slide and introduction notebook.
```
-photo_folder PHOTO_FOLDER  
                            Folder path to store plate test imagesMake sure there are only plate test images in the folder.

-top_cut TOP_CUT            
                            Before detecting the edges of the plate, crop n*100% of the photo's length from the top.Set to a value between 0 and 0.5, default=0

-bottom_cut BOTTOM_CUT      
                            Before detecting the edges of the plate, crop n*100% of the photo's length from the bottom.Set to a value between 0 and 0.5, default=0

-left_cut LEFT_CUT          
                            Before detecting the edges of the plate, crop n*100% of the photo's length from the left.Set to a value between 0 and 0.5, default=0

-right_cut RIGHT_CUT        
                            Before detecting the edges of the plate, crop n*100% of the photo's length from the right.Set to a value between 0 and 0.5, default=0

-canny_down CANNY_DOWN      
                            Pixels with gradient values below this threshold are not considered as edges. default=30

-canny_up CANNY_UP          
                            Pixels with gradient values above this threshold are considered as strong edges default=50

-noise_threshold NOISE_THRESHOLD    
                            Parameters that control noise. If the number of pixels considered to be edges in a row is less than noise_t, this row will be considered not to be the row where the plate is located (non-plate rows). It should be an integer and greater or equal than 1. default=5

-pass_height_length_ratio PASS_HEIGHT_LENGTH_RATIO  
                            Whether the height / length (or length / heigth, depending on which one is smaller) ratio of the image after cropping is less than pass_height_length_ratio. If it is less than this parameter, the cropping will be considered failed. default=0.98

-output_path OUTPUT_PATH 
                            output folder

```

# usage
## (1) use 1 image to find the best parameter for you samples
```
python auto_crop_plate_test_parameter.py -image path/to/your/image 
```
Test with different canny_down, canny_up, noise_threshold to find the parameters that best suit your sample.


## (2) put all the plate test images in a folder.

Using default parameter (Cropping results may not be good)
```
python auto_crop_plate_test.py -photo_folder path/to/your/plate_test_folder -output_path path/to/your/output_folder
```

Using the best parameters you find
```
python auto_crop_plate_test.py -photo_folder path/to/your/plate_test_folder -output_path path/to/your/output_folder -top_cut a -bottom_cut b -left_cut c -right_cut d -canny_down best_canny_down -canny_up best_canny_up -noise_threshold best_noise_thredhold
```








