# -*- code: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

csv_path = "shouene_地域.csv"
shouene = pd.read_csv(csv_path, index_col="地域ID")
font = {"family": "TakaoGothic"}
matplotlib.rc("font", **font)
plt.rcParams["font.size"] = 18
fig, (axex1, axes2) = plt.subplots(ncols=2,figsize=(23,10))
axes1.scatter(shouene["人口(千人)"], shouene["セッション"])
axes1.set_xlabel("人口(千人)")
axes1.set_ylabel("セッション数")
axes1.grid(True)
axes2.scatter(shouene["持家(戸数)"], shouene["所定内給与(千円)"])
axes2.set_xlabel("持家(戸数)")
axes2.set_ylabel("所定内給与(千円)")
axes2.hlines(y=300, xmin=0, xmax=21500, colors="r", linewidths=2)
axes2.vlines(x=10000, ymin=230, ymax=380, colors="b", linewidths=2)
axes2.grid(True)
#axes.set_xlim([0, 3000])
#axes.set_ylim([0, 15000])
for k, v in shouene.iterrows():
    axes1.annotate(v[0], xy=(v[6], v[1]), size=15)
    axes2.annotate(v[0], xy=(v[8], v[7]), size=15)
    
fig.savefig("都道府県別_セッション_人口_持家_給与.png")
plt.close("all")
