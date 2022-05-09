import re
from clld.web.util.helpers import link
from clld.web.util.htmllib import HTML
from clld.web.util.htmllib import literal


GLOSS_ABBR_PATTERN = re.compile(
    "(?P<personprefix>1|2|3)?(?P<abbr>[A-Z]+)(?P<personsuffix>1|2|3)?(?=([^a-z]|$))"
)


def rendered_gloss_units(request, sentence):
    units = []
    if sentence.analyzed and sentence.gloss:
        slices = {sl.index: sl for sl in sentence.forms}
        for pwc, (pword, pgloss) in enumerate(
            zip(sentence.analyzed.split("\t"), sentence.gloss.split("\t"))
        ):
            gwc = 0
            prefix = ""
            shift = 0
            g_words = re.split("(=)",pword)
            g_glosses = re.split("(=)",pgloss)
            while gwc < len(g_words):
                word = g_words[gwc]
                gloss = g_glosses[gwc]
                i = pwc + gwc + shift
                gwc += 1
                if word == "=":
                    prefix = "="
                    shift -= 1
                    continue
                if i not in slices:
                    units.append(
                        HTML.div(
                            HTML.div(prefix+word),
                            HTML.div(word, class_="morpheme"),
                            HTML.div(gloss, **{"class": "gloss"}),
                            class_="gloss-unit",
                        )
                    )
                else:
                    units.append(
                        HTML.div(
                            HTML.div(
                                prefix+rendered_form(request, slices[i].form, structure=False), name=slices[i].form.id
                            ),
                            HTML.div(
                                rendered_form(request, slices[i].form),
                                class_="morpheme",
                            ),
                            HTML.div(gloss, **{"class": "gloss"}),
                            class_="gloss-unit",
                        )
                    )
    return units


def rendered_form(request, ctx, structure=True):
    if structure:
        if ctx.morphs != []:
            return literal(
                "-".join(
                    [
                        link(request, form.morph, label=form.morph.name.strip("-"), name=form.morph.id)
                        for form in ctx.morphs
                    ]
                )
            )
        return literal("&nbsp;")
    return link(request, ctx)