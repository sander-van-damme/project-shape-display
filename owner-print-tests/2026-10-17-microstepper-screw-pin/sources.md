# Motoridentiteit en ontwerpkeuze

Bronnen gelezen op 17 oktober 2026; geen gemeten motorkoppel of fysieke printclaim.

De eigenaar bevestigde in deze opdracht **Ø8 × 8,2 mm**. De oorspronkelijke
[maatfoto](motor-dimensions-original.jpg) komt exact uit commit
`41484f96999847c139b9010e73009d73e9459c89`,
`trial-0-pneumatic-multiplexer/docs/img/stepper-motor-dimensions.jpg`.
Deze toont Ø8 mm, huislengte 8,2 mm, 4 mm uitsteking boven het huis,
een tandwieltje Ø2,2 mm met 9 tanden/module 0,2 en twee frontgaten op 6 mm.
De frontgaten zijn niet nodig voor deze klem. Tandhoogte, terminaluitsteeksel en
asdiameter zijn niet volledig bemaat. De niet bemate frontflens krijgt Ø11,5-mm
vrijloop over de bovenste 1 mm van de zitting; de Ø8-mm cilinder wordt geklemd.
De eigenaar heeft het tandwieltje nog niet
expliciet bevestigd; controleer het vóór montage. Er wordt geen tandwiel verwijderd.

`components.md` uit dezelfde commit vermeldt 40 Ω, 5–6 V, ongeveer 0,12 A,
bipolair/twee fasen/vier draden en een **1,5-mm as**. De tweede draadkleurregel
noemt B− dubbel en is intern tegenstrijdig. Gebruik een ohmmeter voor de paren.
Historische verkooplink: <https://nl.aliexpress.com/item/4000806393169.html>.
De verkooptekst is geen gekalibreerde datasheet.

**De PDF is geen passende maatbron voor dit huis.**
`trial-0-pneumatic-multiplexer/docs/micro-stepper-datasheet.pdf` uit die commit
heet PM08-2/PM08-02 en vermeldt **8 × 9,2 mm, Ø0,8-mm as, 3,3 V**,
40 Ω ±7%, 18°/20 hele stappen per omwenteling. Zijn koppelgetal van
5 gf·cm en frequentieclaims worden daarom **niet** aan de bevestigde
8,2-mm motor toegekend. Ook 20 hele stappen/omw is voorlopig: tel op de
losse motor echt één omwenteling voordat de pin wordt aangesloten.
PDF SHA-256: `ac7a13e9ae7482a40ba0451f8e230c6630cde942ca5c27ab1a77fbedfc3fe132`.
Maatfoto SHA-256: `91b1daabccbcece63d11bcb0b190c2f7bcf23977b242e339027d56f075e935bd`.

## TMC2208

Primaire bron: Analog Devices/Trinamic,
[TMC2202/TMC2208/TMC2224 datasheet rev. 1.13, 25 mei 2022](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2202_TMC2208_TMC2224_datasheet_rev1.13.pdf),
§6.3.1, §9 en §9.1. VM 4,75–36 V; VIO 3,3/5 V. Een geregelde 6-V-bron
met seriediode houdt VM boven de ondergrens. Controleer de spanning op VM.
De kleine fasebelasting ligt ruim onder het vermogensmaximum van de chip.

Een gebruikelijke R110-module zou in standalone een onhandig lage Vref nodig
hebben. De fabrikant raadt Vref beneden ongeveer 0,5–1 V af wegens relatieve
ruis. Daarom **UART, SpreadCycle, VSENSE=1, IRUN=IHOLD=5**, Vref aanvankelijk
0,80 V; geen wijziging van de shuntweerstanden en geen StealthChop-autotuning.
De lage digitale stroomfactor vermindert microstapnauwkeurigheid; dat is voor
deze op/neer-proef aanvaardbaar en is geen bewezen nauwkeurige positionering.

De theoretische fasepiek is
`Ipk = (IRUN+1)/32 × 0,180/(Rsense+0,030) × Vref/2,5`.
Bij R110 en 0,80 V: **77 mA piek / 55 mA RMS**. Bij 1,00 V:
96 mA piek / 68 mA RMS; bij 1,20 V: 116 mA piek / 82 mA RMS.
Dit zijn berekeningen met nominale componenten, geen stroommetingen.
De 0,12-A-historische opgave wordt conservatief als **piekplafond** gebruikt.
Nooit een standaard NEMA17-Vref overnemen.

De historische tekst noemt “MC2208 V1.2”; dat legt geen ondubbelzinnig
PCB-pinout vast. De geleverde aansluiting vereist een echte **TMC2208**
StepStick met twee **R110** externe shunts, bereikbaar **PDN_UART** en
Vref-meetpunt/trimmer. Bij een clone kan een UART-soldeerbrug nodig zijn;
raadpleeg juist dat PCB-schema. Een TMC2209 heeft een andere chip-ID en wordt
door deze firmware geweigerd. Verbind uitsluitend de gelabelde aansluitingen.

Softwarebron: [TMCStepper 0.7.3](https://github.com/teemuatlut/TMCStepper/tree/v0.7.3).
Printbron: [E-295](../../06-experiments/E-295-compact-screw-drive-development.md)
en de [bestaande compacte passing](../2026-10-15-compact-screw-fit/test.md).
De drie soepel bevonden nominale exemplaren zijn eigenaarobservaties uit de
opdracht; nieuw motorkoppel, nieuwe printpassing en belastbaarheid blijven open.
