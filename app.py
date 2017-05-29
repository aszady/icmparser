import argparse
import json

from datetime import datetime, timedelta

from icmparser.current import CurrentMeteogram

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='ICM image parser')
    ap.add_argument('--row', metavar='X', required=True, type=int)
    ap.add_argument('--col', metavar='X', required=True, type=int)
    args = ap.parse_args()

    icm = CurrentMeteogram(args.row, args.col).meteogram

    print(json.dumps({
        'fdate': icm.build_fdate(icm.date),
        'temperature': icm.get_temperature(datetime.utcnow()),
        'temperature_1h': icm.get_temperature(datetime.utcnow()+timedelta(hours=1))
    }))
