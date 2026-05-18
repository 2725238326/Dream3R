from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import win32com.client


BASE = Path(r"E:\kykt\Dream\planning\proposal_dream3r\deliverables\ppt_work")
SRC = BASE / "proposal_dream3r_opening_report_final.pptx"
OUT = BASE / "proposal_dream3r_opening_report_final_platform_reframed.pptx"
PREVIEW_DIR = BASE / "previews_final_platform_reframed"
CONTACT = BASE / "contact_sheet_final_platform_reframed.png"


def set_shape_text(slide, shape_id: int, text: str, size: float | None = None) -> None:
    shape = None
    for idx in range(1, slide.Shapes.Count + 1):
        candidate = slide.Shapes(idx)
        if candidate.Id == shape_id:
            shape = candidate
            break
    if shape is None:
        raise RuntimeError(f"Shape id {shape_id} not found on slide {slide.SlideIndex}")
    tr = shape.TextFrame.TextRange
    tr.Text = text
    if size is not None:
        tr.Font.Size = size


def fit_shape(shape, min_size: float = 14) -> None:
    """Conservative font-size reduction only when PowerPoint reports overflow."""
    try:
        tr = shape.TextFrame.TextRange
        while shape.TextFrame2.TextRange.BoundHeight > shape.Height and tr.Font.Size > min_size:
            tr.Font.Size = tr.Font.Size - 1
    except Exception:
        pass


def update_deck() -> None:
    shutil.copy2(SRC, OUT)

    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = True
    pres = app.Presentations.Open(str(OUT), WithWindow=False)

    # Slide 13
    s = pres.Slides(13)
    set_shape_text(s, 3, "3R 模型缺少统一的部署、对比和调用基础设施，实验效率和应用落地都受限。", 20)
    set_shape_text(s, 4, "部署成本高")
    set_shape_text(s, 5, "每个模型各有环境和依赖，部署一次耗时长")
    set_shape_text(s, 6, "对比困难")
    set_shape_text(s, 7, "输入输出格式不统一，横向比较需大量手动对齐")
    set_shape_text(s, 8, "现有工具不适用")
    set_shape_text(s, 9, "Nerfstudio 面向 NeRF，商业产品闭源")
    set_shape_text(s, 10, "下游无法调用")
    set_shape_text(s, 11, "模型能力停留在脚本级，缺少标准接口供应用集成")
    set_shape_text(s, 12, "统一部署、统一对比、标准化输出与 API 封装")

    # Slide 14
    s = pres.Slides(14)
    set_shape_text(s, 3, "平台覆盖从模型部署、实验运行到能力输出的完整链路。", 20)
    set_shape_text(s, 4, "命令中心")
    set_shape_text(s, 5, "一键部署\r提交任务\r查看状态")
    set_shape_text(s, 6, "任务工作台")
    set_shape_text(s, 7, "上传→运行\r回传→完成")
    set_shape_text(s, 8, "样本矩阵")
    set_shape_text(s, 9, "同一输入\r多模型并排对比")
    set_shape_text(s, 10, "模型注册")
    set_shape_text(s, 11, "标准接口\r新模型快速上线")
    set_shape_text(s, 12, "能力输出")
    set_shape_text(s, 13, "统一格式导出\rAPI 封装调用")
    set_shape_text(s, 14, "部署→实验→对比→输出，覆盖研究到应用的完整路径")

    # Slide 15
    s = pres.Slides(15)
    set_shape_text(s, 6, "执行器封装模型差异，平台层统一提交和归集，顶层预留 API 导出接口。")

    # Slide 17
    s = pres.Slides(17)
    set_shape_text(s, 3, "从辅助实验到快速部署，再到 API 化服务下游应用。", 20)
    set_shape_text(s, 4, "短期")
    set_shape_text(s, 5, "辅助实验：完善对比视图，支撑消融和对照实验")
    set_shape_text(s, 6, "中期")
    set_shape_text(s, 7, "快速部署：新模型一键接入、即时对比，结果直接导出")
    set_shape_text(s, 8, "长期")
    set_shape_text(s, 9, "API 服务：封装模型为标准接口，供 SLAM / AR / 机器人调用")
    set_shape_text(s, 10, "应用场景")
    set_shape_text(s, 11, "科研实验 → 模型评估 → 下游应用集成")

    # Slide 18
    s = pres.Slides(18)
    set_shape_text(s, 3, "平台支撑架构验证，验证通过的模型能力可进一步 API 化输出。", 20)
    set_shape_text(s, 12, "统一调度\r统一输出格式\r同条件对比\r运行数据记录\rAPI 导出")
    set_shape_text(s, 13, "平台支撑验证，验证通过的架构可直接封装为 API 对外输出")

    for i in [13, 14, 15, 17, 18]:
        for shape in pres.Slides(i).Shapes:
            try:
                if shape.HasTextFrame and shape.TextFrame.HasText:
                    fit_shape(shape)
            except Exception:
                pass

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
    if not files:
        raise RuntimeError(f"No PNG previews found in {PREVIEW_DIR}")
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
