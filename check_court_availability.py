import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

def check_court_availability(date=None, mobile=None):
    """
    Check court availability for booking.
    
    Args:
        date: Date in YYYY-MM-DD format (defaults to today)
        mobile: Mobile number for booking (defaults to env variable)
    
    Returns:
        JSON response with availability data
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    if mobile is None:
        mobile = os.getenv('PLAYO_MOBILE')
    
    venue_id = os.getenv('PLAYO_VENUE_ID')
    sport_id = os.getenv('PLAYO_SPORT_ID')
    auth_token = os.getenv('PLAYO_AUTH_TOKEN')
    
    url = f"https://api.playo.io/booking-lab/availability/v1/{venue_id}/{sport_id}/{date}"
    
    headers = {
        "Host": "api.playo.io",
        "Authorization": auth_token,
        "Accept": "application/json",
        "Accept-Charset": "UTF-8",
        "User-Agent": "Ktor client",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    
    params = {
        "mobile": mobile
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def find_available_slots_8_9pm(days_to_check=30):
    """
    Find next 2 dates where courts are available from 8-9 PM (20:00-21:00).
    
    Args:
        days_to_check: Number of days to check from today
    
    Returns:
        List of available dates with court details
    """
    target_time = "20:00:00"
    available_dates = []
    current_date = datetime.now()
    
    for i in range(days_to_check):
        check_date = current_date + timedelta(days=i)
        date_str = check_date.strftime("%Y-%m-%d")
        day_name = check_date.strftime("%A")
        
        result = check_court_availability(date=date_str)
        
        if result and result.get('requestStatus') == 1:
            court_info = result.get('data', {}).get('courtInfo', [])
            available_courts = []
            
            for court in court_info:
                court_name = court.get('courtName')
                slots = court.get('slotInfo', [])
                
                for slot in slots:
                    if slot.get('time') == target_time and slot.get('status') == 1:
                        available_courts.append({
                            'court_name': court_name,
                            'price': slot.get('price')
                        })
                        break
            
            if available_courts:
                available_dates.append({
                    'date': date_str,
                    'day': day_name,
                    'courts': available_courts
                })
                
                if len(available_dates) == 2:
                    break
    
    return available_dates

if __name__ == "__main__":
    target_time = "20:00:00"
    
    for days_ahead in range(4):  # 0, 1, 2, 3 (today + 3 days)
        check_date = datetime.now() + timedelta(days=days_ahead)
        date_str = check_date.strftime("%Y-%m-%d")
        day_name = check_date.strftime("%A")
        
        result = check_court_availability(date=date_str)
        
        if result and result.get('requestStatus') == 1:
            court_info = result.get('data', {}).get('courtInfo', [])
            available_courts = []
            
            for court in court_info:
                court_name = court.get('courtName')
                slots = court.get('slotInfo', [])
                
                for slot in slots:
                    if slot.get('time') == target_time and slot.get('status') == 1:
                        available_courts.append(f"{court_name} - ₹{slot.get('price')}")
                        break
            
            if available_courts:
                print(f"{date_str} ({day_name}):")
                for court in available_courts:
                    print(f"  {court}")
            else:
                print(f"{date_str} ({day_name}): No courts available")
        
        print()
