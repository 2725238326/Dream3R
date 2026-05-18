from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw
import win32com.client


BASE = Path(r"E:\kykt\Dream\planning\proposal_dream3r\deliverables\ppt_work")
SRC = BASE / "proposal_dream3r_opening_report_final_platform_reframed.pptx"
OUT = BASE / "proposal_dream3r_opening_report_final_text_only_cleaned.pptx"
PREVIEW_DIR = BASE / "previews_final_text_only_cleaned"
CONTACT = BASE / "contact_sheet_final_text_only_cleaned.png"


def find_shape(slide, shape_id: int):
    for idx in range(1, slide.Shapes.Count + 1):
        shape = slide.Shapes(idx)
        if shape.Id == shape_id:
            return shape
    raise RuntimeError(f"shape id={shape_id} not found on slide {slide.SlideIndex}")


def set_text(slide, shape_id: int, text: str, size: float | None = None) -> None:
    shape = find_shape(slide, shape_id)
    tr = shape.TextFrame.TextRange
    tr.Text = text
    if size is not None:
        tr.Font.Size = size


def update_deck() -> None:
    shutil.copy2(SRC, OUT)

    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = True
    pres = app.Presentations.Open(str(OUT), WithWindow=False)

    replacements = {
        # Slide 04: avoid "four mechanisms" sounding like a fixed taxonomy.
        (4, 29): ("3R 用一次推理替代多步级联，后续工作沉淀出可借鉴的技术线索。", 20),
        (4, 36): ("可借鉴线索", None),
        (4, 35): ("点图表示\n支持深度 / 位姿扩展", None),
        (4, 38): ("这些技术线索为候选架构提供直接参考", None),

        # Slide 06: "六项机制" was numerically unclear.
        (6, 3): ("先从已有 3R 工作中提炼可用机制，再用本课题设计补足未解决的问题。", 20),
        (6, 4): ("已有技术线索", None),
        (6, 11): ("本课题补足设计", None),
        (6, 13): ("既有机制借鉴 + 四项补足设计 → 候选架构方案", None),

        # Slide 07/08/09: keep module language consistent; do not touch embedded figures.
        (7, 9): ("架构提出候选方案，平台提供统一实验条件", None),
        (8, 3): ("五个核心模块由总线模块协调，形成从特征提取到校验输出的完整链路。", 20),
        (8, 6): ("输出包括三维点图、动态掩码和可复核中间证据。", None),
        (9, 92): ("记忆模块", 28),
        (9, 3): ("长序列记忆分为压缩、检索和滑窗三条支路，分别处理远程状态、空间锚点和近邻上下文。", 19),
        (9, 6): ("压缩分支保留远程状态，选择分支检索空间锚点，滑窗分支保留近邻上下文。", None),
        (10, 6): ("校验思路源自 Test3R，本课题将其嵌入架构内部，支持在线复核与修复。", None),

        # Slide 12: avoid hard numeric claim without unit/source explanation.
        (12, 13): ("端到端运行无崩溃，点图误差指标完成初步接入", None),

        # Later summary consistency.
        (18, 13): ("平台支撑验证，验证通过的架构可进一步封装为 API 对外输出", None),
        (20, 3): ("四个创新点分别回应前面提出的主要问题。", 20),
        (20, 96): ("6 个模型完成端到端验证", None),
        (21, 9): ("7 份设计文档\n跨模块信号契约完成\n原型 v0.3 跑通\n18 项技术里程碑完成", None),
        (22, 93): ("近期完成开题与平台补齐，中期集中做模块消融，后期整理论文并补充实验。", None),
    }

    for (slide_no, shape_id), (text, size) in replacements.items():
        set_text(pres.Slides(slide_no), shape_id, text, size)

    pres.Save()

    if PREVIEW_DIR.exists():
        shutil.rmtree(PREVIEW_DIR)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    pres.Export(str(PREVIEW_DIR), "PNG", 1920, 1080)
    pres.Close()
    app.Quit()


def make_contact_sheet() -> None:
    def slide_no(path: Path) -> int:
        digits = "".join(ch for ch in path.stem if ch.isdigit())
        return int(digits) if digits else 0

    files = sorted(PREVIEW_DIR.glob("*.PNG"), key=slide_no)
    thumbs = []
    for f in files:
        im = Image.open(f).convert("RGB")
        im.thumbnail((360, 203), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (360, 223), "white")
        canvas.paste(im, (0, 20))
        draw = ImageDraw.Draw(canvas)
        draw.rectangle([0, 0, 359, 222], outline=(210, 220, 230))
        draw.text((8, 3), f"Slide {slide_no(f):02d}", fill=(0, 70, 130))
        thumbs.append(canvas)

    cols = 4
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 360, rows * 223), (245, 247, 250))
    for idx, im in enumerate(thumbs):
        sheet.paste(im, ((idx % cols) * 360, (idx // cols) * 223))
    sheet.save(CONTACT)


if __name__ == "__main__":
    update_deck()
    make_contact_sheet()
    print(OUT)
    print(PREVIEW_DIR)
    print(CONTACT)
