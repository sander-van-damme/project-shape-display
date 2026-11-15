# Printtest — centrale motorbank met twee selecteerbare conussen

**Status:** READY voor de afgebakende printproeven; mechanische en elektrische werking nog niet fysiek bewezen.

**Prioriteit:** P1 `actuator.3mf` (zelfstandige passingen/krachtcoupon), P2 `mechanical.3mf` (bank).

**Laatst beoordeeld:** 15 november2026.

**Technische bron:** [DES-010](../../08-integrated-designs/DES-010-central-motor-selectable-cone-bank/DES-010-central-motor-selectable-cone-bank.md), expliciete eigenaarsopdracht; DES-009 blijft historische basis.

**Vraag:** kan één gemeenschappelijke aandrijving twee aangrenzende schroeven onafhankelijk bedienen, volledig loslaten en naar een volgende rij reizen? Daarnaast: kan een zelfgewikkelde, mechanisch vergrendelde selector de benodigde schakelarbeid leveren?

2×2 pinnen,5,08 pitch,4,50-mm pinnen (binnendraad behouden),3mm spoed,8mm proefslag. De handmatige bank is de geïntegreerde referentie; de elektrische3mm-liftcoupon is een **afzonderlijke onzekerheidsproef**, geen reeds werkende elektrische bank. Geen deadline of automatische vervolgopdracht.

## Bestanden en printvolgorde

| Project | Inhoud | Doel |
|---|---|---|
| [actuator.3mf](actuator.3mf) | 1base,1slider,2bobbin,1follower,1bridge; één4,50-pin,3nominale rotor/stiftparen; rotor2,2/2,4 en guide4,6/4,7/4,8 coupons | Kleine passingen en elektrische krachtproef; toleranties eerst handmatig controleren |
| [mechanical.3mf](mechanical.3mf) | Volledige2×2 referentie, bank/kap/motorplaat/railblokken/index, vier ondersteunde schroeven/vier pinnen, jacks/vorken, riemrotoren, poelie, frame/straps/spacers | Twee kanalen en twee rijen met handmatige selectie |

Geen eigen CAD-export nodig. `components/` bevat echte STL-componenten; print voor pin en koppelstift de `pin-supported.stl` / `male-supported.stl` varianten. De schone `pin.stl` en `male.stl` zijn montage-/CAD-referenties, niet de aangeboden printoriëntatie zonder stabilisatie; platen zijn ook als gecombineerde STL beschikbaar. `cad/` heeft parametrische OpenSCAD; `scripts/` reproduceert meshes, nominale bewegingscontrole en Bambu-projecten; `metadata/` bewaart profielen en controle-uitkomsten; `images/` verklaart mechanisme/bedrading. De 3MF is de printlevering, geen lege meshcontainer.

Printer: **Bambu Lab X1 Carbon,0,4mm nozzle,Generic PLA,Textured PEI**. Laag/eerste laag0,12/0,12; Arachne; twee wanden,0,45mm lijnbreedte/minimum75%; gyroid25%;5boven/5onder; automatische supports uitsluitend voor de bank, normal(auto), vanaf bouwplaat; geen raft; globale brim uit,3mm lokale brim voor pinnen/schroeven/stiften; print per laag. Contour/gat/elephant-footcompensatie0. Buitenwand15,binnen20,eerste laag15,brug15,infill40mm/s. Acceleratie1000, buiten/eerste laag500mm/s². Alleen stevige bank-/frameonderdelen hebben opgeslagen30/40/60mm/s buiten/binnen/infill. Temperatuur220°C eerste/overige lagen, PEI55°C, fan100% vanaf na eerste laag, laagvertraging8s/minimumsnelheid10mm/s. Koeling en temperaturen zijn opgeslagen in het Generic PLA-profiel; exacte waarden in metadata/*-settings.json, niet uit hoofd overtypen.

De motorplaat wordt los en vlak geprint. De bank heeft verwijderbare supports onder de jackpockets; pluk die via de open onderkant volledig weg vóór motor/jacks worden geplaatst. De schroeven hebben uitsluitend externe meegeprinte breeksteunen. Interne pinnenboringen blijven supportvrij. Geen onbewezen lange horizontale schroef. Slanke pinnen en koppelstiften staan rechtop met vier externe torens/diagonalen tegen hoogtewobble: pincontacten op8/17/26/35mm, stiftcontacten op6/10,2/14,4mm. Een brim alleen is hiervoor niet voldoende. Knip de twee-laags contactnekken los en maak de buitenvlakken zorgvuldig vlak; nooit aan torens draaien. Binnendraad blijft vrij. De schroeven behouden hun bestaande externe steunconstructie. bruggen in bank en coupon moeten fysiek nog goed blijken. De dunne0,38mm guidewand en rotorjournal vereisen beoordeling van de werkelijke print.

Slicerwaarden: **P1 5u07m12s/16,56g; P2 16u36m17s/65,78g**. Slicer-versie, heropening en werkelijke padcontrole: zie [verification.md](verification.md). Geen van die controles bewijst fysieke passing. Indien het eindrapport een blokkerende slicerbevinding bevat, blijft deze aanbieding DRAFT.

## Montage en veilig testen

Volg [assembly.md](assembly.md) voor de exacte standaardonderdelen, motor/rail/frameopbouw en beide indexposities; [actuator.md](actuator.md) voor winding/elektronica en aparte coupon. [Doorsnede](images/section.svg) en [actuatorschema](images/actuator.svg). Lees de benodigdheden vóór printen: motor, veren, railstangen en bevestiging zijn niet meegeprint. De motor hangt onder de bank; stevige≥45mm verhogingen zijn noodzakelijk.

1. Begin met de kleine key-/guidepassingen en nominale herhalingen. Monteer nooit een stroeve stift door hem met een motor los te draaien.
2. Verwijder alle externe supportrestjes, test vier schroef-pinparen met de hand. Monteer vaste lagers en guides. Iedere schroef blijft zonder bank axiaal gevangen. Test8mm heen/terug. Controleer hoogtebehoud met de bank weg.
3. Plaats bank, rotoren/kap en jacks. Meet de veerkracht met een schaal tegen compressie, start circa0,3N en verhoog alleen indien nodig tot maximaal circa1,2N. Deze waarden zijn proefinstellingen. Stel contramoeren zo af dat de vork beide koppen positief≥2,4mm neerhaalt; nominale tipruimte onder cup≈1,01mm vóór fouten/vervorming.
4. Motor uit, beide OFF: leg riem op en draai handmatig. Alle vaste schroeven blijven stil. Eerst daarna langzaam bekrachtigen met passende stroombegrenzing.
5. Alleen0 ON, alleen1 ON, beide ON, beide OFF; iedere combinatie CW/CCW. Noteer beweging van de andere pinnen. Stop direct bij bindende stiften, keeperlift, framebeweging of onverwachte beweging.
6. Beide ON langzaam laten draaien, één handjack gecontroleerd terugnemen; andere pin moet doorlopen. Eerste koppelproeven motor gestopt instellen. Geen vingers in de riem of als blokkering gebruiken.
7. Meet slip met lichte bekende kracht. Meegeleverde20mm-arm past op een losse male-stift: gebruik horizontale tangentiële krachtmeter of leid draad horizontaal over een aparte lage-frictie keerrol naar massa. **Recht omlaag aan een verticale as hangen levert geen zuiver torsiemoment.**1g tangentiële kracht op20mm≈0,196Nmm. Kalibreer fixturewrijving. Leg met een zacht vastgezet blok een gecontroleerde schroefblokkering aan; bewijs dat de conus slipt terwijl riem/stift blijven draaien. Als riem eerst slipt is conusslip onbekend. Geen schadelijk koppel zoeken.
8. Motor uit, volledig park, beide tipruimtes zichtbaar controleren; indexpin uit, bank5,08mm naar volgende rij, indexpin terug. Herhaal beide richtingen en inspecteer cupranden. Nooit reizen met een kop in een cup.
9. Actuatorcoupon eerst handmatig met0,3/0,5/1N followerlast. Meet piekschakelkracht en beide stroomloze standen. Dan afzonderlijke begrensde spoelpulsen≤0,5A/200ms,≥5s pauze, stoppen bij45°C of10°C stijging. Een mislukte elektrische overgang blijft een nuttige grensmeting, geen werkende selector.

**Succes:** onafhankelijke beweging beide richtingen, niet-geselecteerde schroeven stil binnen meetresolutie, beheersbare conusslip vóór schade, herhaald positief loskomen en tweede rij bereikbaar. Elektrisch succes vergt aantoonbaar volledige slag onder gemeten last en stroomloos behoud in beide standen. **Stop:** binding, scheuren, loskomende magneetkern/bedrading, oververhitting of verlies van vaste schroefondersteuning. Niet forceren of met meer stroom compenseren.

Vul [results.md](results.md) in met de werkelijk geprinte instellingen, gemeten krachten en waarnemingen. Nog niet geprint/getest betekent **onbekend**. Een geslaagde kleine proef kwalificeert geen80-kanaalbank of langdurige PLA-belasting.
