"""
PayloadForce CLI - Main interactive interface
Generate and manage payloads with ease
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from colorama import Fore, Style, init
from payloads.payload_generator import PayloadGenerator
from payloads.payload_listener import PayloadListener
import threading
import json

init(autoreset=True)

class PayloadForceCLI:
    """Interactive CLI for payload generation and management"""
    
    def __init__(self):
        self.generator = PayloadGenerator()
        self.listener = None
        self.generated_payloads = []
        self.show_banner()
    
    def show_banner(self):
        """Display the banner"""
        banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║           {Fore.MAGENTA}PayloadForce v1.0 - Payload Generator & Executor{Fore.CYAN}        ║
║                                                               ║
║    Professional payload generation and reverse shell handler ║
║            For Authorized Penetration Testing Only          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)
    
    def show_help(self):
        """Display help menu"""
        help_text = f"""
{Fore.GREEN}Available Commands:{Style.RESET_ALL}

{Fore.YELLOW}Payload Generation:{Style.RESET_ALL}
  list              - List all available payloads
  generate          - Generate a new payload (interactive)
  gen <type>        - Generate payload by type
  info <type>       - Get info about a payload type
  save <id> <file>  - Save payload to file

{Fore.YELLOW}Payload Management:{Style.RESET_ALL}
  payloads          - Show all generated payloads
  show <id>         - Show payload details
  delete <id>       - Delete a generated payload
  clear             - Clear all generated payloads

{Fore.YELLOW}Listener/Handler:{Style.RESET_ALL}
  listen            - Start reverse shell listener
  listen -p 5555    - Listen on specific port
  sessions          - List active sessions

{Fore.YELLOW}Utilities:{Style.RESET_ALL}
  help              - Show this help message
  clear-screen      - Clear terminal screen
  exit              - Exit the program

{Fore.CYAN}Examples:{Style.RESET_ALL}
  > generate
  > gen windows/shell/reverse_tcp
  > save 1 /tmp/payload.exe
  > listen
  > info web/php_shell
"""
        print(help_text)
    
    def list_payloads(self):
        """List all available payloads"""
        payloads = self.generator.list_payloads()
        
        print(f"\n{Fore.GREEN}Available Payloads ({len(payloads)} total):{Style.RESET_ALL}\n")
        
        categories = {}
        for p in payloads:
            cat = p.split('/')[0]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(p)
        
        for cat in sorted(categories.keys()):
            print(f"{Fore.CYAN}{cat.upper()}:{Style.RESET_ALL}")
            for p in sorted(categories[cat]):
                print(f"  • {Fore.YELLOW}{p}{Style.RESET_ALL}")
            print()
    
    def generate_interactive(self):
        """Interactive payload generation"""
        print(f"\n{Fore.GREEN}=== Payload Generator ==={Style.RESET_ALL}\n")
        
        # List categories
        payloads = self.generator.list_payloads()
        categories = {}
        for p in payloads:
            cat = p.split('/')[0]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(p)
        
        print(f"{Fore.YELLOW}Categories:{Style.RESET_ALL}")
        for i, cat in enumerate(sorted(categories.keys()), 1):
            print(f"  {i}. {cat}")
        
        try:
            cat_choice = int(input(f"\n{Fore.CYAN}Select category (number): {Style.RESET_ALL}")) - 1
            cat_name = sorted(categories.keys())[cat_choice]
            
            print(f"\n{Fore.YELLOW}Payloads in '{cat_name}':{Style.RESET_ALL}")
            for i, p in enumerate(categories[cat_name], 1):
                print(f"  {i}. {p}")
            
            payload_choice = int(input(f"\n{Fore.CYAN}Select payload (number): {Style.RESET_ALL}")) - 1
            payload_type = categories[cat_name][payload_choice]
            
            # Get LHOST and LPORT
            lhost = input(f"{Fore.CYAN}LHOST (your IP) [0.0.0.0]: {Style.RESET_ALL}") or "0.0.0.0"
            lport = input(f"{Fore.CYAN}LPORT (your port) [4444]: {Style.RESET_ALL}") or "4444"
            
            try:
                lport = int(lport)
            except ValueError:
                print(f"{Fore.RED}[-] Invalid port number")
                return
            
            print(f"\n{Fore.YELLOW}[*] Generating {payload_type}...{Style.RESET_ALL}")
            
            payload_data = self.generator.generate(payload_type, lhost, lport)
            
            payload_id = len(self.generated_payloads) + 1
            self.generated_payloads.append({
                'id': payload_id,
                'data': payload_data,
                'type': payload_type,
                'lhost': lhost,
                'lport': lport
            })
            
            print(f"{Fore.GREEN}[+] Payload generated (ID: {payload_id}){Style.RESET_ALL}")
            self._display_payload(payload_data)
            
        except (ValueError, IndexError):
            print(f"{Fore.RED}[-] Invalid selection")
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {e}")
    
    def generate_by_type(self, payload_type):
        """Generate payload by type"""
        if payload_type not in self.generator.list_payloads():
            print(f"{Fore.RED}[-] Unknown payload type: {payload_type}")
            return
        
        lhost = input(f"{Fore.CYAN}LHOST [0.0.0.0]: {Style.RESET_ALL}") or "0.0.0.0"
        lport = input(f"{Fore.CYAN}LPORT [4444]: {Style.RESET_ALL}") or "4444"
        
        try:
            lport = int(lport)
        except ValueError:
            print(f"{Fore.RED}[-] Invalid port")
            return
        
        try:
            payload_data = self.generator.generate(payload_type, lhost, lport)
            
            payload_id = len(self.generated_payloads) + 1
            self.generated_payloads.append({
                'id': payload_id,
                'data': payload_data,
                'type': payload_type,
                'lhost': lhost,
                'lport': lport
            })
            
            print(f"\n{Fore.GREEN}[+] Payload generated (ID: {payload_id}){Style.RESET_ALL}")
            self._display_payload(payload_data)
        
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {e}")
    
    def _display_payload(self, payload_data):
        """Display generated payload"""
        print(f"\n{Fore.CYAN}Payload Details:{Style.RESET_ALL}")
        
        for key, value in payload_data.items():
            if key == 'payload':
                print(f"  {Fore.YELLOW}{key}:{Style.RESET_ALL}")
                if isinstance(value, str) and len(value) > 200:
                    print(f"    {value[:200]}...\n")
                else:
                    print(f"    {value}\n")
            elif key == 'payloads':
                print(f"  {Fore.YELLOW}{key}:{Style.RESET_ALL}")
                for i, p in enumerate(value, 1):
                    print(f"    {i}. {p}")
            elif key != 'shellcode':
                print(f"  {Fore.YELLOW}{key}:{Style.RESET_ALL} {value}")
    
    def show_payload(self, payload_id):
        """Show details of a specific payload"""
        try:
            payload_id = int(payload_id)
            payload = next((p for p in self.generated_payloads if p['id'] == payload_id), None)
            
            if not payload:
                print(f"{Fore.RED}[-] Payload {payload_id} not found")
                return
            
            print(f"\n{Fore.GREEN}=== Payload {payload_id} ==={Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Type:{Style.RESET_ALL} {payload['type']}")
            print(f"{Fore.YELLOW}LHOST:{Style.RESET_ALL} {payload['lhost']}")
            print(f"{Fore.YELLOW}LPORT:{Style.RESET_ALL} {payload['lport']}\n")
            
            self._display_payload(payload['data'])
        
        except ValueError:
            print(f"{Fore.RED}[-] Invalid payload ID")
    
    def list_generated_payloads(self):
        """List all generated payloads"""
        if not self.generated_payloads:
            print(f"{Fore.YELLOW}[*] No payloads generated yet")
            return
        
        print(f"\n{Fore.GREEN}Generated Payloads:{Style.RESET_ALL}\n")
        print(f"{'ID':<5} {'Type':<40} {'LHOST':<15} {'LPORT':<6}")
        print("-" * 70)
        
        for p in self.generated_payloads:
            print(f"{p['id']:<5} {p['type']:<40} {p['lhost']:<15} {p['lport']:<6}")
        print()
    
    def save_payload(self, payload_id, filename):
        """Save payload to file"""
        try:
            payload_id = int(payload_id)
            payload = next((p for p in self.generated_payloads if p['id'] == payload_id), None)
            
            if not payload:
                print(f"{Fore.RED}[-] Payload {payload_id} not found")
                return
            
            payload_data = payload['data']
            
            # Determine what to save
            if 'payload' in payload_data:
                content = payload_data['payload']
            elif 'payloads' in payload_data:
                content = '\n'.join(payload_data['payloads'])
            else:
                content = json.dumps(payload_data, indent=2)
            
            # Write to file
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            with open(filename, 'w') as f:
                f.write(content)
            
            print(f"{Fore.GREEN}[+] Payload saved to {filename}")
        
        except ValueError:
            print(f"{Fore.RED}[-] Invalid payload ID")
        except Exception as e:
            print(f"{Fore.RED}[-] Error saving payload: {e}")
    
    def start_listener(self, lport=4444):
        """Start the payload listener"""
        try:
            lport = int(lport)
        except ValueError:
            print(f"{Fore.RED}[-] Invalid port")
            return
        
        self.listener = PayloadListener('0.0.0.0', lport)
        self.listener.run_interactive()
    
    def run(self):
        """Main interactive loop"""
        self.show_help()
        
        try:
            while True:
                try:
                    command = input(f"\n{Fore.CYAN}payloadforce> {Style.RESET_ALL}").strip()
                    
                    if not command:
                        continue
                    
                    parts = command.split()
                    cmd = parts[0].lower()
                    
                    if cmd == 'help':
                        self.show_help()
                    
                    elif cmd == 'list':
                        self.list_payloads()
                    
                    elif cmd == 'generate':
                        self.generate_interactive()
                    
                    elif cmd == 'gen' and len(parts) > 1:
                        self.generate_by_type(parts[1])
                    
                    elif cmd == 'info' and len(parts) > 1:
                        payload_type = parts[1]
                        if payload_type in self.generator.list_payloads():
                            print(f"{Fore.GREEN}[+] {payload_type} is available")
                        else:
                            print(f"{Fore.RED}[-] Unknown payload type")
                    
                    elif cmd == 'show' and len(parts) > 1:
                        self.show_payload(parts[1])
                    
                    elif cmd == 'payloads':
                        self.list_generated_payloads()
                    
                    elif cmd == 'save' and len(parts) > 2:
                        self.save_payload(parts[1], parts[2])
                    
                    elif cmd == 'delete' and len(parts) > 1:
                        try:
                            pid = int(parts[1])
                            self.generated_payloads = [p for p in self.generated_payloads if p['id'] != pid]
                            print(f"{Fore.GREEN}[+] Payload {pid} deleted")
                        except ValueError:
                            print(f"{Fore.RED}[-] Invalid payload ID")
                    
                    elif cmd == 'clear':
                        self.generated_payloads = []
                        print(f"{Fore.GREEN}[+] All payloads cleared")
                    
                    elif cmd == 'listen':
                        lport = parts[2] if len(parts) > 2 and parts[1] == '-p' else '4444'
                        self.start_listener(lport)
                    
                    elif cmd == 'sessions':
                        if self.listener:
                            self.listener.list_sessions()
                        else:
                            print(f"{Fore.YELLOW}[*] Listener not running")
                    
                    elif cmd == 'clear-screen':
                        os.system('clear' if os.name != 'nt' else 'cls')
                    
                    elif cmd == 'exit':
                        print(f"{Fore.YELLOW}[*] Exiting...")
                        break
                    
                    else:
                        print(f"{Fore.RED}[-] Unknown command. Type 'help' for available commands")
                
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}[*] Exiting...")
                    break
                except Exception as e:
                    print(f"{Fore.RED}[-] Error: {e}")
        
        finally:
            if self.listener:
                self.listener.stop()

if __name__ == '__main__':
    cli = PayloadForceCLI()
    cli.run()
