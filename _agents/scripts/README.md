# Agent scripts

Scripts used to build the reading copies in `_library/text/`. Python 3, standard library plus `pandoc` and `pdftotext` (poppler) on the PATH. Run from `_library/text/`.

- `convert_iapp_epub.py <unzipped-epub>/OEBPS <out-folder>`: IAPP epub → one markdown file per chapter (headings, figures, boxes as blockquotes, endnotes). Built for *AI Governance: From Strategy to Execution*; other InDesign-exported IAPP epubs will need the class names checked. Unzip the epub first (`unzip book.epub -d /tmp/ep`).
- `split_eu_ai_act.py <act.txt> eu-ai-act`: EU AI Act → one file per article and annex, recitals, index, with cross-references linked. Input is `pdftotext EU-ai-act.pdf act.txt` (no `-layout`).
- `split_oecd_report.py <pdf> <out-folder>`: OECD classification report → one file per section with `## Page N` anchors; page ranges are hard-coded in `SECS`. Copy and adjust the ranges for other reports.

Pattern for a new long source: one file per natural unit (chapter, article, section), frontmatter with `title`, `source`, `original`, headings or page anchors for citation, an `00-index.md`, then a source card in `kb/sources/`.
