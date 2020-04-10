import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
plt.ioff()

# データを読み込む。
data = np.loadtxt("n6240_mom8_data.txt")
dist = data[:,0]
co10 = data[:,1]
co21 = data[:,2]

# plotに向けての下準備です。
fig = plt.figure(figsize=(10,10))                # 図の大きさの設定
ax1 = fig.add_subplot(111)                       # これはおまじないです
ax1.grid(which='both',linestyle='--')            # 図にグリッドを表示させます
plt.rcParams["font.size"] = 22                   # 図中の文字サイズの設定
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.85)  # 図の余白設定

cscatter = ax1.scatter(np.log10(co10),           # data for x-axis
                       np.log10(co21),           # data for y-axis
                       lw = 0,                   # 点の輪郭の太さ
                       c = dist,                 # data for colorbar
                       cmap = "jet",             # color code for c
                       alpha = 0.5,              # 点の透明度
                       s = 40,                   # 点の大きさ
                       norm=Normalize(vmin=0, vmax=7)) # おまじないです

ax1.plot([-10,10],[-10,10],"k-",lw=2)            # 1:1の線を引く

cbar = plt.colorbar(cscatter)

ax1.set_xlim([-0.7,1.7])                         # xの範囲の指定
ax1.set_ylim([-0.7,1.7])                         # yの範囲の指定
cbar.set_clim([0,7])                             # colorbarの範囲の指定

ax1.set_xlabel("CO(1-0) Brightness Temperature (K)") # xlabel
ax1.set_ylabel("CO(2-1) Brightness Temperature (K)") # ylabel
cbar.set_label("Distance (kpc)")                 # colorbar label

plt.savefig("figure_co21_vs_co10.png",dpi=300)
