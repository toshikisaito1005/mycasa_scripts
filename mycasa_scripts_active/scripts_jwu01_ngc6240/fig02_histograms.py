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
ax1.grid(which='major',linestyle='--')           # 図にグリッドを表示させます
plt.rcParams["font.size"] = 22                   # 図中の文字サイズの設定

ax1.hist(co10,)