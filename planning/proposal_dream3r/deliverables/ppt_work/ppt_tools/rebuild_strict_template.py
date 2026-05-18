import os
import shutil
from pathlib import Path

import win32com.client
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"E:\kykt\Dream\planning\proposal_dream3r")
WORK = ROOT / "deliverables" / "ppt_work"
TEMPLATE = Path(r"E:\Work\HSY\学术风ppt模板-蓝色.pptx")
OUT = WORK / "proposal_dream3r_opening_report_strict_template_v2.pptx"
PREVIEW_DIR = WORK / "previews_strict_template_v2"
CONTACT = WORK / "contact_sheet_strict_template_v2.png"
ASSET_DIR = ROOT / "ppt_assets" / "ai"
STRICT_ASSET_DIR = WORK / "strict_assets"

SLIDES = [
    (3, "面向前馈式三维重建的\n候选架构设计与统一聚合管理平台"),
    (45, "研究背景：3R 方向快速演进"),
    (51, "问题提出：失败模式与未解问题"),
    (48, "研究现状：四轴覆盖矩阵"),
    (51, "工具链空白：支柱 B 的动机"),
    (37, "研究目标：四个目标与两大支柱"),
    (25, "候选架构 X：整体设计"),
    (25, "校验模块：几何一致性反馈"),
    (51, "编排模块：多专家路由机制"),
    (25, "记忆模块：长序列状态管理"),
    (51, "聚合管理平台：四层架构"),
    (25, "统一执行合同：跨模型抽象"),
    (48, "跨模型实测：耗时差异明显"),
    (25, "实验设计：三层证据链"),
    (37, "创新点：问题驱动的四项设计"),
    (51, "支柱 A 进展：候选架构入口"),
    (51, "支柱 B 进展：平台工程基础"),
    (68, "研究计划：阶段推进安排"),
    (66, "风险分析：边界与对策"),
    (73, "总结与致谢"),
]

TEXTS = {
    2: [
        "DUSt3R 之后，前馈式三维重建从稀疏匹配扩展到密集点图、动态场景与长序列机制。",
        "2024 DUSt3R：pose-free pointmap",
        "2024 MASt3R：3D grounding / matching",
        "2025 Fast3R：many-view single forward",
        "2024-25 MonST3R：dynamic 4D",
        "2025 Spann3R / CUT3R：long-sequence memory",
        "2025 Test3R / TTT3R：test-time mechanisms",
        "方向快速扩展，但比较口径、复现入口与跨模型实验仍不统一。",
    ],
    3: [
        "本研究不押注单一分支，而是围绕失败模式建立候选架构与统一评测入口。",
        "六类失败模式",
        "尺度漂移 / 几何不一致",
        "长序列记忆衰减",
        "动态场景错配",
        "模型接口不统一",
        "研究问题",
        "Q1：验证信号如何反馈到前馈流程？",
        "Q2：长序列内存如何保持稳定？",
        "Q3：多专家如何组合而非孤立比较？",
        "Q4：如何形成统一实验平台？",
        "研究边界：候选架构不是最终方案",
        "输出目标：统一对照实验与复用入口",
    ],
    4: [
        "覆盖矩阵显示：现有方法在几何校验、长序列内存、多专家组合和统一平台方面覆盖不均衡。",
        "first-class：作为核心机制",
        "partial：局部涉及",
        "absent：缺少明确接口",
        "6 项 first-class",
        "11 项 partial",
        "4 项 absent",
        "结论：候选架构与平台建设应服务系统比较，而不是单点性能宣称。",
    ],
    5: [
        "当前工具链主要瓶颈不在模型数量，而在统一入口、统一格式和统一实验记录不足。",
        "模型入口分散",
        "不同仓库、环境与脚本彼此割裂",
        "输出格式异构",
        "pointmap、mesh、动态轨迹难以横向比较",
        "日志口径不一",
        "耗时、状态、失败原因缺少统一记录",
        "平台任务：统一 job / status / scene_meta",
        "支撑作用：降低比较成本",
        "平台支柱 B 用于降低比较成本，并支撑支柱 A 的可验证性。",
    ],
    6: [
        "设计目标 1",
        "建立可检验的候选架构 X",
        "设计目标 2",
        "统一多模型接入与执行合同",
        "设计目标 3",
        "形成对比实验与消融计划",
        "支柱 A：候选架构",
        "支柱 B：聚合管理平台",
        "二者关系：平台提供实验入口，架构提出可检验假设。",
    ],
    7: [
        "候选架构 X 由前馈模型、校验反馈、多专家编排和记忆管理组成，后续通过消融实验验证。",
    ],
    8: [
        "校验模块将几何一致性信号反馈到前馈流程，用于发现失败案例并支撑修正策略。",
    ],
    9: [
        "编排模块不预设某个模型最优，而是依据任务与场景特征进行可配置组合。",
        "任务输入",
        "场景类型、序列长度、动态程度",
        "候选专家",
        "快速模型、鲁棒模型、动态场景模型",
        "路由依据",
        "失败信号、资源约束、输出需求",
        "输出结果",
        "模型选择与结果聚合记录",
        "边界约束",
        "组合机制需通过对照实验验证",
    ],
    10: [
        "记忆模块面向长序列输入，统一短期状态、长期状态和检索记忆三类机制。",
    ],
    11: [
        "聚合管理平台采用桌面前端、本地后端、远端调度和模型执行层的分层结构。",
    ],
    12: [
        "统一执行合同规定输入、状态、日志、输出和错误返回，是跨模型比较的基础。",
    ],
    13: [
        "远端视频输入下，不同模型推理耗时差异显著，说明统一调度和可观测记录具有工程必要性。",
        "Spann3R 24.8s",
        "CUT3R 26.2s",
        "Fast3R 28.5s",
        "DUSt3R 91.2s",
        "MASt3R 95.0s",
        "MonST3R 223.3s",
        "耗时仅作为调度与实验管理依据，不直接等同于模型优劣。",
    ],
    14: [
        "实验设计围绕场景覆盖、校验消融、长序列评测和平台复用能力展开。",
    ],
    15: [
        "创新点 1",
        "校验作为架构组件",
        "创新点 2",
        "异构多专家组合",
        "创新点 3",
        "长序列内存统一",
        "创新点 4",
        "统一聚合管理平台",
        "创新点均从研究问题出发，后续通过对照实验验证。",
    ],
    16: [
        "支柱 A 已完成候选架构拆分与实验入口梳理，后续重点是消融验证。",
        "已完成",
        "综述 18 页，44 篇引用",
        "KITTI 集成验证与实验规划",
        "候选模块",
        "Critic、Composer、Memory",
        "待验证",
        "统一 ablation 与 benchmark",
        "下一步",
        "补充长序列和动态场景对照组",
    ],
    17: [
        "支柱 B 已具备多模型接入、统一执行合同和远端调度基础，UI 截图待稳定后补充。",
        "7 个模型接入",
        "DUSt3R / MASt3R / MonST3R / Fast3R / Spann3R / CUT3R / Align3R",
        "6 项验证通过",
        "文件上传、远端执行、日志记录、结果回传",
        "约 15000 行代码",
        "平台 UI 暂不展示，避免使用未定稿界面。",
        "工程证据",
        "统一执行合同和远端任务闭环",
        "后续补充",
        "稳定版 UI 截图与交互流程",
    ],
    18: [
        "M1-M2",
        "基线复现与平台稳定",
        "M3-M4",
        "Critic / Composer / Memory 消融",
        "M5-M6",
        "长序列与动态场景实验",
        "M7-M8",
        "论文撰写与系统整理",
    ],
    19: [
        "风险可控的前提是明确 claim 边界：候选方案必须由对照实验支持。",
        "实验风险",
        "性能波动或提升不稳定",
        "设置强基线与消融组",
        "工程风险",
        "模型适配与远端资源受限",
        "保留批处理与离线执行方案",
        "表达风险",
        "避免把计划写成既有结果",
        "统一使用候选、评估、对照实验表述",
    ],
}

IMAGES = {
    4: "coverage_matrix_strict.png",
    7: "F05_candidate_architecture_x_3840x2160.png",
    8: "F06_critic_module_flow_3840x2160.png",
    10: "F08_memory_three_branch_3840x2160.png",
    11: "F09_platform_four_layer_architecture_3840x2160.png",
    12: "F10_execution_contract_sequence_3840x2160.png",
    13: "timing_bars_strict.png",
    14: "F12_experiment_design_overview_3840x2160.png",
}

IMAGE_POS = {
    4: (70, 125, 820, 355),
    7: (90, 135, 780, 330),
    8: (90, 135, 780, 330),
    10: (90, 135, 780, 330),
    11: (90, 135, 780, 330),
    12: (90, 135, 780, 330),
    13: (70, 125, 820, 355),
    14: (90, 135, 780, 330),
}


def shape_text(shape):
    try:
        if shape.HasTextFrame and shape.TextFrame.HasText:
            return shape.TextFrame.TextRange.Text.strip()
    except Exception:
        return ""
    return ""


def iter_shapes(shapes):
    for shp in shapes:
        yield shp
        try:
            if shp.Type == 6:  # msoGroup
                for child in iter_shapes(shp.GroupItems):
                    yield child
        except Exception:
            pass


def replace_title(slide, title, idx):
    candidates = []
    for shp in iter_shapes(slide.Shapes):
        txt = shape_text(shp)
        if not txt:
            continue
        try:
            if shp.Top < 85 and shp.Left < 780 and "北京航空航天大学" not in txt:
                candidates.append(shp)
        except Exception:
            pass
    candidates = sorted(candidates, key=lambda s: (s.Top, s.Left))
    if idx not in (1, 20):
        for shp in candidates:
            try:
                if shp.Left < 65 and shp.Width < 80:
                    shp.TextFrame.TextRange.Text = "1.1"
            except Exception:
                pass
        title_box = None
        for shp in candidates:
            try:
                if shp.Left >= 60 and shp.Width > 220:
                    if title_box is None or shp.Width > title_box.Width:
                        title_box = shp
            except Exception:
                pass
        if title_box is not None:
            try:
                title_box.TextFrame.TextRange.Text = title
            except Exception:
                pass
        else:
            for shp in candidates:
                try:
                    shp.TextFrame.TextRange.Text = title
                    break
                except Exception:
                    pass
    elif idx == 1:
        all_text = [s for s in iter_shapes(slide.Shapes) if shape_text(s)]
        all_text = sorted(all_text, key=lambda s: (s.Top, s.Left))
        repl = [
            "硕士学位论文开题报告",
            title,
            "汇报人：XXX",
            "北京航空航天大学  |  计算机视觉与三维重建方向",
            "2026年5月",
        ]
        j = 0
        for shp in all_text:
            txt = shape_text(shp)
            if "北京航空航天大学" in txt and shp.Top < 80:
                continue
            if j < len(repl):
                try:
                    shp.TextFrame.TextRange.Text = repl[j]
                    j += 1
                except Exception:
                    pass
            else:
                try:
                    shp.TextFrame.TextRange.Text = ""
                except Exception:
                    pass
    else:
        for shp in iter_shapes(slide.Shapes):
            txt = shape_text(shp)
            if txt and ("感谢" in txt or "汇报" in txt or "XXXX" in txt):
                try:
                    shp.TextFrame.TextRange.Text = "总结与致谢\n\n本研究以候选架构 X 与聚合管理平台为两大支柱，面向前馈式三维重建提供可对照、可复用的研究框架。\n\n汇报人：XXX"
                    break
                except Exception:
                    pass


def clear_content_pictures(slide):
    doomed = []
    for shp in slide.Shapes:
        try:
            if shp.Top > 90 and shp.Type in (13, 7):  # picture, embedded ole-ish
                doomed.append(shp)
        except Exception:
            pass
    for shp in doomed:
        try:
            shp.Delete()
        except Exception:
            pass


def fill_texts(slide, texts, idx):
    boxes = []
    for shp in iter_shapes(slide.Shapes):
        try:
            if not shp.HasTextFrame:
                continue
            if shp.Top < 88 or shp.Left > 850 and shp.Top < 90:
                continue
            if idx == 20:
                continue
            boxes.append(shp)
        except Exception:
            pass
    boxes = sorted(boxes, key=lambda s: (s.Top, s.Left))
    for i, shp in enumerate(boxes):
        try:
            shp.TextFrame.TextRange.Text = texts[i] if i < len(texts) else ""
            if i < len(texts):
                tr = shp.TextFrame.TextRange
                if shp.Width > 90:
                    tr.Font.Color.RGB = 6826768
                if shp.Top > 160 and shp.Width > 90:
                    tr.Font.Size = min(max(tr.Font.Size, 13), 18)
        except Exception:
            pass


def add_image(slide, path, left=90, top=130, width=780, height=330, backing=True):
    if not path.exists():
        return
    if backing:
        try:
            bg = slide.Shapes.AddShape(1, left, top, width, height)
            bg.Fill.ForeColor.RGB = 16777215
            bg.Line.ForeColor.RGB = 10243594
            bg.Line.Weight = 1
        except Exception:
            pass
    img = Image.open(path)
    iw, ih = img.size
    scale = min(width / iw, height / ih)
    w, h = iw * scale, ih * scale
    l = left + (width - w) / 2
    t = top + (height - h) / 2
    slide.Shapes.AddPicture(str(path), False, True, l, t, w, h)


def make_strict_assets():
    STRICT_ASSET_DIR.mkdir(parents=True, exist_ok=True)

    font_paths = [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simsun.ttc",
        r"C:\Windows\Fonts\arial.ttf",
    ]
    font_path = next((p for p in font_paths if Path(p).exists()), None)
    f_title = ImageFont.truetype(font_path, 34) if font_path else ImageFont.load_default()
    f_head = ImageFont.truetype(font_path, 24) if font_path else ImageFont.load_default()
    f_body = ImageFont.truetype(font_path, 20) if font_path else ImageFont.load_default()
    blue = (18, 82, 155)
    line = (45, 111, 180)
    pale = (238, 245, 252)
    orange = (231, 135, 45)
    green = (66, 158, 108)
    red = (210, 83, 75)

    rows = [
        ("外参估计", "first-class"),
        ("匹配表示", "partial"),
        ("动态场景", "partial"),
        ("长序列记忆", "first-class"),
        ("测试时优化", "partial"),
        ("校验反馈", "absent"),
        ("多专家组合", "partial"),
        ("统一平台", "absent"),
    ]
    im = Image.new("RGB", (1500, 820), "white")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 20, 1480, 800), radius=12, outline=line, width=3, fill=(252, 254, 255))
    d.rectangle((20, 20, 1480, 86), fill=blue)
    d.text((50, 36), "F3 四轴覆盖矩阵（精简展示）", font=f_title, fill="white")
    x0, y0 = 70, 130
    colw = [360, 260, 520]
    headers = ["能力子项", "覆盖状态", "对本研究的启示"]
    x = x0
    for w, h in zip(colw, headers):
        d.rectangle((x, y0, x + w, y0 + 48), fill=pale, outline=line, width=2)
        d.text((x + 18, y0 + 12), h, font=f_head, fill=blue)
        x += w
    status_color = {"first-class": green, "partial": orange, "absent": red}
    for i, (name, status) in enumerate(rows):
        y = y0 + 48 + i * 58
        x = x0
        vals = [name, status, "统一到可比较、可消融、可复用的实验入口"]
        for j, val in enumerate(vals):
            d.rectangle((x, y, x + colw[j], y + 58), fill="white", outline=(190, 210, 230), width=1)
            if j == 1:
                d.rounded_rectangle((x + 20, y + 13, x + 190, y + 45), radius=8, fill=status_color[status])
                d.text((x + 38, y + 17), val, font=f_body, fill="white")
            else:
                d.text((x + 18, y + 15), val, font=f_body, fill=(35, 45, 65))
            x += colw[j]
    d.text((70, 730), "结论：覆盖分布不均衡，平台与候选架构服务系统比较，不直接宣称单一最优。", font=f_head, fill=blue)
    im.save(STRICT_ASSET_DIR / "coverage_matrix_strict.png")

    vals = [
        ("Spann3R", 24.8),
        ("CUT3R", 26.2),
        ("Fast3R", 28.5),
        ("DUSt3R", 91.2),
        ("MASt3R", 95.0),
        ("MonST3R", 223.3),
    ]
    im = Image.new("RGB", (1500, 820), "white")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 20, 1480, 800), radius=12, outline=line, width=3, fill=(252, 254, 255))
    d.rectangle((20, 20, 1480, 86), fill=blue)
    d.text((50, 36), "F11 跨模型推理耗时（秒）", font=f_title, fill="white")
    x_label, x_bar, y = 110, 330, 150
    max_v = max(v for _, v in vals)
    for name, val in vals:
        d.text((x_label, y + 8), name, font=f_head, fill=(35, 45, 65))
        bw = int(880 * val / max_v)
        color = orange if val == max_v else (85, 130, 185)
        d.rounded_rectangle((x_bar, y, x_bar + bw, y + 34), radius=8, fill=color)
        d.text((x_bar + bw + 18, y + 3), f"{val:.1f}s", font=f_head, fill=(35, 45, 65))
        y += 78
    d.text((110, 700), "读法：耗时差异用于说明统一调度和可观测记录的必要性，不等同于模型质量排序。", font=f_head, fill=blue)
    im.save(STRICT_ASSET_DIR / "timing_bars_strict.png")


def export_contact_sheet():
    def key(p):
        stem = p.stem
        digits = "".join(ch for ch in stem if ch.isdigit())
        return int(digits) if digits else 0

    imgs = sorted(PREVIEW_DIR.glob("*.png"), key=key)
    thumbs = []
    for p in imgs:
        im = Image.open(p).convert("RGB")
        im.thumbnail((320, 180))
        canvas = Image.new("RGB", (320, 210), "white")
        canvas.paste(im, ((320 - im.width) // 2, 0))
        d = ImageDraw.Draw(canvas)
        d.text((5, 185), p.stem, fill=(0, 0, 0))
        thumbs.append(canvas)
    cols = 4
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 320, rows * 210), "white")
    for i, im in enumerate(thumbs):
        sheet.paste(im, ((i % cols) * 320, (i // cols) * 210))
    sheet.save(CONTACT)


def main():
    make_strict_assets()
    if OUT.exists():
        OUT.unlink()
    if PREVIEW_DIR.exists():
        shutil.rmtree(PREVIEW_DIR)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = True
    pres = app.Presentations.Add()
    for i, (src, _) in enumerate(SLIDES):
        pres.Slides.InsertFromFile(str(TEMPLATE), pres.Slides.Count, src, src)

    # Remove initial blank slide if PowerPoint created one.
    while pres.Slides.Count > len(SLIDES):
        pres.Slides(1).Delete()

    for i, (_, title) in enumerate(SLIDES, start=1):
        slide = pres.Slides(i)
        replace_title(slide, title, i)
        if i in TEXTS:
            fill_texts(slide, TEXTS[i], i)
        if i in IMAGES:
            clear_content_pictures(slide)
            local_asset = STRICT_ASSET_DIR / IMAGES[i]
            ai_asset = ASSET_DIR / IMAGES[i]
            pos = IMAGE_POS.get(i, (90, 130, 780, 330))
            add_image(slide, local_asset if local_asset.exists() else ai_asset, *pos)
        if i == 6:
            add_image(slide, ASSET_DIR / "F04_two_pillars_3840x2160.png", left=235, top=245, width=500, height=220)
        if i == 15:
            add_image(slide, ASSET_DIR / "F13_question_innovation_mapping_3840x2160.png", left=380, top=245, width=500, height=220)
        if i == 18:
            add_image(slide, ASSET_DIR / "F16_research_timeline_gantt_3840x2160.png", left=55, top=140, width=850, height=350)

    pres.SaveAs(str(OUT))
    pres.Export(str(PREVIEW_DIR), "PNG")
    pres.Close()
    app.Quit()
    export_contact_sheet()
    print(OUT)
    print(PREVIEW_DIR)
    print(CONTACT)


if __name__ == "__main__":
    main()
