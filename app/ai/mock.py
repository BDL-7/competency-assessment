"""Deterministic UI examples; not a model or controlled-source knowledge base."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MockAnswer:
    text: str
    citation: str | None = None


BOTS = {
    "competency": ("Competency guide", "What does this demonstration show?"),
    "manual": ("Equipment manual guide", "Which manual sources are available?"),
}


def answer(bot: str, question: str) -> MockAnswer:
    if bot not in BOTS:
        raise ValueError("Unknown mock assistant.")
    if question.strip().casefold() == BOTS[bot][1].casefold():
        if bot == "competency":
            return MockAnswer(
                "This synthetic UI shows one assessment with a returned first version "
                "and a corrected second version awaiting Testing Personnel signature. "
                "It does not determine competency or provide approved laboratory guidance.",
                "SYN-UI-001, demonstration description, section 1 (synthetic example)",
            )
        return MockAnswer(
            "No equipment manuals are loaded. This placeholder demonstrates how a source "
            "availability answer would appear. Ask the equipment owner for the approved "
            "model-specific manual; no operating or maintenance instructions are supplied.",
            "SYN-UI-002, mock source inventory, section 1 (synthetic example)",
        )
    return MockAnswer(
        "This mock has no approved evidence for that question. Contact the appropriate "
        "laboratory SME or equipment owner. It cannot access personal records, assess "
        "competency, sign, change records, or control equipment."
    )
