// Short Trial 5-inspired print plate. Reconstruction, NOT original BOSL2 mesh.
// Node >=18; no dependencies. Outputs one directly printable STL.
import {writeFileSync} from 'node:fs';
const TWO=Math.PI*2, N=36, pitch=3, dZ=.12, slops=[.20,.20,.20,.16,.24];
const R=(h,a)=>h/Math.max(Math.abs(Math.sin(a)),Math.abs(Math.cos(a)));
const frac=(a,z,depth)=>{
  const q=.5*depth*Math.tan(Math.PI/12)/pitch;
  const p=((z/pitch-a/TWO+.5)%1+1)%1-.5, x=Math.abs(p),lo=.25-q,hi=.25+q;
  return x<=lo?0:x>=hi?1:(x-lo)/(hi-lo);
};
const triangles=[], add=(a,b,c)=>triangles.push([a,b,c]);
const angles=Array.from({length:N},(_,i)=>TWO*i/N);
const ring=(cx,cy,z,r)=>angles.map(a=>[cx+Math.cos(a)*r(a,z),cy+Math.sin(a)*r(a,z),z]);
const band=(a,b,out)=>{
  for(let i=0;i<N;i++){const j=(i+1)%N;
    if(out){add(a[i],a[j],b[j]);add(a[i],b[j],b[i]);}
    else{add(a[i],b[j],a[j]);add(a[i],b[i],b[j]);}
  }
};
const cap=(inner,outer,up)=>{
  for(let i=0;i<N;i++){const j=(i+1)%N;
    if(up){add(inner[i],outer[i],outer[j]);add(inner[i],outer[j],inner[j]);}
    else{add(inner[i],inner[j],outer[j]);add(inner[i],outer[j],outer[i]);}
  }
};
const disk=(r,center,up)=>{
  for(let i=0;i<N;i++){const j=(i+1)%N;if(up)add(center,r[i],r[j]);else add(center,r[j],r[i]);}
};
function screw(cx){
  const footR=(a)=>R(3.5,a),bottom=ring(cx,0,0,footR),top=ring(cx,0,1.6,footR);
  disk(bottom,[cx,0,0],false);band(bottom,top,true);
  const threadR=(a,z)=>1.6-.9*frac(a,z-1.6,.9);
  let prev=ring(cx,0,1.6,threadR);cap(prev,top,true);
  for(let i=1;i<=150;i++){const z=1.6+18*i/150,next=ring(cx,0,z,threadR);band(prev,next,true);prev=next;}
  disk(prev,[cx,0,19.6],true);
}
function pin(cx,slop){
  const outside=a=>R(2.2,a),square=a=>R(1.76,a);
  const hole=(a,z)=>{
    const thread=1.7+2*slop-1.35*frac(a,z,1.35);
    if(z<=10)return thread;
    if(z>=10.12)return square(a);
    const t=(z-10)/.12;return (1-t)*thread+t*square(a);
  };
  const z=[0];
  for(let i=1;i<83;i++)z.push(10*i/83);
  z.push(10,10.12);
  for(let i=1;i<67;i++){const x=10+8*i/67;if(x>10.12)z.push(x);}
  z.push(18);
  let outer=ring(cx,0,0,(a)=>outside(a)),inner=ring(cx,0,0,hole);
  cap(inner,outer,false);
  for(const h of z.slice(1)){const o=ring(cx,0,h,(a)=>outside(a)),v=ring(cx,0,h,hole);
    band(outer,o,true);band(inner,v,false);outer=o;inner=v;}
  cap(inner,outer,true);
}
slops.forEach((s,i)=>{screw(i*14);pin(i*14+7,s);});
const f=x=>{const t=Math.round(x*1000)/1000;return Object.is(t,-0)?'0':String(t);};
const data=['solid trial5_short_comparison\n'];
for(const tri of triangles){
  data.push('facet normal 0 0 0\nouter loop\n');
  for(const v of tri)data.push('vertex ',f(v[0]),' ',f(v[1]),' ',f(v[2]),'\n');
  data.push('endloop\nendfacet\n');
}
data.push('endsolid trial5_short_comparison\n');
writeFileSync(new URL('./trial5-short-comparison-plate.stl',import.meta.url),data.join(''));
console.log(triangles.length+' STL facets written');
