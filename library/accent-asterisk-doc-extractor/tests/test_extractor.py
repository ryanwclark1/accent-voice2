# Copyright 2025 Accent Communications
"""Tests for the Asterisk PJSIP documentation extractor."""

import asyncio
import pytest
from pathlib import Path
from xml.etree import ElementTree

from accent_asterisk_doc_extractor.extractor import (
    trim_spaces,
    reformat_block,
    extract_para,
    extract_pjsip_doc,
)

# Sample XML for testing
SAMPLE_XML = """
<docs>
  <application name="res_pjsip">
    <configFile name="pjsip.conf">
      <configObject name="endpoint">
        <synopsis>An endpoint.</synopsis>
        <configOption name="100rel">
          <synopsis>100rel mode</synopsis>
          <description>
            <para>Mode of operation for SIP 100rel.</para>
            <note>This note is about 100rel.</note>
            <enumlist>
              <enum name="yes">
                <para>Require 100rel</para>
              </enum>
              <enum name="no">
                <para>Do not support 100rel</para>
              </enum>
            </enumlist>
          </description>
        </configOption>
      </configObject>
    </configFile>
  </application>
</docs>
"""


def test_trim_spaces():
    """Test that whitespace is properly normalized."""
    assert trim_spaces("  a  b  c  ") == "a b c"
    assert trim_spaces("a\nb\tc") == "a b c"


def test_reformat_block():
    """Test that XML blocks are properly reformatted."""
    input_str = "<para>This is <emphasis>important</emphasis> text.</para>"
    expected = 'This is "important" text.'
    assert reformat_block(input_str) == expected


@pytest.mark.asyncio
async def test_extract_para():
    """Test that paragraphs are properly extracted."""
    xml = ElementTree.fromstring(
        "<root><para>First paragraph</para><para>Second paragraph</para></root>"
    )
    result = await extract_para(xml)
    assert result == "First paragraph\nSecond paragraph"


@pytest.mark.asyncio
async def test_extract_pjsip_doc():
    """Test that PJSIP documentation is properly extracted."""
    root = ElementTree.fromstring(SAMPLE_XML)
    result = await extract_pjsip_doc(root)

    assert "endpoint" in result
    assert "100rel" in result["endpoint"]
    assert result["endpoint"]["100rel"].synopsis == "100rel mode"
    assert "yes" in result["endpoint"]["100rel"].choices
