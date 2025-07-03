# Test Timesheet Settimanali

Questo documento descrive come testare la nuova funzionalità dei timesheet settimanali.

## Modifiche Implementate

### Backend (Python)

1. **Nuova funzione `get_week_start_date()`**:
   - Calcola l'inizio della settimana (lunedì) per una data specifica
   - Gestisce correttamente il formato delle date

2. **Funzione `get_or_create_timesheet()` aggiornata**:
   - Ora cerca timesheet che coprono la settimana corrente
   - Crea timesheet settimanali (lunedì-domenica)
   - Migliore logica di ricerca per timesheet esistenti

3. **Funzione `create_timesheet_detail()` aggiornata**:
   - Calcola automaticamente l'inizio della settimana per l'attività
   - Utilizza il timesheet settimanale corretto

### Frontend (JavaScript)

1. **Nuova funzione `getWeekStartDate()`**:
   - Calcola l'inizio della settimana nel frontend
   - Compatibile con la logica del backend

2. **Ricerca timesheet aggiornata**:
   - Cerca timesheet per la settimana corrente quando si seleziona un employee
   - Fallback per timesheet che iniziano esattamente nella settimana

## Come Testare

### Test 1: Creazione Nuovo Timesheet Settimanale

1. Aprire il calendario timesheet
2. Selezionare una data (es. mercoledì)
3. Scegliere un employee
4. Verificare che:
   - Venga creato un timesheet che inizia il lunedì della settimana
   - Il timesheet termini la domenica della stessa settimana
   - L'attività sia associata al timesheet settimanale

### Test 2: Utilizzo Timesheet Esistente

1. Creare un'attività per lunedì
2. Creare un'altra attività per venerdì della stessa settimana
3. Verificare che:
   - Entrambe le attività utilizzino lo stesso timesheet
   - Il timesheet copra l'intera settimana (lunedì-domenica)

### Test 3: Settimane Diverse

1. Creare un'attività per una settimana
2. Creare un'attività per la settimana successiva
3. Verificare che:
   - Vengano creati due timesheet separati
   - Ogni timesheet copra la propria settimana

### Test 4: Selezione Employee

1. Aprire il dialog per aggiungere attività
2. Selezionare un employee
3. Verificare che:
   - Il campo timesheet si popoli automaticamente con il timesheet della settimana corrente
   - Se non esiste un timesheet per la settimana, il campo rimanga vuoto

## Comportamento Atteso

- **Timesheet settimanali**: Ogni timesheet copre dal lunedì alla domenica
- **Auto-creazione**: I timesheet vengono creati automaticamente quando necessario
- **Riutilizzo**: Le attività della stessa settimana utilizzano lo stesso timesheet
- **Ricerca intelligente**: Il sistema trova automaticamente il timesheet corretto per la settimana

## Note Tecniche

- La settimana inizia sempre di lunedì (ISO 8601)
- I timesheet vengono creati solo quando necessario (lazy creation)
- La ricerca dei timesheet esistenti è ottimizzata per performance
- Compatibilità mantenuta con il codice esistente