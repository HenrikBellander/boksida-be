# boksida-be
Vi har gjort en webbapplikation för en exklusivit bokklubb. Användarna kan som registrerade och inloggade se och välja olika kategorier av böcker. Inom en kategori kan man sedan favoritmarkera böcker samt lägga till dem i en varukorg. Varukorgen uppdateras i realtid när böcker läggs till och plockas bort - markeringar för favorit och varukorgsval följer med oavsett om man går in och ut i oloka kategorier. (Det finns dock ingen funkionalitet för att köpa böckerna i varukorgen.) Applikationen består av en backend i Flask (med databas SQLite) och en frontend i React.

# Installation och start
- Ladda ner projekten med `git clone https://github.com/HenrikBellander/boksida-be` och `https://github.com/HenrikBellander/boksida-fe`
- Installera requirements.txt i backend med `pip install -r requirements.txt`
- Installera package.json i frontend med `npm install`
- Kör run.py i backend med `python run.py`
- Starta React-projektet med `npm start dev`
- Gå in på http://localhost:5173 för att öppna applikationen

# Login-princip
Vår tanke var att man ska kunna logga in och sedan stanna inloggad medan man navigerar till olika sidor, att vissa sidor endast är tillgängliga om man är inloggad (books t ex), samt visa användarnamn i det inloggade läget. Vid inloggningen gör frontend en POST-förfrågan till backend genom /login, som verifierar användarnamn och lösenord mot databasen, och genererar ett JWT (token), som skickas som en HTTP-only cookie. För att stanna inloggad och nå protected routes skickar frontend en GET-förfrågan till backend genom /verify med en cookie för att bekräfta att token är giltig, som sedan skickar tillbaka användardatan till frontend (authApi -> AuthContext), och då får tillgång till användarnamnet som genom AuthButton-komponenten visas för användaren. ProtectedRoutes får svar från AuthContext om att det finns en användare, och ger då tillgång till sidan.

# Grafisk info
Designprincip ”mobile first". Vi försökte välja en font som är läsbar på mobil och skärm lätt för ung som gammal. Val av färger kan alltid diskuteras - viktigt att att ha en ren sida utan alltför många färger - och att tänka på kontrasteffekter till exempel fontfärg kontra bakgrund. Logiken valdes med en header där huvudfunktioner nås. Vi valde att inte presentera böckerna i ej inloggat läge - för att ge känsla av exklusivitet att vara med i denna nobla klubb. Förutom global css och css för header - krävde boksidan med dess funktioner en unik css, samt css för funktionerna för att markera favorit och markera val för varukorgen.
 
# Branch-struktur
  - Main/master används för färdig produkt.
  - Dev används som huvudbranch i arbetet.
  - Features branchar ut från dev och mergas in när de är färdiga.

# PR-regler
Vi var alla hyfsat osäkra på Git och GitHub. Ganska snart upptäckte vi att vi behövde koordinera. Vi valde att ha fasta möte då vi skulle uppdatera dev - merga, alltså göra pull request och gå igenom, vid behov välja/ta bort kod i våra filer tillsammans. Men sedan var alla fria att utveckla i egna branches med commits. Erfarenheten var att detta var svårare än vi trodde, det blev en del missförstånd som vi sedan fick ägna tid att hantera och parera. Dock blev vi bättre efterhand och lärde oss väldigt mycket av detta. Henrik var den som hade bäst koll på just denna biten, varför han oftast ledde arbetet, medans vi andra granskade på hans delade skärm. Insikten var att vid arbete med nya människor eller i en ny organisation, t ex LIA - är det klokt att tidigt prata med ansvarig chef, projektledare och/eller kollegor om vilka regler och rutiner som gäller, och om de är dokumenterade.

# Databasstruktur 
Vi har i SQLite-databasen books_data.db fyra tabeller:
- Böcker (books)
- Användare (users)
- Favoritmarkeringar (favorites)
- Varukorg (basket)

- Både basket och favorites är kopplingstabeller mellan books och users.
  ![ER-diagram](ER_books_data.png)

# Tester
Vi valde alla att köra Pytest och lyckades få igenom dessa. Vi valde att testa mot backend och inte end to end, detta var ett medvetet val, då det blev tajt med tid efter lektionen på tisdagen 2 dagar före slutpresentationen. Vi var därför mer bekväma i den lösningen.

# Kända buggar
Funktionen Basket/Varukorg: När man markerar ✅ nere till höger på en bok adderas boken koppat till user i kopplingstabellen basket i databasen, samtidigt uppdateras varukorgen i realtid i frontend. Man kan växla kategori, lägga till, ta bort på alla sätt - både databasen och frontens varukorg hänger med. Men när man tar bort SISTA boken från varukorgen, så uppdateras och töms databasen korrekt för usern, men på fronten ligger den enda boken kvar i varukorgen. Om man backar tilll kategoritabellen - och sedan går in i samma (eller annan) kategori igen - så är det rätt, varukorgen tom. Om detta fel har det tänkts mycket...
