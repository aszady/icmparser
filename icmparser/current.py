import os
import urllib.request
from datetime import datetime, time, timedelta

import icmparser.icm as icm
from icmparser import coords


def get_cached_url(url, filename, min_length = 1000):
    print(url)
    if not os.path.exists(filename):
        try:
            f = urllib.request.urlopen(url)
        except Exception as e:
            print(e)
            return False
        content = f.read()
        if len(content) < min_length:
            return False
        with open(filename, 'wb') as ft:
            ft.write(content)
    return True


class CurrentMeteogram(object):

    def __init__(self, lat, lon, cache_dir='.'):
        self.row, self.col = coords.latlon2rowcol(lat, lon)
        self.lat, self.lon = coords.rowcol2latlon(self.row, self.col)
        self.cache_dir = cache_dir

        self.filename, self.fdate = self._fetch_file()
        self.meteogram = icm.Meteogram(self.filename, self.fdate)

    def _genfdates(self, to):
        date = to.date()
        while True:
            for hour in [18, 12, 6, 0]:
                dt = datetime.combine(date, time(hour))
                if dt > to:
                    continue
                yield dt
            date = date + timedelta(days=-1)

    def _fetch_file(self):
        for fdate in self._genfdates(datetime.utcnow()):
            url = 'http://www.meteo.pl/um/metco/mgram_pict.php?ntype=0u&fdate={}&row={}&col={}&lang=pl'.format(icm.Meteogram.build_fdate(fdate), self.row, self.col)
            filename = '{}.{}.{}.png'.format(icm.Meteogram.build_fdate(fdate), self.row, self.col)
            filepath = os.path.join(self.cache_dir, filename)
            if get_cached_url(url, filepath):
                return filepath, icm.Meteogram.build_fdate(fdate)

    def __getattr__(self, item):
        return getattr(self.meteogram, item)