// E-150: finite reciprocal elastic network + unilateral/Jenkins contacts; SI.
// Scenario parameters, not fitted material or manufactured resonator predictions.
#include <array>
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <iomanip>
#include <iostream>
using A=std::array<double,12>;
constexpr double pi=3.141592653589793;
struct Model {
 double N=6,mu=.1,kt=20e6,kn=60e6,ks=60e3,kg=40e6,kc=25e6,kf=0;
 double kb=0;
 double freq=40000,Q=40,amp=1,phase=0,sign=1,ton=.03,toff=.03,dt=1e-7;
 double W[2]={1,0},mr[2]={.12,.02};
 A q{},v{},m{},d{},decay{}; std::array<double,4> e{};
 double heat=0,work=0,positive=0,absorbed=0,neighbor_slip=0,negative_contact_heat=0;
 Model(){m.fill(.001);m[8]=m[9]=.002;}
 double kh()const{return .002*std::pow(2*pi*40000,2)-2*kc;}
 double normal(int i)const{return std::max(0.,N+kn*q[2*i]);}
 double drive(int j,double t)const{
  if(t>=ton)return 0;
  double ramp=std::min(1.,t/.001);
  return amp*ramp*(j==8?40*std::cos(2*pi*freq*t):sign*20*std::sin(2*pi*freq*t+phase));
 }
 void init(){
  m[10]=mr[0];m[11]=mr[1];
  for(int j=0;j<10;j++){d[j]=m[j]*2*pi*40000/Q;decay[j]=std::exp(-d[j]*dt/(2*m[j]));}
  double aa=kg+kf+kc,bb=kg+kf,det=aa*bb-kf*kf;
  double z0=-(W[0]*bb+kf*W[1])/(2*det),z1=-(W[1]*aa+kf*W[0])/(2*det);
  for(int i=0;i<4;i++){q[2*i+1]=i<2?z0:z1;e[i]=std::min(W[i/2]/2,mu*N)/kt;}
  q[10]=z0-W[0]/(2*kt);q[11]=z1-W[1]/(2*kt);
 }
 A force(double t)const{
  A f{};
  for(int i=0;i<4;i++){
   int n=2*i,z=n+1,r=10+i/2;
   f[n]=-ks*q[n]-(normal(i)-N);f[z]=-kg*q[z]-kt*e[i];f[r]+=kt*e[i];
   if(i<2){double s=i==0?1:-1;for(int a=0;a<2;a++){
    double c=kc*(q[n+a]-s*q[8+a]);f[n+a]-=c;f[8+a]+=s*c;
   }}
  }
  for(int cell=0;cell<2;cell++){int j=4*cell;double b=kb*(q[j]+q[j+2]);f[j]-=b;f[j+2]-=b;}
  for(int j=0;j<4;j++){double c=kf*(q[j]-q[j+4]);f[j]-=c;f[j+4]+=c;}
  for(int j=8;j<10;j++)f[j]+=-kh()*q[j]+drive(j,t);
  for(int r=0;r<2;r++)f[10+r]-=W[r];
  return f;
 }
 double energy()const{
  double en=0;
  for(int j=0;j<12;j++)en+=.5*m[j]*v[j]*v[j];
  for(int i=0;i<4;i++){
   double x=q[2*i],z=q[2*i+1],nn=normal(i);
   en+=.5*ks*x*x+(nn*nn-N*N)/(2*kn)-N*x+.5*kg*z*z+.5*kt*e[i]*e[i];
   if(i<2)for(int a=0;a<2;a++){double c=q[2*i+a]-(i==0?1:-1)*q[8+a];en+=.5*kc*c*c;}
  }
  for(int cell=0;cell<2;cell++)en+=.5*kb*std::pow(q[4*cell]+q[4*cell+2],2);
  for(int j=0;j<4;j++)en+=.5*kf*std::pow(q[j]-q[j+4],2);
  en+=.5*kh()*(q[8]*q[8]+q[9]*q[9]);
  for(int r=0;r<2;r++)en+=W[r]*q[10+r];
  return en;
 }
 void damp(){for(int j=0;j<10;j++){double vv=v[j]*decay[j];heat+=.5*m[j]*(v[j]*v[j]-vv*vv);v[j]=vv;}}
 void step(double t){
  damp();A f=force(t),old=q;
  for(int j=0;j<12;j++){v[j]+=.5*dt*f[j]/m[j];q[j]+=dt*v[j];}
  for(int i=0;i<4;i++){
   double previous=e[i];
   double trial=previous+q[2*i+1]-old[2*i+1]-(q[10+i/2]-old[10+i/2]);
   double cap=mu*normal(i)/kt;e[i]=std::clamp(trial,-cap,cap);
   // Midpoint integral f dp; also equals interface work minus elastic
   // storage change. Track negative quadrature increments as model error.
   double dq=.5*kt*(previous+e[i])*(trial-e[i]);
   heat+=dq;negative_contact_heat+=std::max(0.,-dq);
   if(i>=2)neighbor_slip+=std::abs(trial-e[i]);
  }
  A fn=force(t+dt);
  for(int j=0;j<12;j++)v[j]+=.5*dt*fn[j]/m[j];
  for(int j=8;j<10;j++){
   double dw=.5*(drive(j,t)+drive(j,t+dt))*(q[j]-old[j]);
   work+=dw;positive+=std::max(0.,dw);absorbed+=std::max(0.,-dw);
  }
  damp();
 }
};
int main(int argc,char**argv){
 Model a;
 // N W0 W1 mu kt kframe_fraction amp phase sign Q freq dt ton toff initial_v kbridge
 if(argc!=17 && argc!=18){std::cerr<<"16 numeric arguments plus optional imposed-stall flag required\n";return 2;}
 double p[16];for(int i=0;i<16;i++)p[i]=std::atof(argv[i+1]);
 a.N=p[0];a.W[0]=p[1];a.W[1]=p[2];a.mu=p[3];a.kt=p[4];a.kf=p[5]*a.kg;
 a.amp=p[6];a.phase=p[7];a.sign=p[8];a.Q=p[9];a.freq=p[10];a.dt=p[11];a.ton=p[12];a.toff=p[13];
 for(int j=0;j<2;j++)a.mr[j]=a.W[j]>=5?1.1:a.W[j]>.01?.12:.02;
 a.kb=p[15];a.init();a.v[10]=p[14];
 if(argc==18 && std::atof(argv[17])!=0)a.m[10]=1e99; // external stall fixture only
 double e0=a.energy(),y0=a.q[10],n0=a.q[11],cuty=y0,cutv=0,cute=0,startavg=0;
 double minN=1e99,maxN=0,maxfoot=0,maxneighbor=0,postmin=1e99,postmax=-1e99,tailv=0,minAll=1e99,minOff=1e99,peakAll=0,maxNormal=0;
 long duty=0,stick=0,count=0,gap=0;bool cut=false;
 int steps=std::lround((a.ton+a.toff)/a.dt);
 for(int k=0;k<steps;k++){
  double t=k*a.dt;
  if(!cut && t+1e-12>=a.ton){cut=true;cuty=a.q[10];cutv=a.v[10];cute=a.energy()-a.W[0]*a.q[10]-a.W[1]*a.q[11];}
  if(std::abs(t-.8*a.ton)<a.dt/2){startavg=a.q[10];}
  a.step(t);
  minAll=std::min(minAll,a.normal(0)+a.normal(1));
  if(cut)minOff=std::min(minOff,a.normal(0)+a.normal(1));
  for(int i=0;i<4;i++){maxfoot=std::max(maxfoot,std::abs(a.q[2*i+1]));peakAll=std::max(peakAll,a.normal(i));maxNormal=std::max(maxNormal,std::abs(a.q[2*i]));}
  maxneighbor=std::max(maxneighbor,std::abs(a.q[11]-n0));
  if(t>=.8*a.ton && t<a.ton){
   gap+=(a.normal(0)+a.normal(1))==0;minN=std::min(minN,a.normal(0)+a.normal(1));maxN=std::max({maxN,a.normal(0),a.normal(1)});
   for(int i=0;i<2;i++){duty+=a.normal(i)>0;stick+=std::abs(a.kt*a.e[i])<a.mu*a.normal(i)*(1-1e-8);count++;maxfoot=std::max(maxfoot,std::abs(a.q[2*i+1]));}
  }
  if(cut){postmin=std::min(postmin,a.q[10]-cuty);postmax=std::max(postmax,a.q[10]-cuty);}
  if(t>a.ton+a.toff-.002)tailv=std::max(tailv,std::abs(a.v[10]));
 }
 std::cout<<std::setprecision(12)<<"{\"v_drive\":"<<(cuty-startavg)/(.2*a.ton)
 <<",\"y_drive\":"<<cuty-y0<<",\"v_cut\":"<<cutv<<",\"cut_stored_J\":"<<cute
 <<",\"post_min\":"<<postmin<<",\"post_max\":"<<postmax<<",\"final_v\":"<<a.v[10]
 <<",\"tail_max_v\":"<<tailv<<",\"neighbor_max\":"<<maxneighbor<<",\"neighbor_final\":"<<a.q[11]-n0
 <<",\"min_total_N\":"<<minN<<",\"max_pad_N\":"<<maxN<<",\"contact_duty\":"<<double(duty)/std::max(1L,count)
 <<",\"stick_fraction\":"<<double(stick)/std::max(1L,count)<<",\"max_foot_t\":"<<maxfoot
 <<",\"work_J\":"<<a.work<<",\"positive_driver_J\":"<<a.positive<<",\"absorbed_driver_J\":"<<a.absorbed
 <<",\"max_normal_mode\":"<<maxNormal
 <<",\"min_total_all_N\":"<<minAll<<",\"min_total_off_N\":"<<minOff<<",\"max_pad_all_N\":"<<peakAll
 <<",\"gap_fraction\":"<<double(2*gap)/std::max(1L,count)<<",\"neighbor_slip_path\":"<<a.neighbor_slip
 <<",\"negative_contact_heat_J\":"<<a.negative_contact_heat
 <<",\"heat_J\":"<<a.heat<<",\"energy_residual_J\":"<<a.energy()-e0-a.work+a.heat<<"}\n";
}
