# Copyright 2023 Accent Communications


class HTMLVisualizer:
    def __init__(self, output_filename):
        self._output_filename = output_filename

    _HEADER = """\
<html>
<head>
<title>visualplan</title>
<style type="text/css">
table td {
    border-collapse: collapse;
    border-color: #BBBBBB;
    border-spacing: 0;
    border-style: solid;
    border-width: 0;
    font-family: courier,monospace;
    font-size: 11px;
    padding-left: 0.2em;
    padding-right: 0.2em;
}
tr.noCover {
    background-color: #FFFFFF;
}
tr.coverFull {
    background-color: #DDFFDD;
}
tr.coverNone {
    background-color: #FFDDDD;
}
</style>
</head>
<body>
"""

    _FOOTER = """\
</body>
</html>
"""

    def write(self, analyses):
        with open(self._output_filename, 'w') as fobj:
            fobj.write(self._HEADER)
            for analysis in analyses:
                fobj.write(f'<p>{analysis.filename}</p>')
                fobj.write('<table>')
                for no_line, line_analysis in enumerate(analysis.line_analyses, 1):
                    if line_analysis.is_executable:
                        if line_analysis.is_executed:
                            fobj.write('<tr class="coverFull">')
                        else:
                            fobj.write('<tr class="coverNone">')
                    else:
                        fobj.write('<tr class="noCover">')
                    fobj.write(f'<td>{no_line}</td><td>')
                    fobj.write(line_analysis.content)
                    fobj.write('</td>')
                    fobj.write('</tr>\n')
                fobj.write('</table>')
            fobj.write(self._FOOTER)
        print(f'Wrote HTML output in {self._output_filename}')
