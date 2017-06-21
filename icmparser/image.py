import PIL.Image


class Image(object):
    def __init__(self, image_path):
        img = PIL.Image.open(image_path)
        img.load()
        self.rgbim = img.convert('RGB')
        self.width = self.rgbim.width
        self.height = self.rgbim.height

    def __call__(self, x, y):
        return self.rgbim.getpixel((x, y))

    def clip(self, x1, y1, x2, y2):
        return ClippedImage(self, x1, y1, x2, y2)


class ClippedImage(object):
    def __init__(self, img, x1, y1, x2, y2):
        self.img = img
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = x2-x1+1
        self.height = y2-y1+1

    def __call__(self, x, y):
        assert(0 <= x < self.width)
        assert(0 <= y < self.height)
        return self.img(x+self.x1, y+self.y1)

    def clip(self, x1, y1, x2, y2):
        return ClippedImage(self.img, x1+self.x1, y1+self.y1, x2+self.x1, y2+self.y1)


def pixel_dst(rgb1, rgb2):
    return pow(sum([(rgb1[i]-rgb2[i])**2 for i in range(len(rgb1))]), .5)


def match(img1, img2):
    assert(img1.width == img2.width)
    assert(img1.height == img2.height)

    dst = 0
    for y in range(img1.height):
        for x in range(img2.width):
            dst += pixel_dst(img1(x,y), img2(x,y))
    return 1./(dst+1)