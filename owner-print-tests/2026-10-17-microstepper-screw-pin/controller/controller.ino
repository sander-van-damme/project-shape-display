// Arduino Uno R3 + TMC2208, external R110 shunts, VREF initially 0.80 V.
// TMCStepper 0.7.3. Wiring and mandatory current-setting procedure: electronics.md.
#include <TMCStepper.h>
#include <SoftwareSerial.h>
#include "motion_policy.h"

constexpr uint8_t STEP_PIN=2, DIR_PIN=3, EN_PIN=4, RX_PIN=8, TX_PIN=9;
constexpr bool REVERSE_DIR=false; // verify direction with +0.25 rev before pin test
constexpr uint32_t IDLE_MS=30000, MAX_RUN_MS=120000;
SoftwareSerial uart(RX_PIN, TX_PIN);
TMC2208Stepper driver(&uart, 0.11f);
bool armed=false, pinModeActive=false;
int32_t position=0;
float rpm=5;
uint32_t lastActivity=0, runStart=0;
char line[40]; uint8_t used=0; bool overflow=false;

void off() {
  digitalWrite(EN_PIN,HIGH); digitalWrite(STEP_PIN,LOW);
  armed=false; position=0;
}

bool configureDriver() {
  off();
  if (driver.version()!=0x20) { Serial.println(F("ERROR: no TMC2208 UART reply")); return false; }
  uint8_t before=driver.IFCNT();
  driver.pdn_disable(true);
  driver.I_scale_analog(true); driver.internal_Rsense(false);
  driver.mstep_reg_select(true); driver.en_spreadCycle(true);
  driver.toff(4); driver.blank_time(24); driver.vsense(true);
  driver.microsteps(MICROSTEPS); driver.intpol(false);
  driver.ihold(5); driver.irun(5); driver.iholddelay(0);
  driver.TPOWERDOWN(0); driver.VACTUAL(0);
  // IFCNT counts accepted UART writes. These registers are read back from IC.
  uint8_t after=driver.IFCNT();
  uint32_t gc=driver.GCONF(), cc=driver.CHOPCONF();
  // Exactly 15 writes above in pinned TMCStepper 0.7.3: reject even one lost
  // write, especially IHOLD_IRUN (write-only on this chip).
  bool ok=uint8_t(after-before)==15 && (gc & 0xC7)==0xC5 &&
          ((cc>>17)&1)==1 && ((cc>>24)&15)==5 && (cc&15)==4;
  if (!ok) Serial.println(F("ERROR: driver configuration/UART verification failed"));
  return ok;
}

// Any received '!' stops within one short polling interval, even during motion.
// Other input during motion is discarded, never queued as a surprise next move.
bool checkStop() {
  while (Serial.available()) {
    if (Serial.read()=='!') {
      off(); used=0; overflow=false;
      Serial.println(F("STOP: disabled; manual centre invalid")); return false;
    }
  }
  if (millis()-runStart>=MAX_RUN_MS) {
    off(); Serial.println(F("STOP: 120 s run limit; inspect temperature and recenter"));
    return false;
  }
  return armed;
}

bool waitUs(uint32_t period) {
  uint32_t start=micros();
  while (uint32_t(micros()-start)<period) if (!checkStop()) return false;
  return true;
}

bool moveRevs(float revs) {
  int32_t steps;
  if (!armed || !planMove(pinModeActive,position,revs,steps)) {
    Serial.println(F("REJECT: not armed, invalid distance or manual travel limit")); return false;
  }
  digitalWrite(DIR_PIN,(steps>0)^REVERSE_DIR); delayMicroseconds(10);
  digitalWrite(EN_PIN,LOW); delay(5);
  uint32_t count=abs(steps);
  for (uint32_t i=0;i<count;i++) {
    if (!checkStop()) return false;
    uint32_t edge=min(i,count-1-i);
    // Short ramp: 2 rpm to selected speed over 16 microsteps, then back down.
    float v=min(rpm,2.0f+(rpm-2.0f)*min(edge,16UL)/16.0f);
    uint32_t period=uint32_t(60000000.0f/(STEPS_PER_REV*v));
    digitalWrite(STEP_PIN,HIGH); delayMicroseconds(5); digitalWrite(STEP_PIN,LOW);
    position += steps>0 ? 1 : -1;
    if (!waitUs(period-5)) return false;
  }
  lastActivity=millis();
  Serial.print(F("DONE; commanded rev from centre="));
  Serial.println(float(position)/STEPS_PER_REV,3);
  return true;
}

bool number(const char *text,float &out) {
  char *end; out=strtod(text,&end);
  if (end==text || !isfinite(out)) return false;
  while (*end==' ') ++end;
  return *end==0;
}

void command(char *s) {
  lastActivity=millis();
  if (!strcmp(s,"OFF")) { off(); Serial.println(F("OFF; manual centre invalid")); return; }
  if (!strcmp(s,"?")) {
    Serial.println(F("ARM MOTOR (pin detached); ARM PIN (manually centred); S rpm [2..120]; M rev [-1..1]; C cycles [1..20]; ! stop; OFF")); return;
  }
  if (!strcmp(s,"ARM MOTOR") || !strcmp(s,"ARM PIN")) {
    if (armed) { Serial.println(F("REJECT: OFF first; detach/recentre before ARM")); return; }
    bool pin=s[4]=='P';
    if (configureDriver()) {
      pinModeActive=pin; position=0; armed=true; lastActivity=millis();
      Serial.println(pin ? F("ARMED PIN: owner declares manual centre; +/-0.5 rev") : F("ARMED MOTOR: pin must be detached; provisional 20 full steps/rev"));
    }
    return;
  }
  float value;
  if (s[0]=='S' && s[1]==' ' && number(s+2,value) && value>=2 && value<=MAX_RPM) {
    rpm=value; Serial.println(F("Speed set")); return;
  }
  if (s[0]=='M' && s[1]==' ' && number(s+2,value)) { runStart=millis(); moveRevs(value); return; }
  if (s[0]=='C' && s[1]==' ' && number(s+2,value) && value>=1 && value<=20 && value==floorf(value)) {
    if (!armed || !pinModeActive || position!=0) { Serial.println(F("REJECT: cycles require PIN at declared centre")); return; }
    runStart=millis();
    for (uint8_t i=0;i<uint8_t(value);i++) {
      if (!moveRevs(.5f) || !waitUs(300000) || !moveRevs(-1.0f) ||
          !waitUs(300000) || !moveRevs(.5f) || !waitUs(300000)) return;
      Serial.print(F("CYCLE ")); Serial.println(i+1);
    }
    return;
  }
  Serial.println(F("REJECT: invalid command; ? for help"));
}

void setup() {
  digitalWrite(EN_PIN,HIGH); pinMode(EN_PIN,OUTPUT);
  pinMode(STEP_PIN,OUTPUT); pinMode(DIR_PIN,OUTPUT);
  Serial.begin(115200); uart.begin(19200);
  off();
  Serial.println(F("Microstepper screw test. Disabled. Set VREF before ARM. ? for help"));
}

void loop() {
  if (armed && millis()-lastActivity>IDLE_MS) {
    off(); Serial.println(F("Idle OFF after 30 s; manual centre invalid"));
  }
  while (Serial.available()) {
    char c=Serial.read();
    if (c=='!') { off(); used=0; overflow=false; Serial.println(F("STOP")); }
    else if (c=='\r') {}
    else if (c=='\n') {
      if (overflow) { off(); Serial.println(F("REJECT: overlong line; OFF")); }
      else if (used) { line[used]=0; command(line); }
      used=0; overflow=false;
    } else if (used<sizeof(line)-1 && !overflow) line[used++]=c;
    else overflow=true;
  }
}
