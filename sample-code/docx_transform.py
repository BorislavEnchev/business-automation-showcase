"""
AutoMate — DOCX Template Transformation Engine (Simplified)

Demonstrates the OOXML transformation approach used to fill legal document
templates with extracted data. The full production implementation handles
multiple document types, bilingual layout, rich text, and table manipulation.

Key Insight: A .docx file is a ZIP archive containing XML files.
We parse the XML, transform paragraphs, and re-zip.
"""

import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Any, Callable

# OOXML namespace — every element in the document XML uses this
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"
NS = {"w": WORD_NS}
W = f"{{{WORD_NS}}}"


# ── Helper Functions ──

def get_paragraph_text(paragraph: ET.Element) -> str:
    """Extract the full text content of a paragraph (all <w:t> elements)."""
    return "".join(
        node.text or ""
        for node in paragraph.findall(".//w:t", NS)
    )


def set_paragraph_text(paragraph: ET.Element, new_text: str) -> None:
    """Replace all text in a paragraph with a single run of new text."""
    # Remove existing text runs
    for child in list(paragraph):
        if child.tag == f"{W}r":
            paragraph.remove(child)
    
    # Add a single new run with the replacement text
    run = ET.SubElement(paragraph, f"{W}r")
    text_elem = ET.SubElement(run, f"{W}t")
    text_elem.text = new_text
    if new_text.startswith(" ") or new_text.endswith(" "):
        text_elem.set(f"{{{XML_NS}}}space", "preserve")


def set_rich_text(paragraph: ET.Element, segments: list[tuple[str, bool]]) -> None:
    """
    Set paragraph text with mixed bold/normal formatting.
    
    Each segment is (text, is_bold):
        set_rich_text(p, [
            ("Label: ", False),
            ("Bold Value", True),
            (" normal text ", False),
        ])
    """
    # Remove existing runs
    for child in list(paragraph):
        if child.tag == f"{W}r":
            paragraph.remove(child)
    
    for text, is_bold in segments:
        run = ET.SubElement(paragraph, f"{W}r")
        
        # Formatting properties
        rpr = ET.SubElement(run, f"{W}rPr")
        if is_bold:
            ET.SubElement(rpr, f"{W}b")
            ET.SubElement(rpr, f"{W}bCs")
        
        # Text content
        t = ET.SubElement(run, f"{W}t")
        if text.startswith(" ") or text.endswith(" "):
            t.set(f"{{{XML_NS}}}space", "preserve")
        t.text = text


# ── Transform Pipeline ──

DocumentTransform = Callable[[str, dict[str, Any], set[str]], str]
"""
Signature for document-specific text transformation functions.

Args:
    text: The original paragraph text from the template
    context: Merged person + company data for filling
    missing_fields: Set to add field names that couldn't be resolved

Returns:
    The transformed paragraph text (or original if no match)
"""


def render_docx_template(
    template_path: Path,
    output_path: Path,
    context: dict[str, Any],
    transforms: dict[str, DocumentTransform],
) -> list[str]:
    """
    Open a .docx template, apply paragraph-level transformations,
    and save the filled result.
    
    Args:
        template_path: Path to the source .docx template
        output_path: Path to write the filled .docx
        context: Person + company data for template filling
        transforms: Dict mapping template names to transform functions
        
    Returns:
        List of field names that couldn't be filled (missing data)
    """
    missing_fields: set[str] = set()
    
    # Step 1: Open the .docx as a ZIP
    with zipfile.ZipFile(template_path, "r") as source_zip:
        # Step 2: Read the main document XML
        xml_bytes = source_zip.read("word/document.xml")
        root = ET.fromstring(xml_bytes)
        
        # Step 3: Apply transforms to each paragraph
        for paragraph in root.findall(".//w:p", NS):
            original = get_paragraph_text(paragraph)
            
            # Find the right transform for this template
            transform = transforms.get(template_path.name)
            if transform:
                updated = transform(original, context, missing_fields)
                if updated != original:
                    set_paragraph_text(paragraph, updated)
        
        # Step 4: Convert back to XML bytes
        updated_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        
        # Step 5: Re-zip with the modified document.xml
        with zipfile.ZipFile(
            output_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as output_zip:
            for item in source_zip.infolist():
                data = (
                    updated_xml
                    if item.filename == "word/document.xml"
                    else source_zip.read(item.filename)
                )
                output_zip.writestr(item, data)
    
    return sorted(missing_fields)


# ── Example Transform ──

def employment_contract_transform(
    text: str,
    context: dict[str, Any],
    missing_fields: set[str],
) -> str:
    """
    Transform paragraphs in an employment contract template.
    
    Matches paragraph text using case-insensitive comparison,
    then injects the appropriate data from context.
    """
    normalized = re.sub(r"\s+", " ", text).strip().lower()
    
    if normalized.startswith("днес,"):
        return f"Днес, {context['today']}, в град {context['city']} между:"
    
    if "наричано по-долу" in normalized and "клиент" in normalized:
        company_name = str(context.get("company", {}).get("name") or "")
        if not company_name:
            missing_fields.add("company_name")
            company_name = "[MISSING: company_name]"
        return f"2. {company_name}, наричано по-долу „Клиент\","
    
    if normalized.startswith("дата:"):
        return f"дата: {context['today']}"
    
    if normalized.startswith("гр."):
        city = str(context.get("company", {}).get("city") or context.get("city") or "")
        return f"гр. {city}"
    
    # No match — return original text unchanged
    return text


"""
Usage Example:

    person = { "first_name": "John", "last_name": "Doe", ... }
    company = { "name": "ACME Corp", "city": "Sofia", ... }
    context = {
        "person": person,
        "company": company,
        "today": "15.01.2024",
        "city": "Sofia",
    }
    
    transforms = {
        "Employment Contract.docx": employment_contract_transform,
    }
    
    missing = render_docx_template(
        Path("template.docx"),
        Path("output.docx"),
        context,
        transforms,
    )
"""
