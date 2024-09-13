# Import block
from PIL import Image

# Variables 
input_image = Image.open("images/Olympus.jpg")

# Define function to clear EXIF
def clear_EXIF(EXIF_input_image):
    image_in_progress = input_image                                             # Initialise image to work with
    image_data = list(image_in_progress.getdata())                              # Take EXIF data from picture
    output_image = Image.new(image_in_progress.mode, image_in_progress.size)    # Creats output image from input one
    output_image.putdata(image_data)                                            # Put new clear data
    output_image.save("images/output_image.jpg")                                # Saves output image


clear_EXIF(input_image)                                                         # Call function
