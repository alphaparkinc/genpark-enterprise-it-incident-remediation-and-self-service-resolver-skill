"""Example usage for Enterprise IT Incident Remediation & Self-Service Resolver."""
from client import EnterpriseITIncidentResolver

if __name__ == "__main__":
    eng_employee = {"department": "engineering", "role_level": 2, "email": "alex@company.com"}
    res1 = EnterpriseITIncidentResolver.triage_incident("Need GitHub Copilot access for my new laptop", eng_employee)
    print("Copilot Request Status:", res1["status"])
    print("Action:", res1.get("action_taken", res1.get("reason")))

    mktg_employee = {"department": "marketing", "role_level": 1, "email": "sam@company.com"}
    res2 = EnterpriseITIncidentResolver.triage_incident("Need GitHub Copilot license", mktg_employee)
    print("\nMarketing Copilot Status:", res2["status"], "Reason:", res2.get("reason"))
