import os

get_all_images = [image for image in os.listdir() if "Image_Target" in image]
print(get_all_images)

