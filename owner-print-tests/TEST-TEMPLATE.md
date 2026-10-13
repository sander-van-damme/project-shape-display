# Printtest — [korte titel]

> **CTO:** vul de voorbereiding, STL-bestanden, instructies en afkeurcriteria in. **Sander:** vul pas na een eventuele print de resultaten in. Een leeg resultatenvak betekent *nog niet getest*, niet *mislukt*.

**Status:** DRAFT / READY / DEFERRED / COMPLETED / RETIRED (kies één)  
**Prioriteit:** P1 / P2 / P3 / geen (alleen READY krijgt P1–P3)  
**Laatst beoordeeld:** [datum]  
**Reden voor huidige prioriteit/status:** [één zin]  
**Technische bron:** [link naar relevante GitHub-code/experiment/beslissing]

## 1. Waarom deze test? — CTO

**Concrete vraag:** [welke onzekerheid moet deze print oplossen?]  
**Waarom nu fysiek testen:** [waarom volstaat berekening/simulatie niet?]  
**Beslissing na de test:** [wat verandert er bij een goed of slecht resultaat?]  
**Afkeur-/stopconditie:** [welk observeerbaar resultaat maakt deze variant ongeschikt?]

## 2. Printklaar — CTO

| STL-bestand (exacte bestandsnaam, in deze map) | Wat is het? / aantal | Variante / herkenbaar label |
|---|---|---|
| `[voorbeeld-bestandsnaam].stl` | [functie en hoeveelheid] | [A/B/...] |

- **Printjobs:** [1 kleine plaat; alleen indien verantwoord 2 of 3]
- **Materiaal:** [bijv. PLA; geen onaangekondigde aankopen]
- **Printer/profiel:** [indien relevant; nozzle, laaghoogte, schaal 100%]
- **Oriëntatie en supports/brim:** [concreet]
- **Verwachte printtijd en materiaal:** [schatting of slicerwaarde, als zodanig gelabeld]
- **Extra benodigdheden:** [liefst geen; anders vooraf duidelijk vermelden]
- **STL-controle door CTO:** [datum; mm-afmetingen, mesh/printbaarheid en visuele verificatie]
- **Let op / veilig gebruik:** [bijv. geen scherpe randen, niet forceren]

**Voor Sander:** download de vermelde `.stl`-bestanden, open ze rechtstreeks in je slicer en print ze met bovenstaande instellingen. **Je hoeft geen OpenSCAD, Python of CAD-bestanden te compileren.** Dit is volledig vrijblijvend; er staat geen deadline op.

## 3. Test in enkele stappen — CTO

1. [eenvoudige handeling 1]
2. [eenvoudige handeling 2]
3. [eenvoudige handeling 3, met een duidelijk waarneembaar resultaat]

**Succes is:** [observeerbare voorwaarde]  
**Niet goed / stoppen is:** [observeerbare voorwaarde]  
**Niet getest/onduidelijk:** [wat moet als onbekend worden genoteerd]

## 4. Mijn resultaten — Sander

**Testdatum:** [invullen, of leeg laten]  
**Printer / filament / gebruikte slicerinstellingen (indien anders):** [invullen]  
**Print gelukt?** [ ] ja  [ ] deels  [ ] nee  [ ] nog niet geprint

| Variant / onderdeel | Past / beweegt / werkt? | Meting of schatting (eenheid) | Opmerkingen / probleem |
|---|---|---|---|
| [A] | [ ] ja [ ] deels [ ] nee [ ] niet getest | [waarde of n.v.t.] | [...] |
| [B indien van toepassing] | [ ] ja [ ] deels [ ] nee [ ] niet getest | [waarde of n.v.t.] | [...] |

**Handmatige test / belasting / aantal herhalingen (indien uitgevoerd):** [...]  
**Wat voelde of zag ik?** [...]  
**Foto/video of link (optioneel):** [...]  
**Wat zou ik volgende keer anders proberen? (optioneel):** [...]

## 5. Interpretatie en vervolg — CTO, pas na feedback

**Wat is werkelijk gemeten/geobserveerd, en wat blijft onbekend?** [nog open]  
**GO / NO-GO / vervolgactie:** [nog open]  
**Nieuwe prioriteit/status, datum en reden:** [nog open]

> Uitblijvende feedback is geen meetresultaat en geen blokkade. Bij achterhaald ontwerp: zet status op RETIRED, leg de reden vast en verwijder verouderde STL-bestanden.
