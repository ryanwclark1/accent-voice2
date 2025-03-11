# Copyright 2025 Accent Communications
"""Command-line interface for Asterisk PJSIP documentation extractor."""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

from .extractor import load_and_extract_doc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def async_main(file_path: Path, output_file: Path | None = None) -> None:
    """Extract PJSIP documentation from an XML file and output as JSON.

    Args:
        file_path: Path to the XML file.
        output_file: Path to write the output JSON file. If None, prints to stdout.

    """
    try:
        doc = await load_and_extract_doc(file_path)
        json_data = json.dumps(doc.model_dump(), indent=2)

        if output_file:
            output_file.write_text(json_data)
            logger.info(f"Output written to {output_file}")
        else:
            print(json_data)

    except Exception as e:
        logger.error(f"Error processing file: {e}")
        sys.exit(1)


def main() -> None:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description="Extract documentation from Asterisk PJSIP XML files"
    )
    parser.add_argument("file", help="Path to the XML file")
    parser.add_argument(
        "-o", "--output", help="Path to write output JSON file (default: stdout)"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    file_path = Path(args.file)
    output_path = Path(args.output) if args.output else None

    asyncio.run(async_main(file_path, output_path))


if __name__ == "__main__":
    main()
