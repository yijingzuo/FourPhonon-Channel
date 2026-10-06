"""Small plotting helper; matplotlib is imported only when requested."""

from pathlib import Path
import numpy as np
from .channel_io import CHANNELS


def plot_channels(data, output):
    import matplotlib.pyplot as plt
    colors=("#4C6A92","#C17C74","#6E9F75","#C9A66B","#A77B9F")
    fig,axes=plt.subplots(1,2,figsize=(11,4.7))
    for ax,order in zip(axes,("3ph","4ph")):
        d=data[order]; acoustic=d["branch"]<=3
        for color,name in zip(colors,CHANNELS[order]):
            m=acoustic & (d[name]>0)
            ax.scatter(d["frequency"][m]/(2*np.pi),d[name][m],s=20,alpha=.7,label=name,color=color)
        ax.set_yscale("log"); ax.set_xlabel("Target frequency (THz)"); ax.set_title(order); ax.legend(frameon=False)
    axes[0].set_ylabel("Scattering rate (ps$^{-1}$)")
    fig.tight_layout(); fig.savefig(Path(output),dpi=250); plt.close(fig)
