GRID_RESOLUTION = 7
LAT_DEGREE_ROWS = -28
LON_DEGREE_COLS = 17.5
REFERENCE_POINT_LL = (50, 19)
REFERENCE_POINT_RC = (465, 213)

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