#!/usr/bin/env python3
"""Publication-size figure of DES-008 full-scan conditional timing categories.

Reads canonical JSON; does not rerun or change the engineering calculations.
Requires matplotlib. Example from any cwd:
  python /path/to/analysis/plot_timing.py --output-prefix /path/to/work/des008-timing
"""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


def categories(case,scene,stroke):
    preset='40mm' if stroke==40 else 'deep'
    return [
        ('Local reveal',case['local_reveal']['revised_seconds']),
        ('Cold start',case['cold_start']['revised_seconds']),
        ('Scene transition',scene['revised_seconds']),
        ('Sustained mean',case['sustained'][preset]['mean_revised_seconds']),
        ('Neutral + first',case['neutral_then_first']['revised_seconds']),
        ('Dense all levels',case['dense_all_levels']['revised_seconds']),
    ]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=Path(__file__).with_name('revised-system-results.json'))
    parser.add_argument('--output-prefix',type=Path,required=True)
    args=parser.parse_args()
    data=json.loads(args.input.read_text())
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':11,
        'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':9,
        'pdf.fonttype':42,'ps.fonttype':42,'savefig.facecolor':'white'})
    below='#285f85';above='#ad5d1e';threshold='#87354d'
    fig,axes=plt.subplots(2,2,figsize=(11.7,8.3),sharex=True)
    fig.subplots_adjust(left=.135,right=.975,bottom=.145,top=.805,wspace=.50,hspace=.40)
    for row,n in enumerate((64,80)):
        for col,stroke in enumerate((40,50)):
            key=f'N{n}_stroke{stroke}_row80_full_scan'
            case=data['category_cases'][key]
            items=categories(case,data['scene_cases'][key],stroke);ax=axes[row,col]
            labels=[name for name,_ in items];values=[value for _,value in items]
            ax.barh(range(len(items)),values,height=.66,color=[below if v<=30 else above for v in values],zorder=3)
            for y,value in enumerate(values):
                ax.text(value-.65,y,f'{value:.1f}',ha='right',va='center',color='white',weight='bold',fontsize=9,zorder=5)
            ax.axvline(30,color=threshold,linewidth=1.4,linestyle=(0,(4,3)),zorder=4)
            ax.set_yticks(range(len(items)),labels);ax.invert_yaxis()
            ax.set_xlim(0,50);ax.set_xticks(range(0,51,10));ax.grid(axis='x',color='#dce3e8',linewidth=.6,zorder=0)
            ax.set_title(f'{n} × {n} outputs  |  {stroke}-mm travel\n{406.4/n:.2f}-mm pitch',loc='left',pad=10)
            ax.tick_params(axis='both',length=0,pad=5)
            for spine in ax.spines.values():spine.set_visible(False)
            if row==1:ax.set_xlabel('Time (seconds)',labelpad=7)
    fig.suptitle('Stationary full-scan lift: conditional update times',x=.03,y=.98,ha='left',fontsize=17,weight='bold')
    fig.text(.03,.935,'Two independent banks  •  80-ms complete row write  •  5-mm height increments',fontsize=10)
    fig.legend(handles=[Patch(color=below,label='At or below 30 s in the model'),
        Patch(color=above,label='Above 30 s in the model'),
        Line2D([0],[0],color=threshold,linewidth=1.4,linestyle=(0,(4,3)),label='30-s benchmark')],
        loc='upper left',bbox_to_anchor=(.023,.912),ncol=3,frameon=False,fontsize=9,handlelength=2,columnspacing=2)
    fig.text(.03,.065,'Assumed actuator rates; no physical performance qualification. Full-scan programming includes every row in each mask.',fontsize=9)
    fig.text(.03,.041,'Includes forced seating after both signs, finite movement, mask clearing and a retry time reserve. Unknown-OLD reset is unqualified.',fontsize=8.6)
    fig.text(.03,.019,'Source: revised-system-results.json. Guide embodiment has an admitted-play collision; conditional timing does not establish a working machine.',fontsize=8,color='#4f5962')
    args.output_prefix.parent.mkdir(parents=True,exist_ok=True)
    metadata={'Title':'DES-008 conditional full-scan update timing','Author':'Shape Display engineering',
        'Subject':'Conditional calculation; not physical timing qualification'}
    for extension in ('png','pdf'):
        path=args.output_prefix.with_suffix('.'+extension)
        fig.savefig(path,dpi=200,metadata=metadata if extension=='pdf' else {'Software':'Matplotlib','Description':metadata['Subject']})
        print(path)
    plt.close(fig)


if __name__=='__main__':main()
