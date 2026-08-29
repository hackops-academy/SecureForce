"""Console helper functions"""

from colorama import Fore, Style
from prettytable import PrettyTable

def format_exploit(exploit):
    """Format exploit for display"""
    return f"""{Fore.GREEN}{exploit.get('name', 'N/A')}{Style.RESET_ALL}
    Type: {exploit.get('type', 'N/A')}
    Platform: {exploit.get('platform', 'N/A')}
    Severity: {exploit.get('severity', 'N/A')}
    Description: {exploit.get('description', 'N/A')}
"""

def format_payload(payload):
    """Format payload for display"""
    return f"""{Fore.GREEN}{payload.get('payload_type', 'N/A')}{Style.RESET_ALL}
    Format: {payload.get('format', 'N/A')}
    Size: {payload.get('size', 'N/A')} bytes
"""

def create_table(headers, rows):
    """Create formatted table"""
    table = PrettyTable()
    table.field_names = headers
    table.align = "l"
    
    for row in rows:
        table.add_row(row)
    
    return table