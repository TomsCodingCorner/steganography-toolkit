# TABS-steganografie

Een Python-demoproject dat tekst met de oorspronkelijke TABS-woordenboeken omzet
naar bits en die bits in de laagste bits van PNG-pixels verbergt. Een wachtwoord en
SHA-256 bepalen de pixelvolgorde. De oorspronkelijke Kivy-interface en de indeling
in `Final_Minimal_Product` zijn behouden.

## Installatie

Gebruik Python 3.13. Open PowerShell in de hoofdmap van dit project en voer uit:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

De dependencies zijn Pillow, Kivy en plyer. Er is geen losse buildstap nodig.
De GUI heeft een desktop met een werkende OpenGL-driver nodig.

## Demo: tekst verbergen en exact teruglezen

```powershell
.\.venv\Scripts\python.exe Final_Minimal_Product\STEGANOGRAPHY.py
```

Dit gebruikt de meegeleverde, synthetische afbeelding
`Final_Minimal_Product/Input_Directory/demo.png`, de tekst uit `demo_message.txt`
en het openbare voorbeeldwachtwoord `demo-password`.

Verwachte uitvoer:

```text
Teruggelezen bericht: This is a safe demo message.
Demo geslaagd: het teruggelezen bericht is exact gelijk aan de invoer.
Uitvoer: <projectmap>/Final_Minimal_Product/Output_Directory
```

De demo maakt automatisch de uitvoermap aan en schrijft:

- `tabs_innocentimage.png`: de afbeelding met het verborgen bericht.
- `tabs_desteg_output.txt`: exact `This is a safe demo message.`

Bij opnieuw uitvoeren worden deze demo-uitvoerbestanden overschreven. Alle modellen
en voorbeelddata zijn lokaal aanwezig; na installatie is geen netwerk nodig.

Hetzelfde scenario kan met de behouden GUI:

```powershell
.\.venv\Scripts\python.exe Final_Minimal_Product\GUI.py
```

1. Kies bij **Encrypt** met **Select Image** de meegeleverde `demo.png`.
2. Vul `This is a safe demo message.` en wachtwoord `demo-password` in. Klik **Hide**.
3. Ga naar **Decrypt**, kies de gemaakte `tabs_innocentimage.png`, vul hetzelfde
   wachtwoord in en klik **Uncover**.
4. Bekijk `Output_Directory/tabs_desteg_output.txt`; de tekst moet exact gelijk zijn.

De overige twee schermen gebruiken dezelfde TABS-code voor tekst naar bits en terug.
Resultaten worden in `Final_Minimal_Product/Output_Directory` geschreven.

## Bestanden en grenzen

- `GUI.py`: de vier werkende oorspronkelijke schermen.
- `STEGANOGRAPHY.py`: PNG-opslag en teruglezen; ook het automatische demo-startpunt.
- `TABS.py` en `Assisting_Files`: de oorspronkelijke encoding, bitverwerking,
  SHA-256-coördinaten en Pillow-toegang.
- `Model`: twee behouden originele woordenboeken, met het ontbrekende backtick-teken
  aangevuld. De encoder kiest automatisch een passend model.
- `Input_Directory`: kleine, neutrale voorbeelddata.
- `tests`: regressietests en een afzonderlijke GUI-smoketest.

De meegeleverde modellen ondersteunen afdrukbare ASCII-tekens en regelovergangen.
Niet-ondersteunde tekens, een leeg steganografiebericht, onvoldoende afbeeldingsruimte
of een verkeerd wachtwoord geven een foutmelding. Het wachtwoord bepaalt de
pixelvolgorde; er wordt geen cryptografische versleuteling toegepast.

De herstelde PNG-opslag bevat een herkenningscode en berichtlengte. Afbeeldingen van
de oude, onbetrouwbare demo zonder deze header worden niet ondersteund. Bewaar de
uitvoer als PNG zonder hercompressie of beeldbewerking.

Oude experimenten, dubbele modelmappen, tuningvarianten, ongebruikte helpers en het
onafgemaakte modelgeneratiescherm zijn verwijderd. IDE-instellingen, virtuele omgevingen,
caches en gegenereerde uitvoer worden door Git genegeerd. De bestaande licentie staat
in `LICENSE`; de cleanup is uitgevoerd op 12 oktober 2026.

## Verificatie

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tests\gui_smoke.py
.\.venv\Scripts\python.exe -m compileall -q Final_Minimal_Product tests
.\.venv\Scripts\python.exe -m pip check
```

Daadwerkelijk gecontroleerd op Windows met Python 3.13.7: dependency-installatie in
een nieuwe virtuele omgeving, de volledige PNG-demo (ook vanuit een schone bronkopie
zonder bestaande uitvoermap), tien regressietests en drie
GUI-tests met een verborgen Kivy-venster. De regressietests controleren beide modellen,
beide bitmodi, leestekens, regelovergangen, capaciteitscontrole, foutieve invoer,
het wachtwoord en teruglezen in een afzonderlijk proces vanuit een andere werkmap.
De GUI-tests activeren de echte knopkoppelingen; de bestandskiezer is daarbij gemockt.
Er is geen handmatige visuele GUI-controle, native bestandsdialoogtest, executable-build
of test op Linux/macOS uitgevoerd.
