import os
from datetime import datetime

import icmparser.charts as charts
import icmparser.image as image
import icmparser.interpolators as interpolators
import icmparser.ocr as ocr
import icmparser.postprocessors as postprocessors

class MeteogramFormat(object):
    @classmethod
    def formats(cls):
        return [ShortFormat, LongFormat]

    @classmethod
    def detect(cls, img):
        for format in cls.formats():
            if img.width == format.IMG_WIDTH and img.height == format.IMG_HEIGHT:
                return format()
        return None


class ShortFormat(MeteogramFormat):
    IMG_WIDTH = 540
    IMG_HEIGHT = 660

    TEMPERATURE_CLIP = (62, 56, 477, 135)
    TEMPERATURE_SCALE = (40, 56, 56, 135)
    DAY_WIDTH = 168
    WARMUP_PIXELS = 7


class LongFormat(MeteogramFormat):
    IMG_WIDTH = 630
    IMG_HEIGHT = 660

    TEMPERATURE_CLIP = (68, 56, 561, 135)
    TEMPERATURE_SCALE = (47, 56, 63, 135)
    DAY_WIDTH = 154
    WARMUP_PIXELS = 6


class Meteogram(object):
    # eg. `2017052606`
    FDATE_FORMAT = '%Y%m%d%H'

    def __init__(self, image_path, fdate, format = None):
        self.img = image.Image(image_path)
        self.date = datetime.strptime(fdate, self.FDATE_FORMAT)
        self.lat, self.lon = None, None
        if format is None:
            format = MeteogramFormat.detect(self.img)
        self.format = format
        self.ocr8 = ocr.OCR(os.path.join(os.path.dirname(__file__), 'fonts/scale.png'))

        self._parse_temperature()

    @classmethod
    def build_fdate(cls, dt):
        return dt.strftime(cls.FDATE_FORMAT)

    def _parse_temperature(self):
        temperature = self.img.clip(*self.format.TEMPERATURE_CLIP)
        detected = charts.CurvyLine(temperature, (255, 0, 0))()
        selected = postprocessors.Selector()(detected)
        self.temperature = interpolators.LinearInterpolator(selected)

        temperature_scale = self.img.clip(*self.format.TEMPERATURE_SCALE)
        detected = charts.VerticalScale(self.ocr8)(temperature_scale, temperature)
        self.temperature_scale = interpolators.LinearInterpolator(detected)

    def _time_to_x(self, time):
        delta = time - self.date
        pixdelta = delta.total_seconds() / 60 / 60 / 24 * self.format.DAY_WIDTH - self.format.WARMUP_PIXELS
        return pixdelta

    def get_temperature(self, time):
        return self.temperature_scale(self.temperature(self._time_to_x(time)))