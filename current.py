import os
import urllib.request
from datetime import datetime, time, timedelta

import icm

def get_cached_url(url, filename, min_length = 1000):
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
    def __init__(self, row, col):
        self.row = row
        self.col = col

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
            if get_cached_url(url, filename):
                return filename, icm.Meteogram.build_fdate(fdate)