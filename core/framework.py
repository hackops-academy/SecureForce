"""Main framework engine"""

import logging
from datetime import datetime
from .exploit_manager import ExploitManager
from .payload_manager import PayloadManager
from .session_manager import SessionManager

class SecureForceFramework:
    """Main SecureForce Framework class"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.author = "SecureForce Team"
        self.started = datetime.now()
        
        # Initialize managers
        self.exploit_manager = ExploitManager()
        self.payload_manager = PayloadManager()
        self.session_manager = SessionManager()
        
        # Setup logging
        self.setup_logging()
        self.logger.info("SecureForce Framework initialized")
    
    def setup_logging(self):
        """Configure logging"""
        self.logger = logging.getLogger('SecureForce')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            # File handler
            fh = logging.FileHandler('secureforce.log')
            fh.setLevel(logging.INFO)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
    
    def get_status(self):
        """Get framework status"""
        return {
            'version': self.version,
            'uptime': str(datetime.now() - self.started),
            'exploits_loaded': len(self.exploit_manager.exploits),
            'payloads_available': len(self.payload_manager.generators),
            'active_sessions': len(self.session_manager.sessions)
        }