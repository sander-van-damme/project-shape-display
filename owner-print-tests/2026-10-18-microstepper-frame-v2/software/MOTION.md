# Bewegingsplanner

`main.py` bevat één planner per motor. `accel` en `decel` zijn positieve
RPM/s. De standaard updateperiode is 20 ms; de berekende remreserve neemt
ook 40 ms budget voor UART/configuratiecontrole mee (60 ms totale
reactiereserve). De losse planner-unit heeft een 2-ms-default; de firmware
stelt expliciet het ruimere budget in. VACTUAL verandert alleen wanneer de afgeronde
registerwaarde verandert. Bij 115200 baud kost een schrijftelegram van
8 bytes ongeveer 0,694 ms op de draad; diagnostische lezingen kosten extra.
De werkelijk haalbare updatefrequentie met meerdere kanalen moet fysiek
worden gecontroleerd. `max_update_gap_s` en `late_updates` maken vertraging
zichtbaar; de planner claimt geen harde realtimegarantie.

Bij een lange verplaatsing ontstaat een trapezium: versnellen, constante
snelheid, afremmen. Bij een korte verplaatsing raken de hellingen elkaar
zonder het gevraagde toerental te bereiken: een driehoek. Voor een
verplaatsing van `r` omwentelingen geldt zonder sampleafronding:
`r = (v_peak² / accel + v_peak² / decel) / 120`.
De planner begrenst snelheid op basis van de resterende berekende afstand
en `v²/(120*decel) + v*reactietijd/60`, met een reserve voor VACTUAL-afronding.
Dit is een eenvoudig online profiel, zonder vooraf opgeslagen stapentabel.

Elke werkelijk geschreven VACTUAL-waarde wordt naar berekende RPM
teruggerekend. Afstand is vervolgens exact de tijdintegraal van die
vastgehouden, gekwantiseerde waarde: `Δrev = RPM * Δt / 60`.
UART-schrijftijd telt mee bij de vorige snelheid. Een aangevraagde maar
mislukte snelheidswijziging telt niet als uitgevoerde beweging. De interne
versnellingshelling blijft ongekwantiseerd zodat ook kleine acceleraties
uiteindelijk de eerste VACTUAL-eenheid bereiken.

Er is geen 120-RPM-grens en geen arbitraire bovengrens voor afstand, duur
of cycli. Wel moeten invoer en eindpunt numeriek representabel zijn en
moet de aangevraagde snelheid een niet-nul signed 24-bit VACTUAL opleveren.
De minimale snelheidsstap hangt af van oscillator, motorstappen,
microstepping en de kalibratiefactor. Een eindpunt is slechts oplosbaar
tot circa één minimale snelheidsstap maal de updateperiode plus UART-marge.
`endpoint_resolution_rev` en `residual_rev` vermelden die grens en het
verschil met het doel expliciet. Een nog kleinere opdracht kan dus
eindigen zonder een niet-nul snelheid te schrijven. De laatste overgang
naar stilstand kan maximaal ongeveer één snelheidsquantum afwijken van
de ideale helling. Onvoorziene lange programmeerpauzes kunnen grotere
afwijkingen veroorzaken; daarvoor bestaat geen softwarepositiegarantie.

`duration_s` is de totale bewegingsduur inclusief versnellen en afremmen;
de afronding gebeurt op de updateperiode. Een cyclus is heen én terug;
`dwell_s` is de pauze op elk tussenliggend eindpunt. Alle cycli verwijzen
naar dezelfde twee berekende eindpunten, zodat de afrondingsrest niet
iedere cyclus als nieuw nulpunt wordt opgeteld. Er is geen mechanische
referentiemeting. Een richtingswisseling schrijft eerst nul en versnelt
pas daarna in de andere richting. Normale STOP remt af; noodstop vraagt
onmiddellijke uitschakeling aan de controller.

`rpm_requested` is ingesteld; `rpm_calculated`, afstand en positie zijn
berekend. Oscillatorafwijking, gemiste stappen, koppelslip en mechanische
speling blijven buiten die berekening. De handmatige kalibratiefactor
verbetert alleen de schaal; hij levert geen positieterugkoppeling of
bewijs van stapverliesvrije werking. Een fysieke pin krijgt uitsluitend
de expliciet ingestelde mechanische grenzen uit de hoofdcontroller.
Het prestatiedoel van circa 40 mm in minder dan één seconde blijft een
fysiek te onderzoeken doel.
