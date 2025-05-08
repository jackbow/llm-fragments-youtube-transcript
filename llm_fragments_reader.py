import httpx
import llm


@llm.hookimpl
def register_fragment_loaders(register):
    register("reader", reader_loader)


def reader_loader(argument: str) -> llm.Fragment:
    """
    Use Jina Reader to convert a URL to Markdown text.

    Example usage:
      llm -f 'reader:https://simonwillison.net/tags/jina/' ...
    """
    url = "https://r.jina.ai/" + argument
    response = httpx.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to load fragment from {url}: {response.status_code}")
    return llm.Fragment(response.text, url)
