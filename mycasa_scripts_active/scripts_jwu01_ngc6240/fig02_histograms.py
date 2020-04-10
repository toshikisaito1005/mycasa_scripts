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
fig = plt.figure(figsize=(10,5))             # 図の大きさの設定
ax1 = fig.add_subplot(111)                   # これはおまじないです
ax1.grid(axis="x",linestyle='--')            # 図にグリッドを表示させます
plt.rcParams["font.size"] = 22               # 図中の文字サイズの設定

# ヒストグラムの準備
bins = 100
historange = [0.0,25.]

ax1.hist(co10,
	     bins = bins,
	     range = historange,
	     normed=True,
	     lw = 0,
	     alpha = 0.5,
	     c = "blue")

ax1.hist(co21,
	     bins = bins,
	     range = historange,
	     normed=True,
	     lw = 0,
	     alpha = 0.5)

ax1.set_xlim(historange)                      # xの範囲の指定
ax1.set_ylim([0,0.8])                         # yの範囲の指定

plt.savefig("/Users/saito/Desktop/figure_histo_co10.png",dpi=300)
