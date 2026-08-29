#!/usr/bin/env python3
"""
SecureForce - Penetration Testing Framework
Main entry point and interactive console
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from console.repl import SecureForceConsole

def main():
    console = SecureForceConsole()
    console.cmdloop()

if __name__ == "__main__":
    main()