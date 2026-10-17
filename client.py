"""Enterprise IT Incident Remediation and Self-Service Resolver.
100% Python Standard Library.
"""

from typing import List, Dict, Any, Optional
import re


class EnterpriseITIncidentResolver:
    """Triage enterprise IT service desk incidents, automates entitlement validation,
    and executes self-service remediation for common identity, software, and hardware requests."""

    AUTOMATED_SERVICES = {
        "vpn_access": {
            "required_role_level": 2,
            "auto_provisionable": True,
            "entitlement_group": "sec-vpn-global",
        },
        "github_copilot": {
            "required_role_level": 2,
            "eligible_departments": ["engineering", "product", "data"],
            "auto_provisionable": True,
        },
        "zoom_large_meeting_license": {
            "required_role_level": 3,
            "eligible_departments": ["marketing", "sales", "executive"],
            "auto_provisionable": True,
        },
    }

    @classmethod
    def triage_incident(cls, request_text: str, employee_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzes an IT helpdesk request and determines whether it can be autonomously fulfilled."""
        text_lower = request_text.lower()
        dept = str(employee_profile.get("department", "")).lower()
        role_level = int(employee_profile.get("role_level", 1))

        # Request 1: VPN Access
        if any(w in text_lower for w in ["vpn", "remote access", "vpn profile"]):
            spec = cls.AUTOMATED_SERVICES["vpn_access"]
            if role_level >= spec["required_role_level"]:
                return {
                    "request_type": "vpn_provisioning",
                    "status": "AUTONOMOUSLY_FULFILLED",
                    "action_taken": "Assigned employee to 'sec-vpn-global' directory group and generated configuration profile.",
                    "instructions": "Your VPN credentials have been provisioned. Download the client profile from the internal portal.",
                }

        # Request 2: GitHub Copilot License
        if any(w in text_lower for w in ["copilot", "github copilot", "ai code assistant"]):
            spec = cls.AUTOMATED_SERVICES["github_copilot"]
            if dept in spec["eligible_departments"] and role_level >= spec["required_role_level"]:
                return {
                    "request_type": "copilot_license_assignment",
                    "status": "AUTONOMOUSLY_FULFILLED",
                    "action_taken": "Assigned seat in GitHub Enterprise Organization under Developer Productivity pool.",
                    "instructions": "License granted. Restart your IDE to activate GitHub Copilot with SSO.",
                }
            return {
                "request_type": "copilot_license_assignment",
                "status": "ROUTED_FOR_MANAGER_APPROVAL",
                "reason": f"Department '{dept}' or role level '{role_level}' requires manual budget approval.",
            }

        # Request 3: Password / MFA reset
        if any(w in text_lower for w in ["password reset", "forgot password", "mfa reset"]):
            return {
                "request_type": "identity_self_service",
                "status": "AUTONOMOUSLY_FULFILLED",
                "action_taken": "Generated time-bound cryptographic identity verification link to registered backup SMS/email.",
                "instructions": "Click the verification link sent to your backup device within 15 minutes to reset your MFA token.",
            }

        # Default fallback to human ServiceDesk queue
        return {
            "request_type": "general_it_ticket",
            "status": "ESCALATED_TO_TIER2_HELPDESK",
            "reason": "Request requires manual hardware provisioning or administrative review.",
        }
