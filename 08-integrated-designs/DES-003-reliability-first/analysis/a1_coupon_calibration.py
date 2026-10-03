#!/usr/bin/env python3
"""Generate the Q-009 calibration plan; nominal blanks are not measurements."""
from __future__ import annotations
import argparse,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ROWS=[("latch_socket","binary latch cell","radial clearance",.10,.20,.30,"fit, bind, looseness"),("latch_lane","latch toe / owned lane","lane clearance",.10,.20,.30,"interference, stop engagement"),("reader_flag","frame-fixed flag reader","reader standoff",1.60,1.80,2.00,"single-cell contrast"),("registration","gantry registration","half-pitch offset",2.44,2.54,2.64,"seat, repeatability"),("slide","repeated-fit rail","running clearance",.10,.20,.30,"insert force, bind, wear")]
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("-o","--output",type=Path,default=ROOT/"analysis/a1_coupon_calibration.csv"); a=ap.parse_args(); a.output.parent.mkdir(parents=True,exist_ok=True)
 fields=["feature_id","interface","dimension","low_mm","nominal_mm","high_mm","observation","measured_mm","pass_fail","notes","evidence"]
 with a.output.open("w",newline="") as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
  for feature,interface,dimension,low,nominal,high,observation in ROWS: w.writerow(dict(feature_id=feature,interface=interface,dimension=dimension,low_mm=f"{low:.2f}",nominal_mm=f"{nominal:.2f}",high_mm=f"{high:.2f}",observation=observation,measured_mm="",pass_fail="",notes="",evidence="CAD-derived nominal; physical result unresolved"))
 print(f"wrote {len(ROWS)} rows to {a.output}")
 return 0
if __name__=="__main__": raise SystemExit(main())
