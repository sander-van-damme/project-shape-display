// Fast deterministic ensemble for finite_seat.py; same equations, checked against Python.
#include <cmath>
#include <iostream>
#include <iomanip>
#include <vector>
#include <algorithm>
struct State {double q,v;};
struct Case {double K,alpha,b,z,f;int sign;};
const double beta=std::acos(-1.)/3;
double dv(double q){return q*(1-q)*(1-2*q);}
double contact(double q,double v,const Case& c){
 if(q>=c.b)return 0;
 double J=std::cos(beta*(q-c.b)),p=-std::sin(beta*(q-c.b))/beta;
 return c.K*p*(1+c.alpha*std::max(-v*J,0.))*J;
}
double acc(State s,const Case& c,double a,int u){
 return a*u*std::cos(beta*(s.q-.5))-dv(s.q)-2*c.z*s.v+contact(s.q,s.v,c);
}
State step(State s,const Case& c,double h,double a,int u){
 double a1=acc(s,c,a,u);
 State s2={s.q+h*s.v/2,s.v+h*a1/2};double a2=acc(s2,c,a,u);
 State s3={s.q+h*s2.v/2,s.v+h*a2/2};double a3=acc(s3,c,a,u);
 State s4={s.q+h*s3.v,s.v+h*a3};double a4=acc(s4,c,a,u);
 return {s.q+h*(s.v+2*s2.v+2*s3.v+s4.v)/6,s.v+h*(a1+2*a2+2*a3+a4)/6};
}
int main(int argc,char**argv){
 if(argc!=4 && argc!=5)return 2;
 bool fixed=argc==5;
 double h=std::stod(argv[1]),horizon=std::stod(argv[2]),threshold=std::stod(argv[3]);
 Case c;bool first=true;std::cout<<std::setprecision(17)<<"[";
 while(std::cin>>c.K>>c.alpha>>c.b>>c.z>>c.f>>c.sign){
  std::vector<std::pair<double,int>> schedule;
  if(fixed){int n;std::cin>>n;for(int j=0;j<n;j++){double t;int u;std::cin>>t>>u;schedule.push_back({t,u});}}
  size_t edge=0;int fixed_u=0;
  double lo=0,hi=std::max(c.b,0.);
  for(int i=0;i<60;i++){double m=(lo+hi)/2;if(contact(m,0,c)-dv(m)>0)lo=m;else hi=m;}
  State s={(lo+hi)/2,0};double low=s.q,high=s.q,peak=0,cross=-1;int previous=9;
  std::vector<std::pair<double,int>> edges;
  for(int i=0;i<std::lround(horizon/h);i++){
   int u=s.v>=0?1:c.sign?-1:0;
   if(fixed){while(edge<schedule.size() && i*h+1e-10>=schedule[edge].first){fixed_u=schedule[edge].second;edge++;}u=fixed_u;}
   if(u!=previous)edges.push_back({i*h,u});previous=u;
   s=step(s,c,h,c.f*threshold,u);
   low=std::min(low,s.q);high=std::max(high,s.q);peak=std::max(peak,contact(s.q,s.v,c));
   if(s.q>=.5){cross=(i+1)*h;break;}
  }
  if(!first)std::cout<<",";first=false;
  std::cout<<"{\"K\":"<<c.K<<",\"compression_damping\":"<<c.alpha<<",\"seat_offset\":"<<c.b
  <<",\"well_damping\":"<<c.z<<",\"half_fraction\":"<<c.f<<",\"signed\":"<<(c.sign?"true":"false")
  <<",\"step\":"<<h<<",\"horizon\":"<<horizon<<",\"saddle_time\":";
  if(cross<0)std::cout<<"null";else std::cout<<cross;
  std::cout<<",\"min_q\":"<<low<<",\"max_q\":"<<high<<",\"peak_seat_force\":"<<peak<<",\"pulse_edges\":[";
  for(size_t j=0;j<edges.size();j++){if(j)std::cout<<",";std::cout<<"["<<edges[j].first<<","<<edges[j].second<<"]";}
  std::cout<<"]}";
 }
 std::cout<<"]\n";
}
