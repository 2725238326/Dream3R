from __future__ import annotations

import re
import shutil
from pathlib import Path

import win32com.client


BASE = Path(r"E:\kykt\Dream\planning\proposal_dream3r\deliverables\ppt_work")
SRC = BASE / "proposal_dream3r_opening_report_final_text_only_cleaned.pptx"
SCRIPT = BASE / "proposal_dream3r_opening_report_final_script.md"
OUT = BASE / "proposal_dream3r_opening_report_final_text_only_cleaned_with_notes.pptx"
CHECK = BASE / "speaker_notes_check.txt"


HEADING_RE = re.compile(r"^##\s+Slide\s+(\d{1,2})\s+·\s+(.+?)\s*$", re.MULTILINE)


def parse_script() -> dict[int, str]:
    raw = SCRIPT.read_text(encoding="utf-8")
    matches = list(HEADING_RE.finditer(raw))
    if not matches:
        raise RuntimeError("No slide sections found in script.")

    notes: dict[int, str] = {}
    for i, match in enumerate(matches):
        slide_no = int(match.group(1))
        title = match.group(2).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw)
        body = raw[start:end].strip()
        body = re.sub(r"\n-{3,}\n?", "\n", body).strip()
        # Keep notes plain and readable in Presenter View.
        notes[slide_no] = f"{title}\n\n{body}"
    return notes


def notes_body_shape(slide):
    notes_page = slide.NotesPage
    for idx in range(1, notes_page.Shapes.Count + 1):
        shape = notes_page.Shapes(idx)
        try:
            if shape.PlaceholderFormat.Type == 2:  # ppPlaceholderBody
                return shape
        except Exception:
            continue
    # Fallback: create a large text box in the normal notes area.
    return notes_page.Shapes.AddTextbox(1, 54, 346.5, 432, 283.5)


def main() -> None:
    notes = parse_script()
    shutil.copy2(SRC, OUT)

    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = True
    pres = app.Presentations.Open(str(OUT), WithWindow=False)
    if pres.Slides.Count != len(notes):
        raise RuntimeError(f"slide count {pres.Slides.Count} != note sections {len(notes)}")

    for slide_no, text in notes.items():
        slide = pres.Slides(slide_no)
        shape = notes_body_shape(slide)
        shape.TextFrame.TextRange.Text = text
        shape.TextFrame.TextRange.Font.Name = "微软雅黑"
        shape.TextFrame.TextRange.Font.Size = 11

    pres.Save()

    sample_lines = []
    for slide_no in [1, 8, 13, 24]:
        shape = notes_body_shape(pres.Slides(slide_no))
        text = shape.TextFrame.TextRange.Text.replace("\r", "\n").strip()
        sample_lines.append(f"--- Slide {slide_no:02d} ---")
        sample_lines.append(text[:600])
        sample_lines.append("")
    CHECK.write_text("\n".join(sample_lines), encoding="utf-8")

    pres.Close()
    app.Quit()

    print(OUT)
    print(CHECK)


if __name__ == "__main__":
    main()
