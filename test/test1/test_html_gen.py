from src.test1.html_gen import HTML


def test_html_sample():
    html = HTML()
    with html.body():
        with html.div():
            with html.div():
                html.p("Первая строка.")
                html.p("Вторая строка.")
            with html.div():
                html.p("Третья строка.")
    assert (
        html.generate()
        == """<body>
    <div>
        <div>
            <p>Первая строка.</p>
            <p>Вторая строка.</p>
        </div>
        <div>
            <p>Третья строка.</p>
        </div>
    </div>
</body>
"""
    )


def test_html_with_attrs():
    html = HTML()
    with html.html():
        with html.body():
            html.a("Click me", href="#")

    assert html.generate(False) == '<html><body><a href="#">Click me</a></body></html>'


def test_html_escape_attrs():
    html = HTML()
    html.img(src="/image.jpg", alt='Beautiful image of "████"')

    assert html.generate(False) == '<img src="/image.jpg" alt="Beautiful image of &quot;████&quot;">'
