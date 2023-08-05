import re
import unicodedata

MANGLE_DELIM = "X"

normalizes_to_underscore = "_︳︴﹍﹎﹏＿"


def mangle(s):
    """Stringify the argument (with :class:`str`, not :func:`repr` or
    :hy:func:`hy.repr`) and convert it to a valid Python identifier according
    to :ref:`Hy's mangling rules <mangling>`. ::

        (hy.mangle 'foo-bar)   ; => "foo_bar"
        (hy.mangle "🦑")       ; => "hyx_squid"

    If the stringified argument is already both legal as a Python identifier
    and normalized according to Unicode normalization form KC (NFKC), it will
    be returned unchanged. Thus, ``hy.mangle`` is idempotent. ::

        (setv x '♦-->♠)
        (= (hy.mangle (hy.mangle x)) (hy.mangle x))  ; => True

    Generally, the stringifed input is expected to be parsable as a symbol. As
    a convenience, it can also have the syntax of a :ref:`dotted identifier
    <dotted-identifiers>`, and ``hy.mangle`` will mangle the dot-delimited
    parts separately. ::

        (hy.mangle "a.c!.d")  ; => "a.hyx_cXexclamation_markX.d"
    """

    assert s
    s = str(s)

    if "." in s and s.strip("."):
        return ".".join(mangle(x) if x else "" for x in s.split("."))

    # Remove and save leading underscores
    s2 = s.lstrip(normalizes_to_underscore)
    leading_underscores = "_" * (len(s) - len(s2))
    s = s2

    # Convert hyphens without introducing a new leading underscore
    s = s[0] + s[1:].replace("-", "_") if s else s

    # Convert invalid characters or reserved words
    if not (leading_underscores + s).isidentifier():
        # Replace illegal characters with their Unicode character
        # names, or hexadecimal if they don't have one.
        s = "hyx_" + "".join(
            c if c != MANGLE_DELIM and ("S" + c).isidentifier()
            # We prepend the "S" because some characters aren't
            # allowed at the start of an identifier.
            else "{0}{1}{0}".format(
                MANGLE_DELIM,
                unicodedata.name(c, "").lower().replace("-", "H").replace(" ", "_")
                or "U{:x}".format(ord(c)),
            )
            for c in s
        )

    # Step 5: Add back leading underscores
    s = leading_underscores + s

    # Normalize Unicode per PEP 3131.
    s = unicodedata.normalize("NFKC", s)

    assert s.isidentifier()
    return s


def unmangle(s):
    """Stringify the argument and try to convert it to a pretty unmangled
    form. See :ref:`Hy's mangling rules <mangling>`.

    Unmangling may not round-trip, because different Hy symbol names can mangle
    to the same Python identifier. In particular, Python itself already
    considers distinct strings that have the same normalized form (according to
    NFKC), such as ``hello`` and ``𝔥𝔢𝔩𝔩𝔬``, to be the same identifier.

    Examples:
      ::

         => (hy.unmangle 'foo_bar)
         "foo-bar"

         => (hy.unmangle 'hyx_XasteriskX)
         "*"

         => (hy.unmangle 'hyx_XhyphenHminusX_XgreaterHthan_signX)
         "-->"

         => (hy.unmangle 'hyx_XlessHthan_signX__)
         "<--"

         => (hy.unmangle '__dunder_name__)
         "__dunder-name__"

    """

    s = str(s)

    prefix = ""
    suffix = ""
    m = re.fullmatch(r"(_+)(.*?)(_*)", s, re.DOTALL)
    if m:
        prefix, s, suffix = m.groups()

    if s.startswith("hyx_"):
        s = re.sub(
            "{0}(U)?([_a-z0-9H]+?){0}".format(MANGLE_DELIM),
            lambda mo: chr(int(mo.group(2), base=16))
            if mo.group(1)
            else unicodedata.lookup(
                mo.group(2).replace("_", " ").replace("H", "-").upper()
            ),
            s[len("hyx_") :],
        )
    s = s.replace("_", "-")

    return prefix + s + suffix
