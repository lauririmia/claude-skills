# Schema formularului „Creare rețetă" — Monsieur Cuisine (MC smart)

- Pagina: `https://www.monsieur-cuisine.com/ro/creare-reteta?devices=mc-smart`
- Aparat selectat: **MC smart**. Data creării se completează automat („Creat la data de").
- Formularul are 4 pași, afișați în meniul din stânga: **Detalii despre rețetă → Timp → Ingrediente → Etape**. Pe pașii 1–3 butonul de navigare este „Mai departe" (și „Înapoi" de la pasul 2). Pe ultimul pas (Etape) butoanele sunt „Înapoi" și „Previzualizare". Butonul „Salvare proiect" din antet este disponibil la toți pașii.
- Câmpurile marcate cu `*` sunt obligatorii.
- **Despre identificatori:** câmpurile au id-uri generate automat, de forma `input-258`. Ele se schimbă la reîncărcare sau la redeschiderea ferestrelor, deci nu sunt de încredere. Pentru a găsi un câmp, folosește **eticheta vizibilă sau placeholder-ul**, plus ordinea câmpurilor. Id-urile de mai jos sunt doar orientative (observate pe 24 Nov 2026).
- **Despre validare:** câmpurile numerice de timp/temperatură au limite care **nu sunt vizibile în atributele HTML** (`min`/`max` arată doar 0–99 și 0–59). Limitele reale apar ca **mesaj roșu (tooltip)** când valoarea e în afara intervalului, de exemplu „40℃ - 85℃". Toate limitele de mai jos au fost citite din aceste mesaje sau testate direct.

---

## Pasul 1 — Detalii despre rețetă

| Câmp (etichetă) | Tip | Reguli / valori | Id orientativ |
|---|---|---|---|
| **Numele rețetei*** | text pe un rând, placeholder „Dați rețetei un nume." | maximum 86 de caractere (contor „0 / 86") | `input-258` |
| **Scurtă descriere** | text pe mai multe rânduri, placeholder „Exemplu: „Această rețetă este perfectă pentru o seară cu prietenii.” sau „Clasicul reinventat pentru sezonul de Crăciun.”" | maximum 240 de caractere; opțional | `input-262` |
| **Dificultate*** | 3 butoane radio (alegere unică) | `ușor`, `mediu`, `dificil` | `input-269`, `input-274`, `input-279` (în această ordine) |
| **Dimensiunea porției*** | două controale: număr + drop-down | număr: minimum 0; drop-down (unitate), vezi lista de mai jos | număr `input-283`; drop-down `input-284` (doar citire, selecție din listă) |
| **Valoarea calorică** | număr întreg, unitate `kcal` | 0–99999; opțional | `input-288` |
| **Proteine** | număr întreg, unitate `g` | 0–99999; opțional | `input-289` |
| **Carbohidrați** | număr întreg, unitate `g` | 0–99999; opțional | `input-290` |
| **Grăsime** | număr întreg, unitate `g` | 0–99999; opțional | `input-291` |
| **Categorie*** | drop-down cu **selecție multiplă** (fiecare opțiune are casetă de bifat; opțiunile alese apar ca etichete cu „×"; placeholder „Selectați o categorie") | se pot alege una sau mai multe valori din lista de mai jos | `input-293` |
| **Imagine rețetă*** | încărcare de fișier („Răsfoiți și încărcați fișierul") | doar `image/jpeg`, `image/png`; minimum 1560 x 945 px; subiectul centrat | — |

Valorile nutriționale sunt „pe porție". Pe acest pas nu au apărut mesaje de validare pentru câmpurile numerice (testate cu 0, 1, 99999, 100000, -1).

**Valori „Dimensiunea porției" — unitatea (14):** `porție`, `porții`, `pahar`, `pahare`, `borcan`, `borcane`, `unitate`, `unități`, `bucată`, `bucăți`, `felie`, `felii`, `sticlă`, `sticle`.

**Valori „Categorie" (20):** `Food Processor`, `Storcător cu aburi`, `Vegan`, `Vegetarian`, `Sosur`, `Supe și tocănițe`, `Salate`, `Garnituri`, `Snack-uri`, `Feluri principale`, `Hrană pentru bebeluși`, `Băuturi`, `One-Pot / All-in-One`, `Deserturi`, `Coacere`, `Mic dejun`, `Cină`, `EASY+PURE`, `Aperitive`, `Marmeladă și jeleu`.

**Imaginea (necesită intervenție manuală):** deocamdată este un placeholder. Câmpul cere un fișier de pe disc; AI-ul care completează formularul trebuie să aibă acces la un fișier PNG/JPG de minimum 1560 x 945 px.

---

## Pasul 2 — Timp

Toate câmpurile sunt numerice, cu valoare implicită 0. Nu există drop-down-uri.

| Grup | Câmp | Tip | Limită reală (din validare) | Id orientativ |
|---|---|---|---|---|
| **Pregătire*** („Timpul de preparare necesar pentru ingrediente.") | oră | număr | durata totală: **1 Min – 99 ore** | `input-373` |
| | Min. | număr, pas 1 | 0–59 | `input-377` |
| **Gata în*** („Întregul timp de preparare (preparare și gătire).") | oră | număr | durata totală: **1 Min – 300 ore** | `input-386` |
| | Min. | număr, pas 1 | 0–59 | `input-390` |

- Nu există validare între cele două grupuri: pagina a permis „Pregătire" = 5 min cu „Gata în" = 1 min. Logic, „Gata în" ar trebui să fie ≥ „Pregătire"; AI-ul ar trebui să respecte asta.
- Durata nu poate fi 0 (minimum 1 minut în ambele grupuri).

---

## Pasul 3 — Ingrediente*

### Structură
- Ingredientele sunt grupate. Implicit există un singur grup, **„Ingrediente generale"**. Utilizatorul poate adăuga 0 sau mai multe grupuri noi, cu butonul **„Crearea unui grup nou"**. Orice grup nou arată la fel ca „Ingrediente generale".
- Pe antetul unui grup există iconițe: adăugare ingrediente (morcov cu plus), redenumire (creion) și ștergere.
- Într-un grup, rândurile de ingrediente se pot adăuga cu butonul „+" dintre rânduri sau cu „Adăugare ingrediente". Când completezi un rând, apare automat un rând nou gol dedesubt.
- Fiecare rând are un buton de ștergere (coș) și un buton de mutare (săgeți verticale).

### Câmpurile unui rând (în ordine)

| Câmp | Tip | Reguli |
|---|---|---|
| **Ingredient** (placeholder „Ingredient") | text cu sugestii (autocomplete) | vezi mai jos |
| **Cantitate** (placeholder „0") | câmp text liber (nu numeric) | acceptă orice text, fără filtrare și fără mesaj de validare: „0,5", „1/2", „1.5", „1 1/2" sau chiar „1,5 abc/" au fost păstrate. Recomandare pentru AI: folosește un număr simplu sau o fracție clară (ex. „200", „0,5", „1/2") |
| **Unitate** | drop-down, doar selecție | 13 valori + opțiune goală (vezi mai jos) |

### Câmpul „Ingredient" — cum funcționează
- Sugestiile vin de la un serviciu al site-ului (`/proxy-api`), pe măsură ce scrii. Se afișează **maximum 20** de rezultate, în ordine alfabetică.
- Căutarea este de tip „conține" și ține cont de diacritice. Exemplu: căutarea „fa" a returnat aquafaba, bile raffaello, bureți de fag, farfalle, fasole Borlotti, fasole azuki…; „faina" (fără diacritice) nu a returnat nimic.
- **Textul liber este acceptat.** Un ingredient care nu există în catalog (ex. „zzqx") rămâne în câmp după ce se iese din el.
- Catalogul complet nu poate fi extras dintr-o singură listă. Recomandare pentru AI: scrie numele ingredientului **cu diacritice**, așteaptă sugestiile și alege-o pe cea potrivită; dacă nu există, păstrează textul scris.

### Unitate (13 valori + goală)
`(gol)`, `g`, `linguriță`, `lingurițe`, `lingură`, `linguri`, `priză`, `prize`, `vârf de cuțit`, `vârfuri de cuțit`, `bucată`, `strat`, `straturi`.

---

## Pasul 4 — Etape*

- Pasul pornește gol, cu mesajul „Adăugați prima dumneavoastră etapă." și butonul **„Adăugare etapă"** (sus, dreapta). Se pot adăuga mai multe etape.
- „Adăugare etapă" deschide o **fereastră (dialog)** „Etapă N". Închiderea cu „Închidere" cere confirmare: „Sunteți sigur? Informațiile introduse nu vor fi salvate." (butoane „Părăsire" / „Înapoi").
- Butonul „Adăugare" din fereastră este dezactivat până se completează câmpurile obligatorii (Titlu și Instrucțiuni, sau câmpurile programului ales). **Nu există lungime minimă:** un titlu de 1 caracter și instrucțiuni de 1 caracter sunt acceptate. La Turbo, „Activați pentru" = 0 este acceptat.

### Lista de etape (după „Adăugare")
- Fiecare etapă apare ca un card numerotat (insignă cu numărul), cu **titlul** și **instrucțiunile** (sau detaliile programului). La hover apar trei iconițe: **ștergere** (coș), **editare** (creion), **mutare** (săgeți verticale, pentru reordonare).
- Între etape și sub ultima etapă există un buton **„+"** pentru inserarea unei etape noi în acel loc; butonul „Adăugare etapă" din antet adaugă la sfârșit.
- **Editare:** deschide aceeași fereastră, precompletată, cu butoanele „Închidere" și **„Salvare"** (în loc de „Adăugare") și un link **„Ștergere etapă"**.
- **Ștergere:** cere confirmare — „Ștergere etapă ? Chiar doriți să ștergeți această etapă?" cu butoanele „Ștergere" și „Revocare".
- Numărul etapei (ex. „Etapă 2") se calculează automat.

### Câmpurile ferestrei „Etapă N"

| Câmp | Tip | Reguli |
|---|---|---|
| **Titlu*** | text, placeholder „de exemplu, pregătirea cepei" | maximum 80 de caractere |
| **Adăugare program automat / Cântar / Turbo** („Această etapă necesită un program automat?") | comutator on/off | implicit oprit |
| **Instrucțiuni*** | text pe mai multe rânduri, placeholder „De exemplu, se curăță ceapa și se taie în inele subțiri." | maximum 240 de caractere; **apare doar când comutatorul e oprit**, sau pentru programele **Cântar** și **Turbo** (vezi mai jos) |
| **Selectare program automat** | drop-down, doar selecție; apare când comutatorul e pornit | 17 programe, cu câmpuri specifice fiecăruia (vezi mai jos); butonul coș din dreapta îl șterge |

### Panoul „Ingrediente" din fereastră
Afișează ingredientele din pasul 3, pe grupuri, cu cantitatea lângă ele (de exemplu „faina 200 g"), plus un contor (implicit 0). Grupurile se pot plia. **Ingredientele nu se asociază etapei** (confirmat de utilizator): panoul este doar un ajutor vizual, ca să poți scrie mai ușor titlul și instrucțiunile etapei. AI-ul poate folosi lista ca referință pentru text, dar nu trebuie să încerce să „adauge" ingrediente la etapă.

### Programele automate (17) — nume exacte din drop-down
`Aluat ferm`, `Aluat moale`, `Aluat lichid`, `Gătire la aburi`, `Prăjire`, `Cântar`, `Gătire manuală`, `Sous-vide`, `Slow Cook`, `Fierberea ouălor`, `Prespălare`, `Fermentare`, `Turbo`, `Fierberea orezului`, `Food Processor`, `Pasare`, `Smoothie`.

**Intervalele de durată nu depind de temperatură.** Testat la mai multe poziții ale cursorului: Gătire manuală (0, 1, 10, 20), Slow Cook (0, 6, 12), Fermentare (0, 3) și Prăjire (9, 10, 20) au avut același interval la toate pozițiile; la Sous-vide intervalul a fost același pentru toate temperaturile valide (40–85 °C).

**Convenție pentru câmpurile de timp:** acolo unde apar „Min." și „sec.", sunt două câmpuri numerice (Min. 0–99, sec. 0–59 în HTML), iar **durata totală trebuie să se încadreze în intervalul din coloana „Interval durată"**. Unde apar „oră" și „Min.", intervalul se aplică la durata totală (oră + minute).

| Program | Setare / câmpuri | Interval durată | Observații |
|---|---|---|---|
| **Aluat ferm** | **Setare\***: Min. + sec. | **45 sec – 4 Min** | Sfat: „Pentru prepararea pâinii sau a pastelor. Recomandăm o durată minimă de funcționare de 2 minute." |
| **Aluat moale** | **Setare\***: Min. + sec. | **45 sec – 4 Min** | Sfat: „Pentru aluat de drojdie, brioșe, chifle cu lapte și multe altele. Recomandăm o durată minimă de funcționare de 2 minute." |
| **Aluat lichid** | **Setare\***: Min. + sec. | **45 sec – 6 Min** | Sfat: „Pentru clătite și multe altele." |
| **Gătire la aburi** | **Setare\***: Min. + sec. | **0 sec – 60 Min** | fără sfat |
| **Prăjire** | **Setare\***: cursor de temperatură + Min. + sec. | **0 sec – 14 Min** | temperatura: vezi „Scala de temperatură"; fără sfat |
| **Cântar** | **Greutate\***: număr întreg în `g` (implicit 5) + **Instrucțiuni\*** (max. 240 de caractere) | — | Greutate valabilă: **5–5000 g** (sub 5 sau peste 5000 apare ca eroare); nu apare tooltip |
| **Gătire manuală** | cursor de temperatură + timp (Min. + sec.) + cursor de viteză + butoane de rotație | **1 sec – 99 Min** | vezi „Gătire manuală" mai jos |
| **Sous-vide** | **Setare\***: temperatură în `℃` (număr) + durată `oră` + `Min.` | **15 Min – 12 oră** | temperatură valabilă: **40℃ – 85℃** (valoare implicită 40) |
| **Slow Cook** | **Setare\***: cursor de temperatură (13 poziții) + durată `oră` + `Min.` | **15 Min – 8 oră** | temperatura: 37, 40, 45, 50 … 95 °C, din 5 în 5 (poziția 0 = 37, poziția 12 = 95; implicit afișat 95) |
| **Fierberea ouălor** | **Dimensiunea oului**: `MIC` / `MEDIU` / `MARE`; **Cum vi le doriți?**: `MOALE` / `SEMI-MOALE` / `TARE`; **Timp de gătire** afișat automat | — | durata se calculează din alegeri (tabel mai jos); implicit afișat „8 Min." |
| **Prespălare** | **Setare\***: `SCURT` / `LUNGĂ`; **Timp de curățare** afișat automat | — | `SCURT` = 1 Min. 30 sec.; `LUNGĂ` = 5 Min. |
| **Fermentare** | cursor de temperatură (7 poziții) + durată `oră` + `Min.` | **30 Min – 12 oră** | temperatura: 37, 40, 45, 50, 55, 60, 65 °C (poziția 0 = 37, poziția 6 = 65; implicit afișat 65) |
| **Turbo** | **Activați pentru\***: drop-down cu valori 0–20, unitate `sec.` + **Instrucțiuni\*** (max. 240 de caractere) | — | 21 de valori întregi: 0, 1, 2 … 20; dacă „0" e acceptat nu a fost verificat |
| **Fierberea orezului** | **Setare\***: Min. + sec. | **20 Min – 40 Min** | fără sfat |
| **Food Processor** | **Setare\***: Min. + sec. | **1 sec – 5 Min** | fără sfat |
| **Pasare** | **Setare\***: Min. + sec. | **30 sec – 2 Min** | fără sfat |
| **Smoothie** | **Setare\***: Min. + sec. | **30 sec – 2 Min** | fără sfat |

**Sfaturi:** doar cele trei programe de aluat (Aluat ferm, Aluat moale, Aluat lichid) afișează un „Sfat" (cu iconiță de informație). Celelalte 14 programe nu au sfat. Textele sunt reproduse exact în tabelul de mai sus.

### Fierberea ouălor — timpul de gătire pe combinații

| Dimensiune ou | MOALE | SEMI-MOALE | TARE |
|---|---|---|---|
| **MIC** | 8 Min. | 9 Min. | 15 Min. |
| **MEDIU** | 10 Min. | 12 Min. | 18 Min. |
| **MARE** | 11 Min. | 13 Min. | 18 Min. |

Valorile se calculează automat, nu se introduc.

### Scala de temperatură (cursoare)
Cursoarele de temperatură se mută doar cu mouse-ul sau cu tastele săgeți; valoarea **nu se poate tasta**.
- **Gătire manuală** și **Prăjire**: 21 de poziții (0–20): `0` (oprit), `37`, `40`, apoi din 5 în 5 până la `130` °C (40, 45, 50 … 125, 130).
- **Slow Cook**: 13 poziții (0–12): `37`, `40`, `45` … `95` °C.
- **Fermentare**: 7 poziții (0–6): `37`, `40`, `45`, `50`, `55`, `60`, `65` °C.
- **Sous-vide** nu folosește cursor, ci un câmp numeric de 40–85 °C.

### Detalii „Gătire manuală"
- **Temperatura**: vezi scala de mai sus.
- **Timp**: Min. 0–99, sec. 0–59; durata totală valabilă este **1 sec – 99 Min** (nu depinde de temperatură: același interval la pozițiile 0, 1, 10 și 20).
- **Viteza**: cursor cu valori întregi. Limita maximă depinde de temperatură și de sensul de rotație (testat pas cu pas, pornind de la o stare nouă a programului):
  - Rotație **în sens orar** (implicit) **și temperatură 0** (oprit): viteza maximă este **10** (cursor 0–10).
  - Rotație **în sens orar** și **orice temperatură peste 0** (de la 37 °C până la 130 °C): viteza maximă scade la **3** (cursor 0–3). Pragul este chiar trecerea de la 0 la 37 °C; nu există o valoare intermediară.
  - Rotație **în sens antiorar**: viteza maximă este **3**, indiferent de temperatură; la comutare, o viteză mai mare se reduce automat la 3.
  - Când temperatura revine la 0 (cu rotație orară), limita revine la 10.
  - Regula pentru AI: viteza 4–10 este permisă doar cu temperatură 0 și rotație orară; în toate celelalte cazuri alege viteza 0–3.
- **Rotație**: două butoane, `ROTAȚIE ÎN SENS ANTIORAR` și `ROTAȚIE ÎN SENS ORAR`; implicit este ales sensul orar.

---

## Previzualizare, salvare și trimitere

- Butonul **„Previzualizare"** (antet și la finalul pasului Etape) deschide o pagină de previzualizare a rețetei (aceeași adresă). Ea afișează: zona de imagine (încărcare fișier), numele („Dați rețetei un nume." dacă e gol), un șir de stele, **Pregătire** și **Gata în**, „Rețetă de la:", „Ultima actualizare pe:", Scurtă descriere, Etape (cu „Adăugare etapă"), Valori nutriționale (kcal, Proteine, Carbohidrați, Grăsime) și panoul Ingrediente.
- În antetul previzualizării sunt trei butoane: **„Editor"** (înapoi la formular), **„Salvare proiect"** și **„Completare rețetă"**.
- **„Salvare proiect"** (disponibil la toți pașii și în previzualizare) salvează rețeta ca proiect. **Singura condiție este numele rețetei:** fără nume apare mesajul „Rețeta necesită un nume înainte ca proiectul să poată fi salvat."; cu nume apare „Rețeta salvată". Celelalte câmpuri obligatorii nu sunt cerute pentru salvare.
- **„Completare rețetă"** este butonul final și rămâne **dezactivat** cât timp rețeta nu e completă. A rămas dezactivat cu numele, dificultatea, porția (2 porții), categoria, timpul, un ingredient și o etapă completate, dar fără imagine; s-a activat după încărcarea imaginii (fișier PNG/JPG). Deci **imaginea este ultima condiție obligatorie** pentru finalizare.

---

## Finalizarea rețetei: „Trimitere pentru revizuire" sau „Salvare ca privat"

Apăsarea butonului **„Completare rețetă"** (previzualizare, când e activ) deschide un dialog cu titlul **„Completare rețetă"** și textul „Acum puteți trimite rețeta dumneavoastră pentru revizuire. După aprobare, veți găsi rețeta dumneavoastră în prezentarea generală a rețetelor și pe aparat." Dialogul are două opțiuni, ca butoane radio (alegere unică), și un „×" pentru închidere:

| Opțiune | Descriere afișată | Efect |
|---|---|---|
| **Trimitere pentru revizuire** | „Trimiterea dumneavoastră va fi verificată acum." | Rețeta intră la revizuire (starea „Trimis"); după aprobare devine „Publicat" (publică). Textele din pagină indică și opțiunile „When to publish? Now / Schedule" și confirmări de originalitate a rețetei și imaginii, dar această opțiune **nu a fost deschisă**. După publicare, rețeta nu mai poate fi modificată (conform textelor din pagină). |
| **Salvare ca privat** | „Rețeta este salvată ca fiind privată pentru autor." | Rețeta primește starea **„Privat"** (vizibilă doar autorului). Poate fi modificată sau făcută publică oricând (conform textelor din pagină). |

**Pași pentru starea Privat (testat):**
1. În previzualizare, apasă **„Completare rețetă"**.
2. În dialog, alege **„Salvare ca privat"**. Apare butonul **„Confirmare și salvare"**.
3. Apasă **„Confirmare și salvare"**. Apare mesajul **„Rețeta privată salvată"**, iar „Ultima actualizare pe:" se completează cu data și ora.
4. Utilizatorul ajunge pe pagina rețetei (`/ro/previzualizare-reteta?recipe-id=<id>`), cu eticheta **„Privat"** (portocalie) lângă titlu, etichetele limbii (RO), aparatului (MC smart) și „Comunitate", și butonul **„Editare"** în dreapta sus.

**Stările unei rețete** (legenda „Starea rețetei" din „Rețetele mele"): `Proiect` (versiunea curentă, pentru prelucrare ulterioară), `Trimis` (în curs de revizuire de către profesioniștii lor), `Respins` (trimisă, necesită corecturi), `Publicat` (testată, aprobată, disponibilă tuturor), `Privat` (disponibilă numai autorului).

**„Rețetele mele"** (`/ro/retetele-mele`) afișează rețetele ca carduri, cu filtre pe stare (Toate, Proiect, Trimis, Respins, Publicat, Privat), căutare după nume și sortare (A-Z). Meniul „…" al unui card are doar **„Editare"** și **„Ștergere"**; starea nu se schimbă de acolo.

---

## Puncte rămase neconfirmate

1. Cum arată exact opțiunea „Trimitere pentru revizuire" după selectare (câmpurile „Când se publică", confirmările de originalitate) — nedeschisă, nu intră în scopul schemei pentru starea Privat.
2. Cum se trece o rețetă din „Privat" în „Publicat" ulterior.
