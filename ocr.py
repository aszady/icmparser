import operator

import image


class OCR(object):
    def __init__(self, font_file, chars='0123456789'):
        self.fontimg = image.Image(font_file)
        self.chars = chars
        self.glyph_height = self.fontimg.height
        self.glyph_width = self.fontimg.width // len(chars)
        self.glyph_spacing = 1
        self.threshold = .5

    def decode_rtl(self, img):
        x = img.width - self.glyph_width
        y = 0

        result = []
        while True:
            match = self(img.clip(x, y, x+self.glyph_width-1, y+self.glyph_height-1))
            if match[1] > self.threshold:
                result.append(match[0])
            else:
                break
            x -= self.glyph_width + self.glyph_spacing

        return list(reversed(result))

    def __call__(self, img):
        values = []
        for i in range(10):
            glyph = self.fontimg.clip(i*self.glyph_width, 0, (i+1)*self.glyph_width-1, self.glyph_height-1)
            match = image.match(glyph, img)
            values.append(match)
        best = max(enumerate(values), key=operator.itemgetter(1))
        return self.chars[best[0]], best[1]