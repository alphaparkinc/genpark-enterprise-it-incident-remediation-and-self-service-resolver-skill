"""MCP server for Enterprise IT Incident Remediation & Self-Service Resolver."""
import sys
import json
from client import EnterpriseITIncidentResolver


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "triage_it_incident",
                    "description": "Triages enterprise IT helpdesk requests and auto-provisions access or licenses according to employee entitlements",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "request_text": {"type": "string"},
                            "employee_profile": {
                                "type": "object",
                                "description": "Profile containing department, role_level, and email",
                            },
                        },
                        "required": ["request_text", "employee_profile"],
                    },
                }
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "triage_it_incident":
            res = EnterpriseITIncidentResolver.triage_incident(
                args.get("request_text", ""),
                args.get("employee_profile", {}),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
