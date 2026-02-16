import re
from collections.abc import Iterable

CUSTOM_PATTERNS: dict[str, str] = {
    "EMAIL": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "MRN": r"\b(?:MRN[:\s-]*)?\d{6,10}\b",
    "PHONE_NUMBER": r"\b(?:\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
    "DATE_TIME": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
    "PERSON": r"\b([A-Z][a-z]+\s[A-Z][a-z]+)\b",
}

PLACEHOLDERS = {
    "PERSON": "[PERSON]",
    "PHONE_NUMBER": "[PHONE]",
    "LOCATION": "[LOCATION]",
    "DATE_TIME": "[DATE]",
    "EMAIL": "[EMAIL]",
    "MRN": "[MRN]",
}


class Deidentifier:
    def __init__(self) -> None:
        self.analyzer = None
        try:
            from presidio_analyzer import AnalyzerEngine

            self.analyzer = AnalyzerEngine()
        except Exception:
            self.analyzer = None

    def _replace_with_regex(self, text: str, entity_type: str) -> tuple[str, list[dict]]:
        pattern = CUSTOM_PATTERNS.get(entity_type)
        if not pattern:
            return text, []
        matches = list(re.finditer(pattern, text))
        metadata = [{"entity_type": entity_type, "start": m.start(), "end": m.end()} for m in matches]
        replaced = re.sub(pattern, PLACEHOLDERS.get(entity_type, "[REDACTED]"), text)
        return replaced, metadata

    def deidentify(self, text: str, entities: Iterable[str] | None = None) -> tuple[str, list[dict]]:
        target_entities = list(entities or ["PERSON", "PHONE_NUMBER", "LOCATION", "DATE_TIME"])
        collected: list[dict] = []

        if self.analyzer:
            try:
                findings = self.analyzer.analyze(text=text, entities=target_entities, language="en")
                for finding in findings:
                    collected.append({"entity_type": finding.entity_type, "start": finding.start, "end": finding.end})
            except Exception:
                pass

        for entity_type in ["EMAIL", "MRN", "PHONE_NUMBER", "DATE_TIME", "PERSON"]:
            text, metadata = self._replace_with_regex(text, entity_type)
            collected.extend(metadata)

        return text, collected
