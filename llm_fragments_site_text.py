import re

import httpx
import llm
from trafilatura import extract, extract_metadata


@llm.hookimpl
def register_fragment_loaders(register):
    register("site", site_text_loader)


def site_text_loader(argument: str) -> llm.Fragment:
    """
    Use Trafilatura to convert a website into plain text.

    Example usage:
      llm -f 'site:https://danturkel.com/2025/03/10/ignite-machine-understanding-vectors.html' ...
    """
    html = httpx.get(argument).text
    text: str = extract(
        html, output_format="markdown", include_links=True, favor_precision=True
    )  # type: ignore
    metadata = extract_metadata(html)
    result = []
    if text is None:
        raise ValueError("No text found")
    if metadata.sitename:
        result.append(f"Site: {metadata.sitename}")
    if metadata.title:
        result.append(f"Title: {metadata.title}")
    if metadata.author:
        result.append(f"Author: {metadata.author}")
    if metadata.date:
        result.append(f"Date: {metadata.date}")
    if metadata.description:
        result.append(f"Description: {metadata.description}")
    result.append("\n" + text)
    # ensure there's no gratuitous newlines
    result_string = re.sub(r"\n{3,}", "\n\n", "\n".join(result))

    return llm.Fragment(result_string, source=argument)
