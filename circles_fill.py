import cv2
import os

path_file = os.path.abspath('cats.jpg')

# print(path_file)

image = cv2.imread(path_file)
window_name = 'Show_image'

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 600, 600)
cv2.imshow(window_name, image)

center_coordinate = (150, 150)
radius = 30
color = (0, 0, 255)
thickness = -1

image = cv2.circle(image, center_coordinate, radius, color, thickness)

cv2.imshow(window_name, image)
cv2.waitKey(0)
cv2.destroyAllWindows()
