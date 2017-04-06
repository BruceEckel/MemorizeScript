from pathlib import Path
import click

def process_line(line, character):
    if not line.strip():
        return ""
    if not line.startswith(character):
        return '<h3>' + line + '</h3>\n'
    line = strip_parens(line)
    words = line.split()
    result = words[0] + " "
    for word in words[1:]:
        result += compress_word(word)
    return '<h3 class="hintcode">' + \
        result + '&nbsp;&nbsp;' + \
        '<span class="hinttooltip" style="display: none;">' + \
        " ".join(words[1:]) + \
        '</span></h3>\n'

def strip_parens(line):
    """
    >>> print(strip_parens("(pop)foobar(baz)foo bar (baz) bingo(baz)"))
    foobarfoo bar  bingo
    """
    while '(' in line:
        assert ')' in line
        start = line.find('(')
        end = line.find(')')
        line = line[:start] + line[end+1:]
    return line

def compress_word(word):
    result = ""
    word = word.strip()
    if '-' in word:
        for phrase in word.split('-'):
            result += compress(phrase) + '-'
        return result[:-1]
    return compress(word)

def compress(phrase):
    found_first_char = False
    result = ""
    for char in phrase:
        if char.isalnum():
            if not found_first_char:
                result += char
                found_first_char = True
        else:
            if char not in "'":
                result += char # Retain punctuation
    return result

hint_javascript = """
<script language="JavaScript">
window.addEventListener("load", function () {
    var hintcodes = document.getElementsByClassName("hintcode");
    for (var i = 0; i < hintcodes.length; i++) {
        hintcodes[i].addEventListener("mouseover", function () {
            var hinttooltip = this.getElementsByClassName("hinttooltip")[0];
            hinttooltip.removeAttribute("style");
            hinttooltip.style.background = "yellow";
        });
        hintcodes[i].addEventListener("mouseout", function () {
            var hinttooltip = this.getElementsByClassName("hinttooltip")[0];
            hinttooltip.style.display = "none";
        });
    }
});
</script>
</body>
</html>
"""

@click.command(context_settings = {
  "help_option_names" : ['-h', '--help'],
})
@click.argument('script', type = click.Path(exists=True))
@click.argument('character', type = str)
def memorize_script(script, character):
    """
    \b
    The first argument is the file name of the plain-text script.
    The second argument is the character whose lines you want to memorize.
    """
    result = "<html>\n<body>\n"
    for line in Path(script).read_text().splitlines():
        result += process_line(line, character)
    ModifiedScript = Path(script).stem + "-" + character + ".html"
    Path(ModifiedScript).write_text(result + hint_javascript)
    print("Created " + ModifiedScript)

if __name__ == '__main__':
    print("For help: python MemorizeScript.py -h")
    memorize_script()
