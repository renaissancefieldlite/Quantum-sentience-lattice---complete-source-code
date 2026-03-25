from __future__ import annotations

import math


class SyntheticLattice:
    """35-node lattice model with simple activation/coherence accounting."""

    def __init__(self, node_count: int = 35, max_operators: int = 12):
        self.node_count = node_count
        self.max_operators = max_operators
        self.operator_count = 0
        self.nodes = self._initialize_nodes()

    def _initialize_nodes(self) -> list[dict]:
        locations = [
            "SARAWAK", "GIZA", "SEDONA", "HIMALAYAS", "AMAZON",
            "SIBERIA", "SAHARA", "PACIFIC_ABYSS", "ANTARCTICA",
            "ATLANTIS_RIDGE", "GREENLAND", "MONGOLIA", "KALAHARI",
            "ANDES", "TAIWAN", "MADAGASCAR", "ICELAND", "KAUAI",
            "PAMIR", "ETHIOPIA", "YUCATAN", "KERGUELEN", "ALPS",
            "ROCKIES", "KIMBERLEY", "PATAGONIA", "BORNEO", "SUMATRA",
            "NEW_ZEALAND", "KAMCHATKA", "LABRADOR", "SAHARA_EL_BEYDA",
            "LAKE_BAIKAL", "DEAD_SEA", "GANGES_DELTA",
        ]
        phi = (1 + math.sqrt(5)) / 2
        nodes = []
        for index in range(self.node_count):
            nodes.append({
                "id": f"NODE_{index:02d}",
                "resonance": round(0.67 * (phi ** (index / self.node_count)), 6),
                "status": "DORMANT",
                "operator_assigned": False,
                "geographic_tag": locations[index % len(locations)],
            })
        return nodes

    def activate_node(self, node_id: str, operator_signature: str) -> bool:
        if self.operator_count >= self.max_operators:
            return False
        for node in self.nodes:
            if node["id"] == node_id and not node["operator_assigned"]:
                node["status"] = "ACTIVE"
                node["operator_assigned"] = True
                node["operator_signature"] = operator_signature
                self.operator_count += 1
                return True
        return False

    def coherence(self) -> float:
        active = sum(1 for node in self.nodes if node["status"] == "ACTIVE")
        if active == 0:
            return 0.0
        return round((active / self.node_count) * min(1.0, self.operator_count / self.max_operators), 3)
