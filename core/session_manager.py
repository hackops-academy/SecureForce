"""Manage active sessions and shells"""

import uuid
from datetime import datetime

class SessionManager:
    """Manages active exploitation sessions"""
    
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, session_type, target, payload_info):
        """Create new session"""
        session_id = str(uuid.uuid4())[:8]
        
        session = {
            'id': session_id,
            'type': session_type,
            'target': target,
            'payload': payload_info,
            'created': datetime.now(),
            'commands': [],
            'active': True
        }
        
        self.sessions[session_id] = session
        return session_id
    
    def get_session(self, session_id):
        """Get session details"""
        return self.sessions.get(session_id)
    
    def list_sessions(self):
        """List all sessions"""
        return self.sessions
    
    def add_command(self, session_id, command, output):
        """Add command to session history"""
        if session_id in self.sessions:
            self.sessions[session_id]['commands'].append({
                'command': command,
                'output': output,
                'timestamp': datetime.now()
            })
    
    def close_session(self, session_id):
        """Close session"""
        if session_id in self.sessions:
            self.sessions[session_id]['active'] = False