import re
from clld.db.meta import DBSession
from clld.db.models import common as models
from clld.web.util.helpers import link
from clld.web.util.htmllib import HTML
from clld.web.util.htmllib import literal
from markupsafe import Markup
from sqlalchemy import or_


GLOSS_ABBR_PATTERN = re.compile(
    "(?P<personprefix>1|2|3)?(?P<abbr>[A-Z]+)(?P<personsuffix>1|2|3)?(?=([^a-z]|$))"
)


def rendered_sentence(request, sentence, abbrs=None):
    """Format a sentence as HTML."""
    if sentence.xhtml:
        return HTML.div(
            HTML.div(Markup(sentence.xhtml), class_="body"), class_="sentence"
        )

    if abbrs is None:
        q = DBSession.query(models.GlossAbbreviation).filter(
            or_(
                models.GlossAbbreviation.language_pk == sentence.language_pk,
                models.GlossAbbreviation.language_pk is None,
            )
        )
        abbrs = dict((g.id, g.name) for g in q)

    def gloss_with_tooltip(gloss):
        person_map = {
            "1": "first person",
            "2": "second person",
            "3": "third person",
        }

        res = []
        end = 0
        for match in GLOSS_ABBR_PATTERN.finditer(gloss):
            if match.start() > end:
                res.append(gloss[end : match.start()])

            abbr = match.group("abbr")
            if abbr in abbrs:
                explanation = abbrs[abbr]
                if match.group("personprefix"):
                    explanation = (
                        f"{person_map[match.group('personprefix')]} {explanation}"
                    )

                if match.group("personsuffix"):
                    explanation = (
                        f"{explanation} {person_map[match.group('personsuffix')]}"
                    )

                res.append(
                    HTML.span(
                        HTML.span(
                            gloss[match.start() : match.end()].lower(), class_="sc"
                        ),
                        **{"data-hint": explanation, "class": "hint--bottom"},
                    )
                )
            else:
                res.append(
                    (match.group("personprefix") or "")
                    + abbr  # noqa: W504
                    + (match.group("personsuffix") or "")  # noqa: W504
                )

            end = match.end()

        res.append(gloss[end:])
        return filter(None, res)

    units = []
    if sentence.analyzed and sentence.gloss:
        slices = {sl.index: sl for sl in sentence.forms}
        for pwc, (pword, pgloss) in enumerate(
            zip(sentence.analyzed.split("\t"), sentence.gloss.split("\t"))
        ):
            for gwc, (word, gloss) in enumerate(
                zip(pword.split("="), pgloss.split("="))
            ):
                i = pwc + gwc
                print(word, gloss)
                if i not in slices:
                    units.append(
                        HTML.div(
                            HTML.div(word),
                            HTML.div(word, class_="morpheme"),
                            HTML.div(*gloss_with_tooltip(gloss), **{"class": "gloss"}),
                            class_="gloss-unit",
                        )
                    )
                else:
                    units.append(
                        HTML.div(
                            HTML.div(
                                rendered_form(request, slices[i].form, structure=False)
                            ),
                            HTML.div(
                                rendered_form(request, slices[i].form),
                                class_="morpheme",
                            ),
                            HTML.div(*gloss_with_tooltip(gloss), **{"class": "gloss"}),
                            class_="gloss-unit",
                        )
                    )
    return HTML.div(
        HTML.div(
            HTML.div(
                HTML.div(sentence.original_script, class_="original-script")
                if sentence.original_script
                else "",
                HTML.div(sentence.name, class_="object-language"),
                HTML.div(*units, **{"class": "gloss-box"}) if units else "",
                HTML.div(sentence.description, class_="translation")
                if sentence.description
                else "",
                class_="body",
            ),
            class_="sentence",
        ),
        class_="sentence-wrapper",
    )


def rendered_form(request, ctx, structure=True):
    if structure:
        if ctx.morphs != []:
            return literal(
                "-".join(
                    [
                        link(request, form.morph, label=form.morph.name.strip("-"))
                        for form in ctx.morphs
                    ]
                )
            )
        return literal("&nbsp;")
    return link(request, ctx)
