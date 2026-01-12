import win32evtlog
import datetime

def count_program_runs(program_name):
    """Count how many times a specific program appears in event logs"""
    server = 'localhost'
    
    # Try different logs
    logs_to_check = ['Application', 'System', 'Security']
    
    total_count = 0
    program_lower = program_name.lower()
    
    for log_type in logs_to_check:
        try:
            hand = win32evtlog.OpenEventLog(server, log_type)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            year_start = datetime.datetime(2024, 1, 1)
            
            for event in events:
                if event.TimeGenerated > year_start:
                    # Check if program name is in event string
                    event_str = str(event.StringInserts or '')
                    if program_lower in event_str.lower():
                        total_count += 1
                        
            win32evtlog.CloseEventLog(hand)
        except:
            continue
    
    return total_count

# Ask user for specific program
program = input("\nEnter program name to search for (e.g., 'chrome.exe', 'python.exe'): ")
count = count_program_runs(program)
print(f"\n'{program}' found in event logs {count} times this year")