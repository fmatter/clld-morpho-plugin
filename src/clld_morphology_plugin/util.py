import re
from clld.web.util.helpers import link
from clld.web.util.htmllib import HTML
from clld.web.util.htmllib import literal


GLOSS_ABBR_PATTERN = re.compile(
    "(?P<personprefix>1|2|3)?(?P<abbr>[A-Z]+)(?P<personsuffix>1|2|3)?(?=([^a-z]|$))"
)


def get_further_lexemes(lexeme):
    lex_list = [lexeme]
    for lex in lexeme.derived_lexemes:
        lex_list.extend(get_further_lexemes(lex.derived_lexeme))
    return lex_list


def rendered_gloss_units(request, sentence):  # pylint: disable=too-many-locals
    units = []
    if sentence.analyzed and sentence.gloss:
        # g-words associated with this sentence
        slices = {sl.index: sl for sl in sentence.forms}
        g_shift = 0  # to keep up to date with how many g-words there are in total
        for pwc, (pword, pgloss) in enumerate(
            zip(sentence.analyzed.split("\t"), sentence.gloss.split("\t"))
        ):
            g_words = []
            morphs = []
            glosses = []
            posses = []
            for gwc, (word, gloss) in enumerate(
                zip(pword.split("="), pgloss.split("="))
            ):
                i = pwc + gwc + g_shift
                if gwc > 0:
                    g_shift += 1
                    for glosslist in [g_words, morphs, glosses, posses]:
                        glosslist.append("=")
                if i not in slices:
                    g_words.append(HTML.span(word))
                    morphs.append(HTML.span(word, class_="morpheme"))
                    glosses.append(HTML.span(gloss))
                    posses.append(HTML.span("*"))
                else:
                    g_words.append(
                        HTML.span(
                            rendered_form(request, slices[i].form, structure=False),
                            name=slices[i].form.id,
                        )
                    )
                    morphs.append(
                        HTML.span(
                            rendered_form(request, slices[i].form), class_="morpheme"
                        )
                    )
                    glosses.append(HTML.span(gloss, **{"class": "gloss"}))
                    if slices[i].form.pos:
                        posses.append(
                            HTML.span(
                                link(
                                    request,
                                    slices[i].form.pos,
                                    label=slices[i].form.pos.id,
                                ),
                                **{"class": "pos"},
                            )
                        )
                    else:
                        posses.append(HTML.span("*"))
            if posses[0] == HTML.span("*"):
                interlinear_div = HTML.div(
                    HTML.div(*g_words),
                    HTML.div(*morphs, class_="morpheme"),
                    HTML.div(*glosses, **{"class": "gloss"}),
                    class_="gloss-unit",
                )
            else:
                interlinear_div = HTML.div(
                    HTML.div(*g_words),
                    HTML.div(*morphs, class_="morpheme"),
                    HTML.div(*glosses, **{"class": "gloss"}),
                    HTML.div(*posses),
                    class_="gloss-unit",
                )
            units.append(
                interlinear_div
            )
    return units


morph_separators = ["-", "~", "<", ">"]
sep_pattern = f"([{''.join(morph_separators)}])"


def rendered_form(request, form, structure=True):
    if structure:
        if form.morphs != []:
            form_output = []
            p_c = -1
            s_c = 0
            for part in re.split(sep_pattern, form.segmented):
                if part in morph_separators:
                    form_output.append(part)
                else:
                    p_c += 1
                    if len(form.morphs) > s_c and p_c == form.morphs[s_c].index:
                        form_output.append(
                            link(
                                request,
                                form.morphs[s_c].morph.morpheme,
                                label=form.morphs[s_c].morph.name.strip("-"),
                                name=form.morphs[s_c].morph.id
                                + "-"
                                + form.morphs[s_c].morpheme_meaning.id,
                            )
                        )
                        s_c += 1
                    else:
                        form_output.append(part)
            return literal("".join(form_output))
        return literal("&nbsp;")
    return link(request, form)
