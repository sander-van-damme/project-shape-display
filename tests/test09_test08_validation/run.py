"""One-command local workflow. Optional --cad / --render need OpenSCAD."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cad',action='store_true');ap.add_argument('--render',action='store_true');args=ap.parse_args()
    commands=[['analyze.py'],['checks.py'],['qualify.py']]
    if args.cad or args.render:commands.append(['cad_check.py']+(['--render'] if args.render else []))
    for command in commands:
        subprocess.run([sys.executable,str(HERE/command[0]),*command[1:]],check=True)
    # Recalculate analytical outputs twice, compare bytes; CAD logs contain runtimes.
    names=['summary.json','worst_schedule.json','transitions.csv','timing_sweep.csv','levels.csv',
           'fit_sensitivity.csv','detent_torque.csv','structure.csv','lift_drive.csv','reliability.csv','multirow.csv','coupon_parameters.scad']
    def hashes():return {n:hashlib.sha256((HERE/'results'/n).read_bytes()).hexdigest() for n in names}
    before=hashes()
    subprocess.run([sys.executable,str(HERE/'analyze.py')],check=True,stdout=subprocess.DEVNULL)
    after=hashes()
    if before!=after:raise RuntimeError('non-deterministic analytical outputs')
    (HERE/'results/reproducibility.json').write_text(json.dumps({'python':sys.version,'analytical_sha256':after,'repeat_identical':True},indent=2)+'\n')
    print('Analytical outputs byte-identical on repeat; physical gates remain unverified.')


if __name__=='__main__':main()
