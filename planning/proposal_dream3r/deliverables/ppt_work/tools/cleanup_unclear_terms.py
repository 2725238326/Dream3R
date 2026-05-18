from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw
import win32com.client


BASE = Path(r"E:\kykt\Dream\planning\proposal_dream3r\deliverables\ppt_work")
SRC = BASE / "proposal_dream3r_opening_report_final_platform_reframed.pptx"
OUT = BASE / "proposal_dream3r_opening_report_final_terms_cleaned.pptx"
PREVIEW_DIR = BASE / "previews_final_terms_cleaned"
CONTACT = BASE / "contact_sheet_final_terms_cleaned.png"


def rgb(r: int, g: int, b: int) -> int:
    return r + g * 256 + b * 65536


DARK = rgb(0, 65, 125)
BLUE = rgb(0, 84, 160)
MID = rgb(46, 119, 190)
LIGHT = rgb(226, 238, 249)
GREEN = rgb(38, 135, 96)
GREEN_LIGHT = rgb(231, 244, 237)
ORANGE = rgb(220, 97, 23)
ORANGE_LIGHT = rgb(255, 240, 225)
GRAY = rgb(245, 247, 250)
LINE = rgb(43, 107, 185)
TEXT = rgb(5, 35, 70)


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


def style_text(shape, size=15, bold=False, color=TEXT, font="微软雅黑") -> None:
    tr = shape.TextFrame.TextRange
    tr.Font.Name = font
    tr.Font.Size = size
    tr.Font.Bold = -1 if bold else 0
    tr.Font.Color.RGB = color
    tr.ParagraphFormat.Alignment = 2
    try:
        shape.TextFrame.VerticalAnchor = 3
    except Exception:
        pass


def add_box(slide, x, y, w, h, text, fill=LIGHT, line=LINE, size=15, bold=False, color=TEXT, radius=True):
    shape_type = 5 if radius else 1
    shape = slide.Shapes.AddShape(shape_type, x, y, w, h)
    shape.Fill.ForeColor.RGB = fill
    shape.Line.ForeColor.RGB = line
    shape.Line.Weight = 1.2
    shape.TextFrame.TextRange.Text = text
    shape.TextFrame.MarginLeft = 6
    shape.TextFrame.MarginRight = 6
    shape.TextFrame.MarginTop = 4
    shape.TextFrame.MarginBottom = 4
    style_text(shape, size=size, bold=bold, color=color)
    return shape


def add_arrow(slide, x1, y1, x2, y2, color=MID, weight=2.0):
    line = slide.Shapes.AddLine(x1, y1, x2, y2)
    line.Line.ForeColor.RGB = color
    line.Line.Weight = weight
    line.Line.EndArrowheadStyle = 3
    return line


def add_plain_line(slide, x1, y1, x2, y2, color=MID, weight=1.6):
    line = slide.Shapes.AddLine(x1, y1, x2, y2)
    line.Line.ForeColor.RGB = color
    line.Line.Weight = weight
    return line


def delete_pictures(slide) -> None:
    for idx in range(slide.Shapes.Count, 0, -1):
        shape = slide.Shapes(idx)
        if shape.Type == 13:  # msoPicture
            shape.Delete()


def rebuild_slide_08(slide) -> None:
    delete_pictures(slide)
    set_text(slide, 3, "五个核心模块由总线模块协调，形成从特征提取到校验输出的完整链路。", 20)
    set_text(slide, 6, "输出包括三维点图、动态掩码和可复核中间证据。", 17)

    y = 185
    xs = [65, 195, 325, 455, 585, 715]
    labels = [
        ("输入", "图像序列\n单图 / 图像对"),
        ("感知模块", "提取视觉特征"),
        ("记忆模块", "维护长序列上下文"),
        ("永久性模块", "区分静态结构\n与动态对象"),
        ("校验模块", "形成冲突评分\n给出修复动作"),
        ("编排模块", "选择或切换\n候选模型"),
    ]
    for i, (title, body) in enumerate(labels):
        fill = LIGHT if i not in (3, 4) else (GREEN_LIGHT if i == 3 else ORANGE_LIGHT)
        line = LINE if i not in (3, 4) else (GREEN if i == 3 else ORANGE)
        add_box(slide, xs[i], y, 110, 82, f"{title}\n{body}", fill=fill, line=line, size=13, bold=i != 0)
        if i < len(labels) - 1:
            add_arrow(slide, xs[i] + 112, y + 41, xs[i + 1] - 8, y + 41)

    add_box(slide, 220, 335, 520, 46, "总线模块：统一信号传递、修复动作与模型切换规则", fill=GRAY, line=rgb(150, 160, 170), size=16, bold=True)
    for x in [250, 380, 510, 640]:
        add_arrow(slide, x, 335, x, 285, color=rgb(120, 130, 140), weight=1.4)


def rebuild_slide_09(slide) -> None:
    delete_pictures(slide)
    set_text(slide, 92, "记忆模块", 28)
    set_text(slide, 3, "长序列记忆分为压缩、检索和滑窗三条支路，分别处理远程状态、空间锚点和近邻上下文。", 19)
    set_text(slide, 6, "压缩分支保留远程状态，选择分支检索空间锚点，滑窗分支保留近邻上下文。", 17)

    add_box(slide, 70, 222, 130, 55, "当前帧特征", fill=GRAY, line=LINE, size=16, bold=True)
    branches = [
        (260, 150, "压缩分支", "压缩历史特征\n递推状态\n状态记忆向量", BLUE, LIGHT),
        (260, 258, "选择分支", "空间锚点检索\n锚点库（容量可调）\n相关锚点检索", GREEN, GREEN_LIGHT),
        (260, 366, "滑窗分支", "近邻帧局部特征\n局部直接注意力", rgb(40, 150, 170), rgb(230, 248, 250)),
    ]
    for x, y, title, body, line, fill in branches:
        add_box(slide, x, y, 185, 88, f"{title}\n{body}", fill=fill, line=line, size=13, bold=True)
        add_arrow(slide, 200, 250, x - 8, y + 44)
        add_arrow(slide, x + 188, y + 44, 545, 250)

    add_box(slide, 555, 205, 130, 90, "注意力融合\n\n多源记忆合并", fill=BLUE, line=BLUE, size=17, bold=True, color=rgb(255, 255, 255))
    add_arrow(slide, 685, 250, 760, 250)
    add_box(slide, 770, 192, 130, 116, "输出\n\n长序列几何上下文\n隐空间漂移监测", fill=GRAY, line=LINE, size=14, bold=True)
    add_box(slide, 570, 350, 210, 40, "记忆缓存管理：控制保留、压缩与删除", fill=GRAY, line=rgb(150, 160, 170), size=14, bold=True)
    add_arrow(slide, 675, 350, 675, 298, color=rgb(120, 130, 140), weight=1.4)


def rebuild_slide_10(slide) -> None:
    delete_pictures(slide)
    set_text(slide, 3, "校验模块把几何不一致转成冲突评分，再决定通过、局部重跑或模型切换。", 20)
    set_text(slide, 6, "校验思路源自 Test3R，本课题将其嵌入架构内部，支持在线复核与修复。", 17)

    sources = [
        (85, "Sampson 残差\n对极几何一致性"),
        (305, "深度一致性\n相邻帧尺度检查"),
        (525, "共视冲突\n多帧可见区域对照"),
    ]
    for x, label in sources:
        add_box(slide, x, 175, 155, 72, label, fill=LIGHT, line=LINE, size=14, bold=True)
        add_arrow(slide, x + 155, 211, 725, 211)

    add_box(slide, 725, 170, 130, 82, "冲突评分\n\n低 / 中 / 高", fill=ORANGE_LIGHT, line=ORANGE, size=16, bold=True)
    add_plain_line(slide, 790, 252, 790, 300, color=ORANGE, weight=1.8)
    add_plain_line(slide, 235, 300, 760, 300, color=ORANGE, weight=1.8)
    actions = [
        (175, "低冲突\n通过并保留"),
        (345, "局部冲突\n重跑问题区域"),
        (515, "全局冲突\n整窗口重跑"),
        (685, "模型不匹配\n交给编排模块"),
    ]
    for x, label in actions:
        add_box(slide, x, 325, 125, 58, label, fill=GRAY, line=LINE, size=13, bold=True)
        add_arrow(slide, x + 62.5, 300, x + 62.5, 323, color=ORANGE, weight=1.4)


def update_texts(pres) -> None:
    replacements = {
        (4, 29): ("3R 用一次推理替代多步级联，后续工作沉淀出可复用的技术线索。", 20),
        (4, 36): ("可复用线索", None),
        (4, 35): ("点图表示\n支持深度 / 位姿扩展", None),
        (4, 37): ("记忆、递推\n校验、匹配增强", None),
        (4, 38): ("这些技术线索为候选架构提供直接参考", None),
        (6, 3): ("先从已有 3R 工作中提炼可用机制，再用本课题设计补足未解决的问题。", 20),
        (6, 4): ("已有技术线索", None),
        (6, 11): ("本课题补足设计", None),
        (6, 13): ("既有机制借鉴 + 四项补足设计 → 候选架构方案", None),
        (7, 9): ("架构提出候选方案，平台提供统一实验条件", None),
        (12, 13): ("端到端运行无崩溃，点图误差指标完成初步接入", None),
        (18, 13): ("平台支撑验证，验证通过的架构可进一步封装为 API 对外输出", None),
        (20, 3): ("四个创新点分别回应前面提出的主要问题。", 20),
        (20, 96): ("6 个模型完成端到端验证", None),
        (21, 9): ("7 份设计文档\n跨模块信号契约完成\n原型 v0.3 跑通\n18 项技术里程碑完成", None),
        (22, 93): ("近期完成开题与平台补齐，中期集中做模块消融，后期整理论文并补充实验。", None),
    }
    for (slide_no, shape_id), (text, size) in replacements.items():
        set_text(pres.Slides(slide_no), shape_id, text, size)


def export_and_contact(pres) -> None:
    if PREVIEW_DIR.exists():
        shutil.rmtree(PREVIEW_DIR)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    pres.Export(str(PREVIEW_DIR), "PNG", 1920, 1080)


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


def main() -> None:
    shutil.copy2(SRC, OUT)
    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = True
    pres = app.Presentations.Open(str(OUT), WithWindow=False)

    update_texts(pres)
    rebuild_slide_08(pres.Slides(8))
    rebuild_slide_09(pres.Slides(9))
    rebuild_slide_10(pres.Slides(10))

    pres.Save()
    export_and_contact(pres)
    pres.Close()
    app.Quit()
    make_contact_sheet()
    print(OUT)
    print(PREVIEW_DIR)
    print(CONTACT)


if __name__ == "__main__":
    main()
