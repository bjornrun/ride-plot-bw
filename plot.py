import sys
import pandas as pd
import folium
import datetime as dt


def _plot_bw_data(src_file: str, dst_file: str) -> None:
    df = pd.read_csv(src_file, index_col='datetime', parse_dates=True).fillna(0)
    print(df.head())
    print(df.info())
    df = df[(df['lat'] != 0) & (df['lon'] != 0)]
    lon_max = df['lon'].max()
    lon_min = df['lon'].min()
    lon_mean = df['lon'].mean()
    lat_max = df['lat'].max()
    lat_min = df['lat'].min()
    lat_mean = df['lat'].mean()

    m = folium.Map(width=2048, height=2048, location=[lat_max, lon_max], zoom_start=11, min_zoom=5, max_zoom=19)

    oneday = dt.timedelta(1)
    currentday = df.index[0].replace(hour=0, minute=0, second=0, microsecond=0)
    lastday = df.index[-1]
    while currentday < lastday:
        tmp_df = df[(df.index >= currentday) & (df.index <= currentday + oneday)]
        if len(tmp_df) > 0:
            f = folium.FeatureGroup(currentday.strftime('%Y-%02m-%d'))
            for i, row in tmp_df.iterrows():
                folium.vector_layers.CircleMarker((row['lat'], row['lon']), popup=i.strftime('%Y-%02m-%d'),
                                                  tooltip='Ride',
                                                  color='red', weight=1, radius=1).add_to(f)
                folium.vector_layers.PolyLine([(row['lat'], row['lon']), (row['client_lat'], row['client_lon'])],
                                              popup="&uarr; {up} MB/s</br>&darr; {down} MB/s".format(
                                                  up=row['bw_up'] / (1024.0 * 1024),
                                                  down=row['bw_down'] / (1024.0 * 1024)),
                                              tooltip="&uarr; {up} MB/s</br>&darr; {down} MB/s".format(
                                                  up=row['bw_up'] / (1024.0 * 1024),
                                                  down=row['bw_down'] / (1024.0 * 1024)),
                                              color='blue', weight=1).add_to(f)
            f.add_to(m)
        currentday += oneday

    folium.LayerControl().add_to(m)
    m.save(dst_file)


if __name__ == '__main__':
    if sys.argv == 1:
        _plot_bw_data("/mnt/bandwidth.csv", "/mnt/bandwidth_plot.html")
    else:
        print("Src:", sys.argv[1], " Dst:", sys.argv[2])
        _plot_bw_data(sys.argv[1], sys.argv[2])
