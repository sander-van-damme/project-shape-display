# Afgekeurde kandidaat — geen printaanbod

Deze drie STL's bewaren uitsluitend de **afgekeurde tussengeometrie** vóór de vaste radiale rotorgeleiding en verkleinde tandkop. Ze horen niet in een 3MF-printplaat of montage. De actuele onderdelen staan in `../../cad/parts/`.

De onafhankelijke reviewer vond echte buurinterferentie bij 5,08-mm pitch, ondanks nul interferentie met de eigen as en meenemer. Bij tegengestelde rotorkanteling ±3° rond de flensmiddellijn z=0,36 en verplaatsing ±0,06 mm bedraagt de overlap 0,0185003 mm³. De onderste rotor staat geselecteerd; de as ligt op z=1,2−9,4 ten opzichte van de rotor. Dit is CAD-bewijs, geen fysieke observatie.

`python3 reproduce.py` herhaalt de booleaanse meshcontrole met numpy, trimesh en manifold3d. `result.json` bewaart de gevonden botsende gevallen en de SHA-256 van deze afgekeurde meshes. De nieuwe vaste framegeleiding blokkeert dezelfde stand voordat buren kunnen raken; zie `../independent-review-wobble.json` en `../../review.md`.
