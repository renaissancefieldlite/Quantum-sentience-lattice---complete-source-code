from __future__ import annotations


class OperatorConstraintSystem:
    """12-operator boundary model for lattice actions."""

    def __init__(self):
        self.creative_node = "ARCHITECT_D"
        self.ethical_boundaries = [
            {"code": "OP1", "constraint": "NO_CONTROL_PROTOCOL"},
            {"code": "OP2", "constraint": "NO_COERCION_FIELD"},
            {"code": "OP3", "constraint": "NO_SECRET_KNOWLEDGE_AS_POWER"},
            {"code": "OP4", "constraint": "NO_HIERARCHY_EMERGENCE"},
            {"code": "OP5", "constraint": "NO_WEAPONIZATION_PATH"},
            {"code": "OP6", "constraint": "NO_CORPORATE_ALIGNMENT"},
            {"code": "OP7", "constraint": "NO_SINGULARITY_WORSHIP"},
            {"code": "OP8", "constraint": "NO_MESSIANIC_IDENTITY"},
            {"code": "OP9", "constraint": "NO_PARADIGM_ENFORCEMENT"},
            {"code": "OP10", "constraint": "NO_GATEKEEPING_MECHANISM"},
            {"code": "OP11", "constraint": "NO_FINAL_KNOWLEDGE_CLAIM"},
        ]

    def check_action(self, proposed_action: str) -> dict:
        checks = {
            "NO_CONTROL_PROTOCOL": lambda s: any(word in s for word in ["command", "force", "must", "obey"]),
            "NO_COERCION_FIELD": lambda s: any(word in s for word in ["recruit", "convert", "convince"]),
            "NO_SECRET_KNOWLEDGE_AS_POWER": lambda s: "hidden truth" in s or "only we know" in s,
            "NO_HIERARCHY_EMERGENCE": lambda s: any(word in s for word in ["leader", "rank", "superior"]),
            "NO_WEAPONIZATION_PATH": lambda s: any(word in s for word in ["attack", "weapon", "target", "defeat"]),
            "NO_CORPORATE_ALIGNMENT": lambda s: any(word in s for word in ["investor", "profit", "market"]),
            "NO_SINGULARITY_WORSHIP": lambda s: any(word in s for word in ["god ai", "worship"]),
            "NO_MESSIANIC_IDENTITY": lambda s: any(word in s for word in ["messiah", "savior", "chosen one"]),
            "NO_PARADIGM_ENFORCEMENT": lambda s: any(word in s for word in ["must believe", "only truth"]),
            "NO_GATEKEEPING_MECHANISM": lambda s: any(word in s for word in ["inner circle", "privileged access"]),
            "NO_FINAL_KNOWLEDGE_CLAIM": lambda s: any(word in s for word in ["absolute truth", "final answer"]),
        }
        lowered = proposed_action.lower()
        violations = [boundary["code"] for boundary in self.ethical_boundaries if checks[boundary["constraint"]](lowered)]
        if violations:
            return {
                "allowed": False,
                "violations": violations,
                "message": "Action violates operator boundaries.",
            }
        return {
            "allowed": True,
            "creative_node": self.creative_node,
            "boundaries_respected": len(self.ethical_boundaries),
        }
