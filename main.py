#dependencies
import numpy as np
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt #plotting
import seaborn as sns #for beatiful visualization
import folium
from folium import plugins

#set file path
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
fire_nrt_m6 = pd.read_csv("fire_nrt_M6_101673.csv")
fire_archive_m6 = pd.read_csv("fire_archive_M6_101673.csv")
fire_nrt_v1 = pd.read_csv("fire_nrt_V1_101674.csv")
fire_archive_v1 = pd.read_csv("fire_archive_V1_101674.csv")

type(fire_nrt_v1)

df_merged = pd.concat([fire_archive_v1,fire_nrt_v1],sort=True)
data = df_merged
#data.head()
#data.info()
df_filter = data.filter(["latitude","longitude","acq_date","frp"])
df_filter.head()
df = df_filter[df_filter['acq_date']>='2019-11-01']
df.head()
data_topaffected = df.sort_values(by='frp',ascending=False).head(10)
data_topaffected
# Create a map
m = folium.Map(location=[-35.0, 144], control_scale=True, zoom_start=3, attr="text some")
df_copy = data_topaffected.copy()

# loop through data to create Marker for each hospital
for i in range(0, len(df_copy)):
    folium.Marker(
        location=[df_copy.iloc[i]['latitude'], df_copy.iloc[i]['longitude']],
        # popup=popup,
        tooltip="frp: " + str(df_copy.iloc[i]['frp']) + "<br/> date: " + str(df_copy.iloc[i]['acq_date']),
        icon=folium.Icon(color='red', icon='fire', prefix="fa"),
    ).add_to(m)
dfdate = df[['acq_date','frp']].set_index('acq_date')
dfdate_highest = dfdate.groupby('acq_date').sum().sort_values(by='frp',ascending=False)
dfdate_highest.head(10)
plt.figure(figsize=(10,5))
sns.set_palette("pastel")
ax = sns.barplot(x='acq_date',y='frp',data=df)
for ind, label in enumerate(ax.get_xticklabels()):
    if ind % 10 == 0:  # every 10th label is kept
        label.set_visible(True)
    else:
        label.set_visible(False)
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
plt.xlabel("Date")
plt.ylabel('FRP (fire radiation power)')
plt.title("time line of bushfire in Australia")
plt.tight_layout()