from llm.plugins import pm
from llm_fragments_reader import reader_loader


def test_reader_loader(httpx_mock):
    example_text = '# Example Title\n\nExample content.'
    httpx_mock.add_response(
        url="https://r.jina.ai/https://example.com/",
        method="GET",
        text=example_text,
    )
    fragment = reader_loader("https://example.com/")
    assert str(fragment) == example_text
    assert fragment.source == "https://r.jina.ai/https://example.com/"
