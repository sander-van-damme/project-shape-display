# Vierpins-demonstratie — drie alternatieve Bambu Studio-projecten

**Status:** DEFERRED · **Prioriteit:** geen · **Beoordeeld:** 2026-10-15. Eerst moet de [compacte passing](../2026-10-15-compact-screw-fit/test.md) fysiek soepel en reproduceerbaar blijken. Een volledig voorbereid 3MF-project heft deze voorwaarde niet op. Kies daarna hoogstens **één** alternatief.

| Open als Bambu Studio-**project** | Radiale CAD-relief | Totale Bambu-raming | Modelprinttijd | PLA |
|---|---:|---:|---:|---:|
| [**four-pin-demo-015-plate.3mf**](four-pin-demo-015-plate.3mf) | **0,15 mm** | **2 u 9 min 28 s** | 1 u 58 min 14 s | **9,23 g / 3,095 m** |
| [**four-pin-demo-0175-plate.3mf**](four-pin-demo-0175-plate.3mf) | **0,175 mm** | **2 u 9 min 16 s** | 1 u 58 min 2 s | **9,22 g / 3,093 m** |
| [**four-pin-demo-020-plate.3mf**](four-pin-demo-020-plate.3mf) | **0,20 mm** | **2 u 9 min 17 s** | 1 u 58 min 3 s | **9,22 g / 3,090 m** |

Iedere variant bevat één complete plaat met **12 afzonderlijk benoemde delen**: vier schroeven, vier gesloten pinnen, onderplaat, kooi, handkop en 3,3-mm neutraalmaatje. De variant wijzigt uitsluitend de binnendraad. Alle drie hebben **200 lagen**. Raming uit de werkelijk ingebedde G-code, met officiële X1C-start-/eindroutine, brim en 1,24 g/cm³ PLA; werkelijke tijd, kalibratie, purge en verbruik blijven onbekend. Print niet alle drie. Her-slicen behoudt alle instellingen, maar kan door meshprecisie en routing enkele seconden andere ramingen geven; de tabel citeert de daadwerkelijk opgeslagen bestanden.

| In alle drie projecten opgeslagen instelling | Exacte waarde |
|---|---|
| Slicer / printer | Bambu Studio **02.08.02.61**; **Bambu Lab X1 Carbon**, hardened-steel **0,4 mm**, Standard hotend |
| Filament / temperatuur | **Generic PLA 1,75 mm**, dichtheid **1,24 g/cm³**, flowratio **0,98**, max. **12 mm³/s**; nozzle **220 °C**, **Textured PEI Plate 55 °C**, ook eerste laag |
| Koeling | Partfan **100%**, eerste laag uit; auxfan **0%**; korte-laagvertraging aan, **8 s**, minimum **10 mm/s** |
| Lagen / wanden | **0,12 mm**, ook eerste laag; **Arachne**, **2 wanden**, nominale lijnbreedten **0,45 mm**; **100% rectilinear** infill; 5 boven-/onderlagen, bovenschaaldikte 0,6 mm |
| Arachne-details | Minimale wandbreedte **85%**, feature **25%**, overgangslengte **100%**, filtermarge **25%**, hoek **10°**, verdeling **1** |
| Snelheden | Buiten-/binnen-/kleine wanden, gap fill en normale infill/top **30 mm/s**; kleine-perimeterdrempel **20 mm**; eerste laag en bruggen **20 mm/s**; overhangstappen **30/20/10/10 mm/s**; travel **150 mm/s** |
| Acceleratie | Model/travel maximaal **1000 mm/s²**, eerste-laagextrusie **500 mm/s²**; officiële X1C-start-/eindbewegingen behouden eigen printerwaarden |
| Supports / brim | **Supports uit**, **uitsluitend buitenbrim 3 mm**, **0 mm brimafstand**; geen binnenbrim; skirt **0**, raft **0**, prime tower uit |
| Toleranties / plaatsing | XY-contour, XY-gat en elephant foot **0 mm**, circle compensation uit, krimp **100%**, schaal **100%**; per laag; bronoriëntatie behouden, complete plaat naar bedmidden verplaatst |
| Overig | Arc fitting uit; scarf seam uit; seam aligned; geen automatische oriëntatie of schaling |

**Oriëntatie:** schroeven op de kraag met hexopening onder; pinnen met open draadzijde onder; kooi op een volledige buitenwand; onderplaat vlak. Alle delen raken het bed. De schroeven zijn 21,5 mm hoog op een kleine 4,4-mm kraag; behoud de buitenbrim. Inspecteer en verwijder die later alleen aan de buitenkant, zonder in draad of hex te snijden.

**Werkelijke slicerpaden:** op alle varianten gecontroleerd, inclusief eerste laag/buitenbrim, 0,48-mm geleidewebben, binnendraad, hex-dak en gesloten pintop. Geen supportpaden en geen los laagcomponent zonder overlap met de vorige laag. Beide geleidewebben zijn aanwezig in alle 144 relevante laagchecks per variant. De ingestelde 3-mm buitenbrim is rond alle acht slanke delen aanwezig; de gereconstrueerde buitenrand reikt circa **2,55 mm** voorbij de CAD-rand door de discretisatie van brimlijnen. De openingen blijven vrij van binnenbrim.

**Resterende onzekerheid:** de kooi bevat bruggen. Grootste werkelijk vrije centerlijnoverspanning **8,985 mm**; sommige ankers liggen tot **2,823 mm** buiten materiaal van de vorige laag en steunen deels op dezelfde-laagperimeters. Lokale doorhang is dus een reëel fysiek risico, ook zonder nieuwe losse laagcomponent. De dunne onderste draadwand heeft lokale onderbrekingen. Controleer webben, daken, draad en hechting na afkoelen; forceer niets en plaats geen supports in draad of hex om dit te verbergen.

Bewijs per variant: [0,15 rapport](validation-015.json) / [paden](toolpaths-015.png), [0,175 rapport](validation-0175.json) / [paden](toolpaths-0175.png), [0,20 rapport](validation-020.json) / [paden](toolpaths-020.png); [heropening zonder externe profielen](roundtrip.json) en [herkomst](build-provenance.json). De aanvullende boring-/dak-/binnenbrimchecks staan bij [0,15](critical-detail-015.json), [0,175](critical-detail-0175.json) en [0,20](critical-detail-020.json). De [oorspronkelijke STLs en CAD](../four-pin-screw-demo/test.md) zijn ongewijzigd; de geometrie is onder een vaste XY-verplaatsing onafhankelijk vergeleken.

Volg na een fysieke passingbeslissing de bestaande [montage, handtest, stopcriteria en resultatenregistratie](../four-pin-screw-demo/test.md#3-montage-en-test--cto). Geen nieuw testresultaat of GO wordt geclaimd. De vierpins-proef blijft **DEFERRED** totdat de compacte passing fysiek bewezen is.

Controle gebeurde met Bambu Studio-CLI: daadwerkelijke slice, opnieuw openen en her-slicen zonder externe profielen, en onafhankelijke inspectie van alle paden plus visueel bekeken laagbeelden. Bambu-geometriepreviews zijn met software-rendering gegenereerd. Geen interactieve GUI-handcontrole, printerverbinding of fysieke print is uitgevoerd.

Voor onderhoud: [generator](../build-bambu-projects.py) gebruikt de officiële 02.08.02.61-resources en ongewijzigde STLs; [onafhankelijke padchecker](../validate-bambu-project.py) leest de ingebedde G-code en 3MF-transformaties. Versies en SHA-256-herkomst staan in `build-provenance.json`. Scratchuitvoer hoort in `work/`.
