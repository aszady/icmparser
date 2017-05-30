import argparse
import json

from datetime import datetime, timedelta

from icmparser.current import CurrentMeteogram

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='ICM image parser')
    ap.add_argument('--lat', metavar='X', required=True, type=int)
    ap.add_argument('--lon', metavar='X', required=True, type=int)
    args = ap.parse_args()

    current = CurrentMeteogram(args.lat, args.lon)
    meteo = current.meteogram

    print(json.dumps({
        'source':{
            'fdate': meteo.build_fdate(meteo.date),
            'row': current.row,
            'col': current.col
        },
        'temperature': meteo.get_temperature(datetime.utcnow()),
        'temperature_1h': meteo.get_temperature(datetime.utcnow()+timedelta(hours=1))
    }))
