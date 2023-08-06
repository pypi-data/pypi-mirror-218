# pip install googletrans==3.1.0a0 #
from googletrans import Translator
# pip install opencv-python #
from cv2 import imwrite, imread, filter2D, bitwise_not, bitwise_or, transform, bilateralFilter, cvtColor, stylization, convertScaleAbs, detailEnhance, pencilSketch, GaussianBlur, medianBlur, warpAffine, getRotationMatrix2D, getGaussianKernel, threshold, adaptiveThreshold, bilateralFilter, bitwise_and, line, ellipse, putText, findContours, drawContours, FONT_HERSHEY_SIMPLEX, COLOR_BGR2HSV, inRange
# pip install rembg --user #
from rembg import remove
from numpy import uint8, zeros, copy, array, float64, matrix, where
from math import cos, sin

class create():
    def image(prompt, styles=['hyper_realistic'], aspectRatio='square'):
        url = f"https://firefly.adobe.com/generate/images?prompt={Translator().translate(prompt).text.replace(' ', '+')}&"
        for style in styles:
            url += f'style={style}&'
        return f"{url}aspectRatio={aspectRatio}&locale=en-en"

    def text(prompt, text = 'Firefly', font = 'acumin-pro-wide', background = 'transparent', fitType = 'tight'):
        return f"https://firefly.adobe.com/generate/font-styles?prompt={Translator().translate(prompt).text.replace(' ', '+')}&fitType={fitType}&text={text}&font={font}&bgColor={background}&textColor=%23000000"

class edit():
    def cut(image, startwidth, endwidth, startheight, endheight):
        imwrite(image, imread(image)[startheight:endheight, startwidth:endwidth])

    def rotate(image, gradus = 180):
        file = imread(image)
        imwrite(image, warpAffine(file, getRotationMatrix2D((file.shape[1] // 2, file.shape[0] // 2), gradus, 1), (file.shape[1], file.shape[0])))

    def blur(image, stage = 0):
        imwrite(image, GaussianBlur(imread(image), (stage+51, stage+51), 0))

    def bright(image, stage = 20):
        imwrite(image, convertScaleAbs(imread(image), beta = stage))

    def invert(image):
        imwrite(image, bitwise_not(imread(image)))

    def blackwhite(image):
        imwrite(image, cvtColor(imread(image), 6))

    def median(image, stage = 5):
        imwrite(image, medianBlur(imread(image), stage))

    def bilateral(image):
        imwrite(image, bilateralFilter(imread(image), 9, 75, 75))

    def scratch(image, scale=127):
        imwrite(image, cvtColor(imread(image), 6))
        imwrite(image, threshold(imread(image), scale, 255, 0)[1])

    def cartoon(image):
        file = imread(image)
        imwrite(image, bitwise_and(bilateralFilter(file, 9, 250, 250), file, mask = adaptiveThreshold(cvtColor(file, 6), 255, 0, 0, 9, 9)))

    def paint(image):
        imwrite(image, filter2D(imread(image), ddepth = -1, kernel = array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])))

    def paint2(image):
        imwrite(image, stylization(GaussianBlur(imread(image), (5, 5), 0, 0), sigma_s = 40, sigma_r = 0.1))

    def hd(image):
        imwrite(image, detailEnhance(imread(image), sigma_s = 12, sigma_r = 0.15))

    def pencil(image):
        imwrite(image, pencilSketch(imread(image), sigma_s = 60, sigma_r = 0.07, shade_factor = 0.1)[1])

    def vignette(image, level = 3):
        file = imread(image)
        kernel = getGaussianKernel(file.shape[0], file.shape[0]/level) * getGaussianKernel(file.shape[1], file.shape[1]/level).T
        mask = kernel / kernel.max()
        image_vignette = copy(file)
        for i in range(3):
            image_vignette[:,:,i] = image_vignette[:,:,i] * mask
        imwrite(image, image_vignette)

    def embossed(image):
        imwrite(image, filter2D(imread(image), -1, kernel = array([[0, -3, -3], [3, 0, -3], [3, 3, 0]])))

    def sepia(image):
        sepia = transform(array(imread(image), dtype=float64), matrix([[0.272, 0.543, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]))
        sepia[where(sepia > 255)]=255
        imwrite(image, array(sepia, dtype=uint8))

    def outline(image, level = 200):
        file = imread(image)
        img_grey = cvtColor(file, 6)
        ret, thresh_img = threshold(img_grey, level, 255, 0)
        contours, hierarchy = findContours(thresh_img, 3, 2)
        img_contours = uint8(zeros((file.shape[0], file.shape[1])))
        drawContours(img_contours, contours, -1, (255,255,255), 1)
        imwrite(image, drawContours(img_contours, contours, -1, (255,255,255), 1))

    def splash(image, lower = 20, upper = 32):
        img = imread(image)
        res = zeros(img.shape, uint8)
        mask = inRange(cvtColor(img, COLOR_BGR2HSV), array([lower,128,128]), array([upper,255,255]))
        for i in range(3):
            res[:, :, i] = bitwise_and(cvtColor(img, 6), cvtColor(img, 6), mask=bitwise_not(mask))
        imwrite(image, bitwise_or(bitwise_and(img, img, mask=mask), res))

    def backdrop(image, output):
        with open(image, 'rb') as i:
            with open(output, 'wb') as o:
                o.write(remove(i.read()))

class draw():
    def text(image, text, position, size = 4, color = (150, 120, 255), thickness = 6):
        imwrite(image, putText(imread(image), text, position, FONT_HERSHEY_SIMPLEX, size, color, thickness))

    def point(image, position, color = (150, 120, 255), thickness = 6):
        imwrite(image, line(imread(image), position, position, color, thickness))

    def line(image, start, end, color = (150, 120, 255), thickness = 6):
        imwrite(image, line(imread(image), start, end, color, thickness))

    def angle(image, center, firstradius, secondradius, degree = 0, inclination=90, color = (150, 120, 255), thickness = 3):
        file = imread(image)
        angle_radians = degree*0.017453292519943295
        inclination_radians = inclination*0.017453292519943295
        point1 = int(center[0] + firstradius * cos(angle_radians)), int(center[1] - firstradius * sin(angle_radians))
        point2 = int(center[0] + secondradius * cos(angle_radians + inclination_radians)), int(center[1] - secondradius * sin(angle_radians + inclination_radians))
        line(file, center, point1, color, thickness)
        line(file, center, point2, color, thickness)
        imwrite(image, file)

    def triangle(image, firstpoint, secondpoint, thirdpoint, degree = 0, color = (150, 120, 255), thickness = 3):
        file = imread(image)
        angle_radians = degree*0.017453292519943295
        rotated_firstpoint = (int(firstpoint[0] * cos(angle_radians) - firstpoint[1] * sin(angle_radians)), int(firstpoint[0] * sin(angle_radians) + firstpoint[1] * cos(angle_radians)))
        rotated_secondpoint = (int(secondpoint[0] * cos(angle_radians) - secondpoint[1] * sin(angle_radians)), int(secondpoint[0] * sin(angle_radians) + secondpoint[1] * cos(angle_radians)))
        rotated_thirdpoint = (int(thirdpoint[0] * cos(angle_radians) - thirdpoint[1] * sin(angle_radians)), int(thirdpoint[0] * sin(angle_radians) + thirdpoint[1] * cos(angle_radians)))
        line(file, rotated_firstpoint, rotated_secondpoint, color, thickness)
        line(file, rotated_secondpoint, rotated_thirdpoint, color, thickness)
        line(file, rotated_thirdpoint, rotated_firstpoint, color, thickness)
        imwrite(image, file)

    '''
    def quadrangle(): pass
    def pentagon(): pass
    def hexagon(): pass
    def heptagon(): pass
    def octagon(): pass
    '''

    def ellipse(image, center, axes = (100, 60), degree = 0, startAngle = 0, endAngle = 360, color = (150, 120, 255), thickness = 3):
        imwrite(image, ellipse(imread(image), center, axes, degree, startAngle, endAngle, color, thickness))

    def circle(image, center, radius = 20, startAngle = 0, endAngle = 360, color = (150, 120, 255), thickness = 3):
        imwrite(image, ellipse(imread(image), center, (radius, radius), 0, startAngle, endAngle, color, thickness))