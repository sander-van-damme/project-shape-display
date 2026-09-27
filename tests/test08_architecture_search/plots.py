"""Optional static engineering figures from generated metrics; matplotlib 3.8.2."""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent


def main():
    out=HERE/'results'; metric=json.loads((out/'metrics.json').read_text())
    rows=list(csv.DictReader((out/'timing_sweep.csv').open()))
    fig, axes=plt.subplots(1,3,figsize=(14,4.6),layout='constrained')
    fig.suptitle('80 x 80 terrain display: conditional feasibility, not product qualification',fontsize=15)
    for channels,color in [(40,'#ab5745'),(80,'#26756a')]:
        data=[r for r in rows if int(r['channels'])==channels and float(r['couple_each_s'])==.025]
        axes[0].plot([float(r['step_rate_hz']) for r in data],[float(r['time_s']) for r in data],
                     'o-',label=f'{channels} head channels',color=color)
    axes[0].axhline(30,color='#a02132',linestyle='--',label='30 s limit')
    axes[0].set(xlabel='Assumed loaded step rate (pulses/s)',ylabel='Complete map time (s)',title='All cells homed and rewritten',ylim=(0,100))
    axes[0].legend(fontsize=8)
    bom=metric['bom']; labels=['Low','Working','High']; values=[bom[k]*1.2 for k in ['low','working','high']]
    axes[1].bar(labels,values,color=['#91b4a0','#d89c56','#b76c65'])
    axes[1].axhline(500,color='#a02132',linestyle='--'); axes[1].axhline(400,color='#7f858a',linestyle=':')
    for i,value in enumerate(values): axes[1].text(i,value+15,f'${value:.0f}',ha='center')
    axes[1].set(ylabel='Purchased USD including 20% allowance',title='Unquoted cost scenarios',ylim=(0,1050))
    for name in ['solid','hollow']:
        variant=metric['mass_variants'][name]; weight=variant['forces']['column_weight_n']*1000
        axes[2].bar(name,weight,label=name,color='#26756a' if name=='solid' else '#91b4a0')
        axes[2].text(name,weight+.7,f'{weight:.1f} mN',ha='center')
    axes[2].axhline(5,color='#a02132',linestyle='--',label='Assumed drag, unmeasured')
    axes[2].set(ylabel='Gravity return force per column (mN)',title='Return margin depends on friction',ylim=(0,26))
    axes[2].legend(fontsize=8,loc='upper right')
    for ax in axes:
        ax.spines[['top','right']].set_visible(False); ax.grid(axis='y',alpha=.18)
    fig.savefig(out/'engineering_summary.png',dpi=160)
    fig.savefig(out/'engineering_summary.svg')
    print(f'Figures written with matplotlib {matplotlib.__version__}')


if __name__=='__main__': main()
