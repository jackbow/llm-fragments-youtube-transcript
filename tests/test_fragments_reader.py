from llm_fragments_site_text import site_text_loader

EXAMPLE_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Title element</title>
  <meta charset="utf-8">
  <meta name="author" content="Dan Turkel">
  <meta name="description" content="Meta description">
  <meta property="og:site_name" content="Meta site name" />
  <meta property="og:title" content="Meta title" />
  <meta property="article:published_time" content="2025-03-10" />
</head>
<body>
<h2 id="title">H2 element</h2>
<p>A <em>sample</em> paragraph. <code>Code</code></p>
<p>Here's a <a href="/foo.html">link</a></p>
</body>
</html>"""


def test_site_text_loader(httpx_mock):
    httpx_mock.add_response(
        url="https://test_site.com/",
        method="GET",
        text=EXAMPLE_HTML,
    )
    fragment = site_text_loader("https://test_site.com/")
    example_output = """Site: Meta site name
Title: Meta title
Author: Dan Turkel
Date: 2025-03-10
Description: Meta description

A *sample* paragraph. `Code`

Here's a [link](/foo.html)"""
    assert str(fragment) == example_output
    assert fragment.source == "https://test_site.com/"
