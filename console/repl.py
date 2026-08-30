#!/usr/bin/env python3
\"\"\"console/repl.py

SecureForce Console - simple interactive CLI for SecureForce framework.
Drop exploit modules under the `exploits/` directory. Each exploit module can
export a top-level dict named `EXPLOIT` with keys:
  - name (str)
  - description (str)
  - options (dict)  # mapping option name -> dict(default=..., desc=...)
Optionally the module can provide a `run(options, payload)` function to actually execute.
\"\"\"

import cmd
import os
import sys
import shlex
import importlib.util
import traceback
import logging
from typing import Dict, Any, Optional, List

from colorama import init as colorama_init, Fore, Style
from prettytable import PrettyTable

colorama_init(autoreset=True)

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "console.log"),
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPLOITS_DIR = os.path.join(PROJECT_ROOT, "exploits")


def _log_and_print(msg: str, lvl="info"):
    getattr(logging, lvl)(msg)
    print(msg)


class ExploitStub:
    \"\"\"A minimal runtime representation of an exploit module.\"\"\"

    def __init__(self, key: str, meta: Dict[str, Any], module=None):
        self.key = key  # e.g., "windows/smb/eternal_blue"
        self.meta = meta
        self.module = module
        self.options = {}
        for k, v in meta.get("options", {}).items():
            # each option can be dict(default=..., desc=...)
            if isinstance(v, dict):
                self.options[k] = v.get("default")
            else:
                self.options[k] = v

    def show_options(self):
        tbl = PrettyTable()
        tbl.field_names = ["Option", "Value", "Description"]
        for opt, val in self.options.items():
            desc = ""
            optmeta = self.meta.get("options", {}).get(opt)
            if isinstance(optmeta, dict):
                desc = optmeta.get("desc", "")
            tbl.add_row([opt, str(val), desc])
        print(tbl)

    def run(self, payload=None):
        # If the module provided a run function, call it; otherwise fake it.
        if self.module and hasattr(self.module, "run"):
            try:
                return self.module.run(self.options.copy(), payload)
            except Exception as e:
                _log_and_print(f\"Exploit run failed: {e}\", "error")
                logging.debug(traceback.format_exc())
                return False
        else:
            _log_and_print(
                f\"[SIMULATION] Running exploit {self.key} with options {self.options}\",
                "info",
            )
            return True


class SecureForceConsole(cmd.Cmd):
    intro = Fore.GREEN + "Welcome to SecureForce console. Type help or ? to list commands." + Style.RESET_ALL
    prompt = Fore.CYAN + "SecureForce> " + Style.RESET_ALL

    def __init__(self):
        super().__init__()
        self.exploits: Dict[str, ExploitStub] = {}
        self.load_exploits()
        self.current_exploit: Optional[ExploitStub] = None
        self.sessions: List[Dict[str, Any]] = []
        self.last_payload = None

    # ----- filesystem / module loader -----
    def load_exploits(self):
        \"\"\"Discover and load exploit metadata from the exploits/ directory.

        Expected layout:
        exploits/<category>/<name>.py

        Each file may declare a top-level EXPLOIT dict.
        \"\"\"
        self.exploits.clear()
        if not os.path.isdir(EXPLOITS_DIR):
            _log_and_print(f\"No exploits directory found at {EXPLOITS_DIR}.\", \"warning\")
            return

        for root, _, files in os.walk(EXPLOITS_DIR):
            for fname in files:
                if not fname.endswith(".py"):
                    continue
                fpath = os.path.join(root, fname)
                rel = os.path.relpath(fpath, EXPLOITS_DIR)
                key = rel[:-3].replace(os.sep, "/")  # e.g., "windows/smb/eternal_blue"
                try:
                    spec = importlib.util.spec_from_file_location(f\"secureforce.exploits.{key}\", fpath)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)  # type: ignore
                    meta = getattr(module, "EXPLOIT", None)
                    if isinstance(meta, dict):
                        self.exploits[key] = ExploitStub(key, meta, module)
                        logging.debug(f\"Loaded exploit metadata: {key}\")
                    else:
                        # if no EXPLOIT provided, create a minimal entry
                        self.exploits[key] = ExploitStub(key, {"name": key, "description": "No metadata provided"}, module)
                except Exception:
                    logging.debug(f\"Failed to load exploit {key}:\\n\" + traceback.format_exc())
                    # don't crash the loader
                    self.exploits[key] = ExploitStub(key, {"name": key, "description": "Failed to load (see logs)"} , None)

    # ----- basic commands -----
    def do_show(self, arg):
        \"\"\"show exploits     - list available exploits
show options       - show options for selected exploit
show sessions      - list recorded sessions
\"\"\"
        args = shlex.split(arg)
        if len(args) == 0:
            print(\"Usage: show <exploits|options|sessions>\")
            return
        sub = args[0]
        if sub == "exploits":
            if not self.exploits:
                print(\"No exploits found. Put .py files under the exploits/ directory.\")
                return
            tbl = PrettyTable()
            tbl.field_names = ["Key", "Name", "Description"]
            for key, ex in sorted(self.exploits.items()):
                name = ex.meta.get("name", key)
                desc = ex.meta.get("description", "") or ""
                tbl.add_row([key, name, desc])
            print(tbl)
        elif sub == "options":
            if not self.current_exploit:
                print(\"No exploit selected. Use: use <exploit/key>\")
                return
            self.current_exploit.show_options()
        elif sub in ("sessions", "session"):
            tbl = PrettyTable()
            tbl.field_names = ["ID", "Exploit", "Target", "Result"]
            for i, s in enumerate(self.sessions, 1):
                tbl.add_row([i, s.get("exploit"), s.get("target"), s.get("result")])
            print(tbl)
        else:
            print(f\"Unknown show target: {sub}\")

    def complete_show(self, text, line, begidx, endidx):
        options = ["exploits", "options", "sessions"]
        return [o for o in options if o.startswith(text)]

    def do_use(self, arg):
        \"\"\"use <exploit/key>   - select an exploit to work with (e.g. use windows/smb/eternal_blue)\"\"\"
        key = arg.strip()
        if not key:
            print(\"Usage: use <exploit/key>\")
            return
        if key not in self.exploits:
            # offer close matches
            matches = [k for k in self.exploits.keys() if k.endswith(key) or key in k]
            if matches:
                print(\"No exact match. Did you mean:\")
                for m in matches:
                    print(\"  \", m)
            else:
                print(f\"Exploit '{key}' not found.\")
            return
        self.current_exploit = self.exploits[key]
        print(Fore.YELLOW + f\"Selected exploit: {key}\" + Style.RESET_ALL)
        desc = self.current_exploit.meta.get("description", "")
        if desc:
            print(desc)

    def complete_use(self, text, line, begidx, endidx):
        return [k for k in self.exploits.keys() if k.startswith(text)]

    def do_set(self, arg):
        \"\"\"set <option> <value>   - set an option for the selected exploit\"\"\"
        if not self.current_exploit:
            print(\"No exploit selected. Use: use <exploit/key>\")
            return
        try:
            parts = shlex.split(arg)
        except ValueError:
            print(\"Could not parse arguments. Use: set <option> <value>\")
            return
        if len(parts) < 2:
            print(\"Usage: set <option> <value>\")
            return
        opt = parts[0]
        val = \" \".join(parts[1:])
        if opt not in self.current_exploit.options:
            print(f\"Unknown option '{opt}'. Use 'show options' to list options.\")
            return
        # simple type inference: preserve as string; consumers can cast
        self.current_exploit.options[opt] = val
        print(f\"Set {opt} = {val}\")

    def do_generate(self, arg):
        \"\"\"generate payload    - placeholder payload generator

Usage:
  generate payload
\"\"\"
        args = shlex.split(arg)
        if len(args) == 0 or args[0] != "payload":
            print(\"Usage: generate payload\")
            return
        # simple placeholder payload creation
        payload = {
            "type": "reverse_shell",
            "format": "sh",
            "content": \"# reverse shell placeholder\\necho 'This is a simulated payload'\\n\",
        }
        self.last_payload = payload
        print(Fore.GREEN + \"Generated payload:\" + Style.RESET_ALL)
        print(f\"Type: {payload['type']}, Format: {payload['format']}\")
        print(payload["content"])

    def do_exploit(self, arg):
        \"\"\"exploit    - run the selected exploit (uses last generated payload if available)\"\"\"
        if not self.current_exploit:
            print(\"No exploit selected. Use: use <exploit/key>\")
            return
        # check for a 'target' option often used
        if "target" in self.current_exploit.options and not self.current_exploit.options["target"]:
            print(\"Warning: target option is not set for this exploit.\")
        print(Fore.MAGENTA + f\"Launching exploit {self.current_exploit.key}...\" + Style.RESET_ALL)
        success = False
        try:
            success = self.current_exploit.run(payload=self.last_payload)
        except Exception:
            logging.debug(traceback.format_exc())
            print(\"Exploit execution threw an error (see logs).\")
        result_text = \"success\" if success else \"failure\"
        # register a session
        session = {
            "exploit": self.current_exploit.key,
            "target": self.current_exploit.options.get("target"),
            "result": result_text,
        }
        self.sessions.append(session)
        print(Fore.YELLOW + f\"Exploit finished with result: {result_text}\" + Style.RESET_ALL)

    def do_sessions(self, arg):
        \"\"\"sessions - alias for show sessions\"\"\"
        self.do_show("sessions")

    # ----- housekeeping -----
    def do_reload(self, arg):
        \"\"\"reload - reload exploit modules from disk\"\"\"
        self.load_exploits()
        print(\"Exploit list reloaded.\")

    def do_exit(self, arg):
        \"\"\"exit - exit the console\"\"\"
        print(\"Goodbye.\")
        return True

    def do_EOF(self, arg):
        print()
        return self.do_exit(arg)

    def emptyline(self):
        # don't repeat last command on empty line
        pass

    def default(self, line):
        print(f\"Unknown command: {line}. Type help or ? to list commands.\")

    def do_help(self, arg):
        # use parent help but keep it friendly
        if not arg:
            print(\"Commands:\")
            print(\"  show exploits | options | sessions\")
            print(\"  use <exploit/key>\")
            print(\"  set <option> <value>\")
            print(\"  generate payload\")
            print(\"  exploit\")
            print(\"  reload\")
            print(\"  exit\\n\")
            print(\"Type help <command> for detailed help.\")
        else:
            return super().do_help(arg)

if __name__ == \"__main__\":  # simple local test runner
    c = SecureForceConsole()
    try:
        c.cmdloop()
    except KeyboardInterrupt:
        print(\"\\nExiting...\")
