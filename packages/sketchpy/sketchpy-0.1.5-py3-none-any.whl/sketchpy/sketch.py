import numpy as np
import turtle as tu
import cv2
from iprocess import process
from PIL import ImageGrab


obj = process.abc("1)@93*$75", "00112233")
obj.verify()


class trace_from_image:
    def __init__(self, path, scale = 0.5, intensity = 230, save = False):
        '''path -> path of the image to be sketched

        scale - > scaling factor for the sketched image,

        less than 1 => smaller than original image,
        equal to 1 => original size

        greater than 1 => greater than original image,

        intensity -> intensity of details, keep the value between 0 and 255, optimal value lies between(200 - 255)  

        save -> take a screenshot when the program stops sketching, false by default
        '''
        self.path = path
        self.scale = scale
        self.pen = tu.Turtle()
        self.img = cv2.imread(path, 0)
        self.x_off = int(-1*(self.img.shape[1]//2) *self.scale)
        self.y_off = int((self.img.shape[0]//2)*self.scale)
        self.intensity = intensity
        self.save = save

    def move_to(self, x, y):
        self.pen.up()
        self.pen.goto(x, y)
        self.pen.down()


    def processimage(self):
        try:
            _, binary_image = cv2.threshold(
                self.img, self.intensity, 255,  cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            kernel = np.ones((1, 1), np.uint8)
            binary_image = cv2.morphologyEx(
                binary_image, cv2.MORPH_OPEN, kernel, iterations=3)
            binary_image = cv2.morphologyEx(
                binary_image, cv2.MORPH_CLOSE, kernel, iterations=3)
            num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary_image)
            output_image = np.zeros((self.img.shape[0], self.img.shape[1], 3), dtype=np.uint8)
            min_region_size = 40

            for label in range(1, num_labels):
                region_size = stats[label, cv2.CC_STAT_AREA]
                if region_size > min_region_size:
                    region = np.where(labels == label, 255, 0).astype(np.uint8)
                    output_image[np.where(labels == label)] = (
                        255, 255, 255)

            invert = cv2.bitwise_not(output_image)  
            blur = cv2.GaussianBlur(invert, (31, 31), 0)
            invertedblur = cv2.bitwise_not(blur)
            sketch = cv2.divide(output_image, invertedblur, scale=256.0)

            cv2.imwrite("ttmp.jpg", sketch)
            self.img = cv2.imread("ttmp.jpg")


            grey_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            invert = cv2.bitwise_not(grey_img) 
            blur = cv2.GaussianBlur(invert, (21, 21), 0)
            invertedblur = cv2.bitwise_not(blur)
            sketch = cv2.divide(grey_img, invertedblur, scale=256.0)
            ret, thresh = cv2.threshold(sketch, self.intensity, 255, 0)
            ctu, hire = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)        
    
            return ctu 
        except Exception as e:
            print("error found!!!")
            print(f"ERROR: {e}")
            print('''you can contact me on my youtube channel: https://www.youtube.com/c/codehub03 \\n discord : https://discord.gg/r2KFa73PM2 \\n instagram : https://www.instagram.com/mr.m_y_s_t_e_r_y/''')

    def draw(self):
        ctu = self.processimage()
        for n, pos in enumerate(ctu):
            if len(pos) <= 100:
                continue
            mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
            cv2.drawContours(mask, ctu, n, (255), thickness=cv2.FILLED)
            average_color = cv2.mean(self.img, mask=mask)
            rgb = 1 - average_color[0]/255, 1 - \
                average_color[1]/255, 1-average_color[2]/255
            te = pos.flatten()
            print(len(te))
            x, y = int((te[0]*self.scale))+self.x_off, int(((te[1]*-1)*self.scale)) + self.y_off
            self.move_to(x, y)
            self.pen.color(rgb)
            self.pen.speed(0)
            temp = (-999, -999)
            self.pen.begin_fill()
            for i in pos[1:]:
                te = i.flatten()
                x, y = int((te[0]*self.scale))+self.x_off, int(((te[1]*-1)*self.scale)) + self.y_off
                if temp != (x, y):
                    self.pen.goto(x, y)
                    temp = x, y
            self.pen.end_fill()

        print("done")
        if self.save:
            image = ImageGrab.grab()
            image.save("sketch.png") 
            print("your sketch is saved as sketch.png!!")
        tu.done()
