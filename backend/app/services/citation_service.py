import re
from dataclasses import dataclass


@dataclass
class SourceCandidate:
    title: str
    source: str
    year: str | None = None


class CitationService:
    def generate(self, text: str, style: str) -> tuple[list[str], str, list[str]]:
        warnings: list[str] = []
        candidates = self._extract_candidates(text)

        if not candidates:
            warnings.append("No strong citation candidates found. References are empty.")
            return [], text, warnings

        references = [self._format_reference(candidate, style, index + 1) for index, candidate in enumerate(candidates)]
        annotated_text = self._insert_inline_citations(text, candidates, style)
        return references, annotated_text, warnings

    def _extract_candidates(self, text: str) -> list[SourceCandidate]:
        candidates: list[SourceCandidate] = []
        seen_titles: set[str] = set()

        bibliography_match = re.search(r"(references|bibliography)\s*[:\n](.*)$", text, re.IGNORECASE | re.DOTALL)
        if bibliography_match:
            for line in bibliography_match.group(2).splitlines():
                cleaned = line.strip(" -\t")
                if len(cleaned) < 20:
                    continue
                self._add_candidate(candidates, seen_titles, cleaned, cleaned)

        for url_match in re.finditer(r"https?://[^\s)]+", text):
            url = url_match.group(0).strip(".,;")
            host = re.sub(r"^https?://", "", url).split("/")[0]
            title = f"Web source from {host}"
            self._add_candidate(candidates, seen_titles, title, url)

        for doi_match in re.finditer(r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b", text):
            doi = doi_match.group(0)
            self._add_candidate(candidates, seen_titles, f"DOI source {doi}", f"https://doi.org/{doi}")

        for quoted_title in re.finditer(r"\"([^\"]{12,120})\"", text):
            title = quoted_title.group(1).strip()
            self._add_candidate(candidates, seen_titles, title, "Quoted title found in report")

        return candidates[:20]

    def _add_candidate(
        self,
        candidates: list[SourceCandidate],
        seen_titles: set[str],
        title: str,
        source: str,
    ) -> None:
        normalized = re.sub(r"\s+", " ", title.lower()).strip()
        if not normalized or normalized in seen_titles:
            return
        year_match = re.search(r"\b(19|20)\d{2}\b", source)
        year = year_match.group(0) if year_match else None
        seen_titles.add(normalized)
        candidates.append(SourceCandidate(title=title, source=source, year=year))

    def _format_reference(self, candidate: SourceCandidate, style: str, index: int) -> str:
        year = candidate.year or "n.d."
        if style == "MLA":
            return f'Source {index}. "{candidate.title}." {candidate.source}, {year}.'
        if style == "IEEE":
            return f"[{index}] {candidate.title}. Available: {candidate.source}"
        return f"Source {index}. ({year}). {candidate.title}. {candidate.source}."

    def _insert_inline_citations(self, text: str, candidates: list[SourceCandidate], style: str) -> str:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        if len(sentences) <= 1:
            return text

        annotated: list[str] = []
        for index, sentence in enumerate(sentences):
            stripped = sentence.strip()
            if not stripped:
                continue
            source_index = (index % len(candidates)) + 1
            citation = self._inline_citation(style, source_index)
            annotated.append(f"{stripped} {citation}")
        return " ".join(annotated)

    def _inline_citation(self, style: str, source_index: int) -> str:
        if style == "MLA":
            return f"(Source {source_index})"
        if style == "IEEE":
            return f"[{source_index}]"
        return f"(Source {source_index}, n.d.)"
