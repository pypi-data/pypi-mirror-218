import algorithms
import cv2


image = cv2.imread('Unknown.png', cv2.IMREAD_GRAYSCALE)
cv2.imshow('image', image)
# waits for user to press any key
# (this is necessary to avoid Python kernel form crashing)
x = algorithms.IE(image)
image_output = x.MVSIHE()
cv2.imshow('output',image_output)

cv2.waitKey(0)
# closing all open windows
cv2.destroyAllWindows()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

