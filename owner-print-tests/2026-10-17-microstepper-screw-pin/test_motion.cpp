// Host test of the same travel policy compiled into the Uno firmware.
// g++ -std=c++11 test_motion.cpp -o /tmp/test-motion && /tmp/test-motion
#include <cassert>
#include <limits>
#include <initializer_list>
#include "controller/motion_policy.h"
int main() {
  int32_t n=0, pos=0;
  assert(STEPS_PER_REV==160);
  assert(planMove(true,pos,.5f,n)); pos+=n; assert(pos==80);
  assert(!planMove(true,pos,.01f,n)); // cannot cross upper travel boundary
  assert(planMove(true,pos,-1.f,n)); pos+=n; assert(pos==-80);
  assert(!planMove(true,pos,-.01f,n)); // cannot cross lower travel boundary
  assert(planMove(true,pos,.5f,n)); pos+=n; assert(pos==0);
  for(int i=0;i<20;i++) {
    for(float rev : {.5f,-1.f,.5f}) {
      assert(planMove(true,pos,rev,n)); pos+=n;
      assert(pos>=-PIN_LIMIT && pos<=PIN_LIMIT);
    }
    assert(pos==0);
  }
  assert(!planMove(true,0,0.f,n));
  assert(!planMove(true,0,1.01f,n));
  assert(!planMove(true,0,std::numeric_limits<float>::quiet_NaN(),n));
  assert(!planMove(true,0,std::numeric_limits<float>::infinity(),n));
  assert(planMove(false,0,1.f,n) && n==160);
  assert(planMove(false,0,-1.f,n) && n==-160);
}
