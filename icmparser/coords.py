from haversine import haversine

GRID_RESOLUTION = 7
LAT_DEGREE_ROWS = -28
LON_DEGREE_COLS = 17.5
REFERENCE_POINT_LL = (50, 19)
REFERENCE_POINT_RC = (465, 213)

def latlondst(p1, p2):
    return haversine(p1, p2)

def latlon2rowcol(lat, lon):
    dlat = lat - REFERENCE_POINT_LL[0]
    dlon = lon - REFERENCE_POINT_LL[1]

    row = REFERENCE_POINT_RC[0] + (round(dlat * LAT_DEGREE_ROWS/GRID_RESOLUTION)*GRID_RESOLUTION)
    col = REFERENCE_POINT_RC[1] + (round(dlon * LON_DEGREE_COLS/GRID_RESOLUTION)*GRID_RESOLUTION)
    return row, col

def rowcol2latlon(row, col):
    drow = row - REFERENCE_POINT_RC[0]
    dcol = col - REFERENCE_POINT_RC[1]

    lat = REFERENCE_POINT_LL[0] + drow/LAT_DEGREE_ROWS
    lon = REFERENCE_POINT_LL[1] + dcol/LON_DEGREE_COLS
    return lat, lon

def latlonradius2grid(lat, lon, radius):
    points = []
    center_row, center_col = latlon2rowcol(lat, lon)
    points.append((center_row, center_col))

    dr = 0
    while True:
        stopr = True
        for drv in [dr, -dr] if dr > 0 else [dr]:
            dc = 0
            while True:
                stopc = True
                for dcv in [dc, -dc] if dc > 0 else [dc]:
                    candidate = center_row + drv, center_col + dcv
                    if points[-1] == candidate:
                        stopc = stopr = False
                        continue

                    if latlondst(rowcol2latlon(*candidate), (lat, lon)) <= radius:
                        stopc = stopr = False
                        points.append(candidate)

                if stopc:
                    break
                dc += GRID_RESOLUTION
        if stopr:
            break
        dr += GRID_RESOLUTION
    return map(lambda p: rowcol2latlon(*p), points)