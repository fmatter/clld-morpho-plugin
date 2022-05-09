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
        # g-words associated with this sentence
        slices = {sl.index: sl for sl in sentence.forms}
        g_shift = 0 # to keep up to date with how many g-words there are in total
        for pwc, (pword, pgloss) in enumerate(
            zip(sentence.analyzed.split("\t"), sentence.gloss.split("\t"))
        ):
            g_words = []
            morphs = []
            glosses = []
            for gwc, (word, gloss) in enumerate(
                zip(pword.split("="), pgloss.split("="))
            ):
                i = pwc + gwc + g_shift
                if gwc > 0:
                    g_shift += 1
                    for glosslist in [g_words, morphs, glosses]:
                        glosslist.append("=")
                if i not in slices:
                    g_words.append(HTML.span(word))
                    morphs.append(HTML.span(word, class_="morpheme"))
                    glosses.append(HTML.span(gloss))
                else:
                    g_words.append(
                        HTML.span(
                            rendered_form(request, slices[i].form, structure=False),
                            name=slices[i].form.id,
                        )
                    )
                    morphs.append(
                        HTML.span(
                            rendered_form(request, slices[i].form),
                            class_="morpheme",
                        )
                    )
                    glosses.append(HTML.span(gloss, **{"class": "gloss"}))
            units.append(
                HTML.div(
                    HTML.div(*g_words),
                    HTML.div(
                        *morphs,
                        class_="morpheme",
                    ),
                    HTML.div(*glosses, **{"class": "gloss"}),
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
                        link(
                            request,
                            form.morph,
                            label=form.morph.name.strip("-"),
                            name=form.morph.id,
                        )
                        for form in ctx.morphs
                    ]
                )
            )
        return literal("&nbsp;")
    return link(request, ctx)
