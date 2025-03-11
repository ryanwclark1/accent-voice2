# Copyright 2025 Accent Communications
"""Functions for extracting information from Asterisk PJSIP documentation."""

import asyncio
import logging
from functools import lru_cache
from pathlib import Path
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import httpx

from .models import PJSIPDocumentation, PJSIPOption

# Configure logging
logger = logging.getLogger(__name__)

# Tags to convert to quotes in the text
TAG_TO_QUOTE: list[str] = [
    "emphasis",
    "filename",
    "literal",
    "replaceable",
    "warning",
]


def trim_spaces(s: str) -> str:
    """Turn all kind of white spaces to a single one.

    Args:
        s: The string to process.

    Returns:
        The processed string with normalized whitespace.

    """
    logger.debug(f"Trimming spaces from string of length {len(s)}")
    return " ".join(s.split())


@lru_cache(maxsize=128)
def reformat_block(string: str) -> str:
    """Replace some tags by quotes and remove all other tags.

    Args:
        string: The XML string to process.

    Returns:
        The processed string with quoted elements and removed tags.

    """
    logger.debug(f"Reformatting XML block of length {len(string)}")
    for tag in TAG_TO_QUOTE:
        string = string.replace(f"<{tag}>", '"')
        string = string.replace(f"</{tag}>", '"')

    try:
        elem = ElementTree.fromstring(string)
        string = ElementTree.tostring(elem, encoding="utf-8", method="text").decode(
            "utf-8"
        )
        return trim_spaces(string)
    except ElementTree.ParseError:
        logger.error(f"Failed to parse XML: {string[:100]}...")
        return string


async def extract_para(elem: Element) -> str:
    """Extract text from paragraph elements.

    Args:
        elem: The XML element containing paragraphs.

    Returns:
        A string containing the formatted text from all paragraphs.

    """
    tasks = []
    for para in elem.findall("para"):
        para_str = ElementTree.tostring(para, encoding="utf-8").decode("utf-8")
        tasks.append(asyncio.to_thread(reformat_block, para_str))

    parts = await asyncio.gather(*tasks)
    return "\n".join(parts)


async def extract_node(elem: Element) -> str:
    """Extract note elements from an XML element.

    Args:
        elem: The XML element containing notes.

    Returns:
        A string containing the formatted text from all notes.

    """
    notes = []
    for note in elem.findall("note"):
        notes.append(await extract_para(note))

    return "\n".join(notes)


async def extract_choices(elem: Element) -> dict[str, str]:
    """Extract choices from an XML element.

    Args:
        elem: The XML element containing choices.

    Returns:
        A dictionary mapping choice names to their descriptions.

    """
    choices = {}
    for enum in elem.findall("./*enum"):
        name = enum.attrib["name"]
        if enum.text:
            choices[name] = await extract_para(enum)
        else:
            choices[name] = ""

    return choices


async def extract_pjsip_option(elem: Element) -> PJSIPOption:
    """Extract details about a PJSIP option from an XML element.

    Args:
        elem: The XML element containing option information.

    Returns:
        A PJSIPOption object containing the extracted data.

    """
    synopsis, description, note = "", "", ""
    choices = {}

    for e in elem:
        if e.tag == "synopsis":
            synopsis = trim_spaces(e.text) if e.text else ""
        if e.tag == "description":
            description = await extract_para(e)
            note = await extract_node(e)
            choices = await extract_choices(e)

    return PJSIPOption(
        name=elem.attrib["name"],
        default=elem.attrib.get("default"),
        synopsis=synopsis,
        description=description,
        note=note,
        choices=choices,
    )


async def extract_pjsip_doc_section(elem: Element) -> dict[str, PJSIPOption]:
    """Extract information about a PJSIP documentation section.

    Args:
        elem: The XML element containing section information.

    Returns:
        A dictionary mapping option names to PJSIPOption objects.

    """
    tasks = []
    options = {}

    for option in elem:
        if "name" in option.attrib:
            tasks.append((option.attrib["name"], extract_pjsip_option(option)))

    for name, task in tasks:
        options[name] = await task

    return options


async def extract_pjsip_doc(root: Element) -> dict[str, dict[str, PJSIPOption]]:
    """Extract PJSIP documentation from the XML root element.

    Args:
        root: The XML root element.

    Returns:
        A dictionary mapping section names to dictionaries of options.

    """
    sections = root.findall(".//*[@name='res_pjsip']/configFile/")
    tasks = []
    result = {}

    for section in sections:
        if "name" in section.attrib:
            tasks.append((section.attrib["name"], extract_pjsip_doc_section(section)))

    for name, task in tasks:
        result[name] = await task

    return result


async def load_and_extract_doc(filepath: str | Path) -> PJSIPDocumentation:
    """Load an XML file and extract PJSIP documentation from it.

    Args:
        filepath: Path to the XML file.

    Returns:
        A PJSIPDocumentation object containing the extracted data.

    """
    logger.info(f"Loading XML file: {filepath}")
    try:
        root = ElementTree.parse(filepath).getroot()
        sections = await extract_pjsip_doc(root)
        return PJSIPDocumentation(sections=sections)
    except ElementTree.ParseError:
        logger.error(f"Failed to parse XML file: {filepath}")
        raise
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise


@lru_cache(maxsize=10)
async def fetch_and_extract_doc(url: str) -> PJSIPDocumentation:
    """Fetch an XML file from a URL and extract PJSIP documentation from it.

    Args:
        url: URL of the XML file.

    Returns:
        A PJSIPDocumentation object containing the extracted data.

    """
    logger.info(f"Fetching XML file from URL: {url}")
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        xml_content = response.text

    try:
        root = ElementTree.fromstring(xml_content)
        sections = await extract_pjsip_doc(root)
        return PJSIPDocumentation(sections=sections)
    except ElementTree.ParseError:
        logger.error(f"Failed to parse XML from URL: {url}")
        raise
