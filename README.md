# boksida-be

Vi har gjort en webbapplikation där man kan sortera och favoritmarkera böcker samt lägga till dem i en varukorg. (Det finns dock ingen funkionalitet för att köpa dem då det inte är en riktig butik.) Applikationen består av en backend i Flask och en frontend i React.

# Installation och start

- Ladda ner projekten med `git clone https://github.com/HenrikBellander/boksida-be` och `https://github.com/HenrikBellander/boksida-fe`
- Installera requirements.txt i backend med `pip install -r requirements.txt`
- Installerea package.json i frontend med `npm install`
- Kör run.py i backend med `python run.py`
- Starta React-projektet med `npm start dev`
- Gå in på http://localhost:5173 för att öppna applikationen

# Grafisk info

Designprincip ”mobile first".
Färgschema, font. (motivering)
 
# Branch-struktur

  - Main/master används för färdig produkt.
  - Dev används som huvudbranch i arbetet.
  - Features branchar ut från dev och mergas in när de är färdiga.

# PR-regler
Vi samarbetar vid pull requests då vi alla är nya på detta.

# Databasstruktur

Vi har fyra tabeller:
- Böcker
- Användare
- Favoritmarkeringar
- Varukorg
  Både varukorg och favoriter är kopplingstabeller mellan böcker och användare.

# Kända buggar

Inga i nuläget.
