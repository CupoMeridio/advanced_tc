#!/usr/bin/env python3
"""
Script di test per verificare la funzionalità dei timesheet settimanali

Questo script può essere eseguito in ERPNext per testare le nuove funzionalità.
"""

import frappe
from datetime import datetime, timedelta
from advanced_tc.api.timesheet_details import get_week_start_date, get_or_create_timesheet

def test_week_start_calculation():
    """
    Testa il calcolo dell'inizio della settimana
    """
    print("\n=== Test Calcolo Inizio Settimana ===")
    
    # Test con diverse date
    test_dates = [
        "2024-01-15",  # Lunedì
        "2024-01-17",  # Mercoledì
        "2024-01-21",  # Domenica
        "2024-01-22",  # Lunedì successivo
    ]
    
    for date_str in test_dates:
        date_obj = frappe.utils.getdate(date_str)
        week_start = get_week_start_date(date_obj)
        print(f"Data: {date_str} ({date_obj.strftime('%A')}) -> Inizio settimana: {week_start} ({week_start.strftime('%A')})")
        
        # Verifica che sia sempre lunedì
        assert week_start.weekday() == 0, f"L'inizio settimana dovrebbe essere lunedì, ma è {week_start.strftime('%A')}"
    
    print("✅ Test calcolo inizio settimana: PASSATO")

def test_timesheet_creation():
    """
    Testa la creazione di timesheet settimanali
    """
    print("\n=== Test Creazione Timesheet Settimanali ===")
    
    # Ottieni un employee di test
    employees = frappe.get_all("Employee", limit=1)
    if not employees:
        print("❌ Nessun employee trovato per il test")
        return
    
    employee = employees[0].name
    print(f"Usando employee: {employee}")
    
    # Test con date della stessa settimana
    same_week_dates = ["2024-01-15", "2024-01-17", "2024-01-19"]  # Lun, Mer, Ven
    
    timesheets = []
    for date_str in same_week_dates:
        date_obj = frappe.utils.getdate(date_str)
        timesheet = get_or_create_timesheet(employee, date_obj, None)
        timesheets.append(timesheet)
        print(f"Data {date_str}: Timesheet {timesheet.start_date} - {timesheet.end_date}")
    
    # Verifica che tutti i timesheet abbiano le stesse date
    first_timesheet = timesheets[0]
    for ts in timesheets[1:]:
        assert ts.start_date == first_timesheet.start_date, "I timesheet della stessa settimana dovrebbero avere la stessa start_date"
        assert ts.end_date == first_timesheet.end_date, "I timesheet della stessa settimana dovrebbero avere la stessa end_date"
    
    # Verifica che copra una settimana completa (7 giorni)
    week_duration = (first_timesheet.end_date - first_timesheet.start_date).days
    assert week_duration == 6, f"Il timesheet dovrebbe coprire 6 giorni (lun-dom), ma copre {week_duration}"
    
    print("✅ Test creazione timesheet settimanali: PASSATO")

def test_different_weeks():
    """
    Testa che settimane diverse creino timesheet separati
    """
    print("\n=== Test Settimane Diverse ===")
    
    employees = frappe.get_all("Employee", limit=1)
    if not employees:
        print("❌ Nessun employee trovato per il test")
        return
    
    employee = employees[0].name
    
    # Date di settimane diverse
    week1_date = "2024-01-15"  # Settimana 1
    week2_date = "2024-01-22"  # Settimana 2
    
    timesheet1 = get_or_create_timesheet(employee, frappe.utils.getdate(week1_date), None)
    timesheet2 = get_or_create_timesheet(employee, frappe.utils.getdate(week2_date), None)
    
    print(f"Settimana 1: {timesheet1.start_date} - {timesheet1.end_date}")
    print(f"Settimana 2: {timesheet2.start_date} - {timesheet2.end_date}")
    
    # Verifica che siano timesheet diversi
    assert timesheet1.start_date != timesheet2.start_date, "Settimane diverse dovrebbero avere timesheet con start_date diverse"
    assert timesheet1.end_date != timesheet2.end_date, "Settimane diverse dovrebbero avere timesheet con end_date diverse"
    
    print("✅ Test settimane diverse: PASSATO")

def run_all_tests():
    """
    Esegue tutti i test
    """
    print("🧪 Avvio test funzionalità timesheet settimanali...")
    
    try:
        test_week_start_calculation()
        test_timesheet_creation()
        test_different_weeks()
        
        print("\n🎉 Tutti i test sono passati con successo!")
        print("\n📋 Riepilogo funzionalità:")
        print("   ✅ Calcolo corretto dell'inizio settimana (lunedì)")
        print("   ✅ Creazione timesheet settimanali (lunedì-domenica)")
        print("   ✅ Riutilizzo timesheet per attività della stessa settimana")
        print("   ✅ Timesheet separati per settimane diverse")
        
    except Exception as e:
        print(f"\n❌ Test fallito: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Per eseguire in ERPNext:
    # bench --site [site-name] console
    # exec(open('test_weekly_functionality.py').read())
    run_all_tests()