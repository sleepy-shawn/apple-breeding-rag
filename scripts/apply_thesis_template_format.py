from __future__ import annotations

import re
import shutil
import tempfile
import zipfile
from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path("/Users/shuaige/code/apple-breeding-rag")
THESIS = ROOT / "thesis" / "葛帅毕业论文.docx"
TEMPLATE = ROOT / "thesis" / "附件1.西北农林科技大学本科毕业论文（设计）模板.docx"
OUTPUT = ROOT / "thesis" / "葛帅毕业论文_附件1格式定稿.docx"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
XML = "http://www.w3.org/XML/1998/namespace"
NS = {"w": W, "r": R}

ET.register_namespace("w", W)
ET.register_namespace("r", R)


def qn(ns: str, name: str) -> str:
    return f"{{{ns}}}{name}"


def wtag(name: str) -> str:
    return qn(W, name)


def paragraph_text(p: ET.Element) -> str:
    return "".join(t.text or "" for t in p.findall(".//w:t", NS)).strip()


def first_text_node(p: ET.Element) -> ET.Element | None:
    return p.find(".//w:t", NS)


def set_paragraph_text(p: ET.Element, text: str) -> None:
    texts = p.findall(".//w:t", NS)
    if not texts:
        r = ET.SubElement(p, wtag("r"))
        t = ET.SubElement(r, wtag("t"))
        t.text = text
        return
    texts[0].text = text
    for t in texts[1:]:
        t.text = ""


def ppr(p: ET.Element) -> ET.Element:
    existing = p.find("w:pPr", NS)
    if existing is not None:
        return existing
    created = ET.Element(wtag("pPr"))
    p.insert(0, created)
    return created


def set_pstyle(p: ET.Element, style_id: str) -> None:
    props = ppr(p)
    style = props.find("w:pStyle", NS)
    if style is None:
        style = ET.Element(wtag("pStyle"))
        props.insert(0, style)
    style.set(wtag("val"), style_id)


def get_pstyle(p: ET.Element) -> str | None:
    style = p.find("w:pPr/w:pStyle", NS)
    return style.get(wtag("val")) if style is not None else None


def make_run(text: str) -> ET.Element:
    r_el = ET.Element(wtag("r"))
    t_el = ET.SubElement(r_el, wtag("t"))
    if text.startswith(" ") or text.endswith(" "):
        t_el.set(qn(XML, "space"), "preserve")
    t_el.text = text
    return r_el


def make_field_paragraph(instruction: str, placeholder: str) -> ET.Element:
    p = ET.Element(wtag("p"))
    r_begin = ET.SubElement(p, wtag("r"))
    fld_begin = ET.SubElement(r_begin, wtag("fldChar"))
    fld_begin.set(wtag("fldCharType"), "begin")

    r_instr = ET.SubElement(p, wtag("r"))
    instr = ET.SubElement(r_instr, wtag("instrText"))
    instr.set(qn(XML, "space"), "preserve")
    instr.text = instruction

    r_sep = ET.SubElement(p, wtag("r"))
    fld_sep = ET.SubElement(r_sep, wtag("fldChar"))
    fld_sep.set(wtag("fldCharType"), "separate")

    p.append(make_run(placeholder))

    r_end = ET.SubElement(p, wtag("r"))
    fld_end = ET.SubElement(r_end, wtag("fldChar"))
    fld_end.set(wtag("fldCharType"), "end")
    return p


def make_heading(text: str, style_id: str = "1") -> ET.Element:
    p = ET.Element(wtag("p"))
    set_pstyle(p, style_id)
    p.append(make_run(text))
    return p


def make_blank_with_sectpr(sect_pr: ET.Element | None) -> ET.Element:
    p = ET.Element(wtag("p"))
    if sect_pr is not None:
        props = ppr(p)
        props.append(deepcopy(sect_pr))
    return p


def iter_body_paragraphs(body: ET.Element) -> list[ET.Element]:
    return [child for child in list(body) if child.tag == wtag("p")]


def find_paragraph(body: ET.Element, predicate) -> ET.Element | None:
    for p in iter_body_paragraphs(body):
        if predicate(paragraph_text(p)):
            return p
    return None


def paragraph_index(body: ET.Element, target: ET.Element) -> int:
    for index, child in enumerate(list(body)):
        if child is target:
            return index
    raise ValueError("paragraph is not a direct body child")


def normalize_heading_texts(body: ET.Element) -> None:
    replacements = {
        "检索增强生成（RAG）原理": "2.1 检索增强生成（RAG）原理",
        "向量数据库与语义检索": "2.2 向量数据库与语义检索",
        "大语言模型接口": "2.3 大语言模型接口",
        "苹果育种相关知识背景": "2.4 苹果育种相关知识背景",
        "知识库整体设计": "3.1 知识库整体设计",
        "论文数据的获取和处理": "3.2 论文数据的获取和处理",
        "目 录": "目次",
        "目录": "目次",
    }
    full_width_digits = str.maketrans("０１２３４５６７８９", "0123456789")

    for p in iter_body_paragraphs(body):
        text = paragraph_text(p)
        if not text:
            continue
        if text in replacements:
            set_paragraph_text(p, replacements[text])
            continue
        normalized = text.translate(full_width_digits)
        if re.match(r"^第\d+章\s+", normalized) and normalized != text:
            set_paragraph_text(p, normalized)


def insert_missing_structural_headings(body: ET.Element) -> None:
    english_title = find_paragraph(
        body,
        lambda text: text.startswith(
            "An Intelligent Question-Answering System for Apple Breeding Knowledge"
        ),
    )
    has_abstract = find_paragraph(body, lambda text: text == "ABSTRACT") is not None
    if english_title is not None and not has_abstract:
        body.insert(paragraph_index(body, english_title), make_heading("ABSTRACT", "1"))

    chapter4_anchor = find_paragraph(body, lambda text: text.startswith("4.1 系统总体架构"))
    has_chapter4 = find_paragraph(body, lambda text: text.startswith("第4章")) is not None
    if chapter4_anchor is not None and not has_chapter4:
        body.insert(paragraph_index(body, chapter4_anchor), make_heading("第4章 系统设计与实现", "1"))


def replace_toc_block(body: ET.Element) -> None:
    toc = find_paragraph(body, lambda text: text == "目次")
    chapter1 = find_paragraph(body, lambda text: text.startswith("第1章"))
    if toc is None or chapter1 is None:
        return

    children = list(body)
    start = paragraph_index(body, toc) + 1
    end = paragraph_index(body, chapter1)
    sect_pr = None
    for child in children[start:end]:
        candidate = child.find("w:pPr/w:sectPr", NS) if child.tag == wtag("p") else None
        if candidate is not None:
            sect_pr = deepcopy(candidate)

    for child in children[start:end]:
        body.remove(child)

    insert_at = paragraph_index(body, chapter1)
    body.insert(insert_at, make_blank_with_sectpr(sect_pr))
    body.insert(insert_at, make_field_paragraph('TOC \\o "1-3" \\h \\z \\u', "右键更新目录"))


def style_document(body: ET.Element) -> None:
    in_references = False
    in_biography = False
    source_to_template = {
        "10": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "a3": "a",
        "a4": "afd",
        "a6": "affa",
        "ae": "afff",
        "af": "afff0",
        "af0": "afff1",
        "TableParagraph": "afff5",
    }

    for p in iter_body_paragraphs(body):
        text = paragraph_text(p)
        if not text:
            continue

        original_style = get_pstyle(p)
        if original_style in source_to_template:
            set_pstyle(p, source_to_template[original_style])

        if text == "参考文献":
            in_references = True
            set_pstyle(p, "1")
            continue
        if text in {"致谢", "作者简历"}:
            in_references = False
            in_biography = text == "作者简历"
            set_pstyle(p, "1")
            continue
        if in_references:
            set_pstyle(p, "affc")
            continue
        if in_biography:
            set_pstyle(p, "a")
            continue

        if text in {
            "本科生毕业论文(设计)的原创性声明",
            "本科生毕业论文(设计)的使用授权说明",
        }:
            set_pstyle(p, "affe")
        elif text in {"摘要", "ABSTRACT", "目次"}:
            set_pstyle(p, "1")
        elif re.match(r"^第\d+章\s+", text):
            set_pstyle(p, "1")
        elif re.match(r"^\d+\.\d+\.\d+\.\d+\s*", text):
            set_pstyle(p, "4")
        elif re.match(r"^\d+\.\d+\.\d+\s*", text):
            set_pstyle(p, "3")
        elif re.match(r"^\d+\.\d+\s*", text):
            set_pstyle(p, "2")
        elif text.startswith(("关键词", "KEY WORDS", "Key words")):
            set_pstyle(p, "afff8")
        elif re.match(r"^(图\s*\d+\s*[-－]\s*\d+(?:\s|$)|表\s*\d+\s*[-－]\s*\d+(?:\s|$)|Table\s+\d)", text):
            set_pstyle(p, "afff1")
        elif text.startswith(
            (
                "基于RAG方法的苹果育种专业知识问答系统及Web实现",
                "RAG-Based Apple Breeding Domain Knowledge",
                "An Intelligent Question-Answering System",
            )
        ):
            set_pstyle(p, "afd")
        elif original_style in {"a3", None} and len(text) > 20:
            set_pstyle(p, "a")


def extract_template_page_geometry() -> tuple[ET.Element | None, ET.Element | None]:
    with zipfile.ZipFile(TEMPLATE) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    sect = root.find(".//w:sectPr", NS)
    if sect is None:
        return None, None
    return deepcopy(sect.find("w:pgSz", NS)), deepcopy(sect.find("w:pgMar", NS))


def apply_page_geometry(root: ET.Element) -> None:
    pg_sz, pg_mar = extract_template_page_geometry()
    if pg_sz is None and pg_mar is None:
        return
    for sect in root.findall(".//w:sectPr", NS):
        for tag, replacement in (("pgSz", pg_sz), ("pgMar", pg_mar)):
            if replacement is None:
                continue
            existing = sect.find(f"w:{tag}", NS)
            if existing is not None:
                sect.remove(existing)
            sect.insert(0, deepcopy(replacement))


def enable_update_fields(settings_path: Path) -> None:
    root = ET.parse(settings_path).getroot()
    update_fields = root.find("w:updateFields", NS)
    if update_fields is None:
        update_fields = ET.SubElement(root, wtag("updateFields"))
    update_fields.set(wtag("val"), "true")
    ET.ElementTree(root).write(settings_path, encoding="UTF-8", xml_declaration=True)


def copy_template_format_parts(tmp_dir: Path) -> None:
    with zipfile.ZipFile(TEMPLATE) as zf:
        for member in ("word/styles.xml", "word/fontTable.xml", "word/theme/theme1.xml"):
            target = tmp_dir / member
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(zf.read(member))


def rewrite_document_xml(tmp_dir: Path) -> None:
    document_path = tmp_dir / "word" / "document.xml"
    root = ET.parse(document_path).getroot()
    body = root.find("w:body", NS)
    if body is None:
        raise RuntimeError("word/document.xml has no body")

    normalize_heading_texts(body)
    insert_missing_structural_headings(body)
    normalize_heading_texts(body)
    replace_toc_block(body)
    style_document(body)
    apply_page_geometry(root)

    ET.ElementTree(root).write(document_path, encoding="UTF-8", xml_declaration=True)


def repack_docx(tmp_dir: Path, output: Path) -> None:
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(tmp_dir.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(tmp_dir).as_posix())


def main() -> None:
    if not THESIS.exists():
        raise FileNotFoundError(THESIS)
    if not TEMPLATE.exists():
        raise FileNotFoundError(TEMPLATE)

    with tempfile.TemporaryDirectory() as td:
        tmp_dir = Path(td)
        with zipfile.ZipFile(THESIS) as zf:
            zf.extractall(tmp_dir)
        copy_template_format_parts(tmp_dir)
        rewrite_document_xml(tmp_dir)
        enable_update_fields(tmp_dir / "word" / "settings.xml")
        repack_docx(tmp_dir, OUTPUT)

    print(OUTPUT)


if __name__ == "__main__":
    main()
