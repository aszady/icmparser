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

    def _chart(self, y):
        return self.CHART_X[0], y[0], self.CHART_X[1], y[1]

    def _scale(self, y):
        return self.SCALE_X[0], y[0], self.SCALE_X[1], y[1]

    def _clip(self, y):
        return self._chart(y), self._scale(y)

    def temperature_clip(self):
        return self._clip(self.TEMPERATURE_Y)

    def wind_clip(self):
        return self._clip(self.WIND_Y)


class StandardHeightFormat(MeteogramFormat):
    IMG_HEIGHT = 660

    TEMPERATURE_Y = 56, 135
    WIND_Y = 316, 395


class ShortFormat(StandardHeightFormat):
    IMG_WIDTH = 540

    CHART_X = 62, 477
    SCALE_X = 40, 56

    DAY_WIDTH = 168
    WARMUP_PIXELS = 7


class LongFormat(StandardHeightFormat):
    IMG_WIDTH = 630

    CHART_X = 68, 561
    SCALE_X = 47, 63

    DAY_WIDTH = 154
    WARMUP_PIXELS = 6


class StandardInterpreter(object):
    def __init__(self, img_chart, img_scale, scale_ocr, line_color):
        detected = charts.CurvyLine(line_color)(img_chart)
        selected = postprocessors.Selector()(detected)
        self.values = interpolators.LinearInterpolator(selected)

        detected = charts.VerticalScale(scale_ocr)(img_scale, img_chart)
        self.scale = interpolators.LinearInterpolator(detected)

    def __call__(self, x):
        return self.scale(self.values(x))

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
        self._parse_wind()

    @classmethod
    def build_fdate(cls, dt):
        return dt.strftime(cls.FDATE_FORMAT)

    def _build_standard_interpreter(self, clip, color):
        return StandardInterpreter(
            self.img.clip(*clip[0]),
            self.img.clip(*clip[1]),
            self.ocr8,
            color
        )

    def _parse_temperature(self):
        self.temperature = self._build_standard_interpreter(
            self.format.temperature_clip(),
            (255, 0, 0)
        )

    def _parse_wind(self):
        self.wind = self._build_standard_interpreter(
            self.format.wind_clip(),
            (17, 17, 153)
        )

    def _time_to_x(self, time):
        delta = time - self.date
        pixdelta = delta.total_seconds() / 60 / 60 / 24 * self.format.DAY_WIDTH - self.format.WARMUP_PIXELS
        return pixdelta

    def get_temperature(self, time):
        return self.temperature(self._time_to_x(time))

    def get_wind(self, time):
        return self.wind(self._time_to_x(time))