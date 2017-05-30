import icmparser.postprocessors as postprocessors


class Detector(object):
    pass


class CurvyLine(Detector):
    def __init__(self, color):
        self.color = color

    def __call__(self, img):
        data = {}
        for x in range(img.width):
            col = []
            for y in range(img.height):
                if img(x, y) == self.color:
                    col.append(y)
            data[x] = col
        return data


class VerticalScale(Detector):
    def __init__(self, ocr):
        self.ocr = ocr

    def _read_scale(self, img_scale):
        data = {}
        for y in range(img_scale.height - self.ocr.glyph_height):
            clip = img_scale.clip(0, y, img_scale.width-1, y+ self.ocr.glyph_height-1)
            decoded = self.ocr.decode_rtl(clip)
            if len(decoded):
                label = float(''.join(decoded))
                data[y+self.ocr.glyph_height/2] = label
        return data

    DOTTED_LINE_COLOR = 60
    def _detect_dotted_lines(self, img_chart):
        ys = []
        for y in range(img_chart.height):
            count = 0
            for x in range(img_chart.width):
                if max(img_chart(x, y)) <= self.DOTTED_LINE_COLOR:
                    count += 1
            if count*3 >= img_chart.width:
                ys.append(y)
        return ys

    def __call__(self, img_scale, img_chart):
        assert(img_scale.height == img_chart.height)
        scale = self._read_scale(img_scale)
        lines = self._detect_dotted_lines(img_chart)
        nearest = postprocessors.Nearest(lines)
        def as_nearest(item):
            approx_y, label = item
            return nearest(approx_y), label
        scale = dict(map(as_nearest, scale.items()))
        return scale
