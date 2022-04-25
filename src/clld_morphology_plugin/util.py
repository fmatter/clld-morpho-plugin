from clld.web.util.htmllib import HTML, literal
from clld.db.meta import DBSession
from markupsafe import Markup
from clld.db.models import common as models
from sqlalchemy import or_
import re
GLOSS_ABBR_PATTERN = re.compile(
    '(?P<personprefix>1|2|3)?(?P<abbr>[A-Z]+)(?P<personsuffix>1|2|3)?(?=([^a-z]|$))')

def rendered_sentence(sentence, abbrs=None, fmt='long'):
    """Format a sentence as HTML."""
    if sentence.xhtml:
        return HTML.div(
            HTML.div(Markup(sentence.xhtml), class_='body'), class_="sentence")

    if abbrs is None:
        q = DBSession.query(models.GlossAbbreviation).filter(
            or_(models.GlossAbbreviation.language_pk == sentence.language_pk,
                models.GlossAbbreviation.language_pk == None)
        )
        abbrs = dict((g.id, g.name) for g in q)

    def gloss_with_tooltip(gloss):
        person_map = {
            '1': 'first person',
            '2': 'second person',
            '3': 'third person',
        }

        res = []
        end = 0
        for match in GLOSS_ABBR_PATTERN.finditer(gloss):
            if match.start() > end:
                res.append(gloss[end:match.start()])

            abbr = match.group('abbr')
            if abbr in abbrs:
                explanation = abbrs[abbr]
                if match.group('personprefix'):
                    explanation = '%s %s' % (
                        person_map[match.group('personprefix')], explanation)

                if match.group('personsuffix'):
                    explanation = '%s %s' % (
                        explanation, person_map[match.group('personsuffix')])

                res.append(HTML.span(
                    HTML.span(gloss[match.start():match.end()].lower(), class_='sc'),
                    **{'data-hint': explanation, 'class': 'hint--bottom'}))
            else:
                res.append(
                    (match.group('personprefix') or '') +  # noqa: W504
                    abbr +  # noqa: W504
                    (match.group('personsuffix') or ''))

            end = match.end()

        res.append(gloss[end:])
        return filter(None, res)

    units = []
    if sentence.analyzed and sentence.gloss:
        analyzed = sentence.analyzed
        glossed = sentence.gloss
        for morpheme, gloss in zip(analyzed.split('\t'), glossed.split('\t')):
            units.append(HTML.div(
                HTML.div(morpheme, class_='morpheme'),
                HTML.div(*gloss_with_tooltip(gloss), **{'class': 'gloss'}),
                class_='gloss-unit'))

    return HTML.div(
        HTML.div(
            HTML.div(
                HTML.div(sentence.original_script, class_='original-script')
                if sentence.original_script else '',
                HTML.div(literal(sentence.markup_text or sentence.name),
                         class_='object-language'),
                HTML.div(*units, **{'class': 'gloss-box'}) if units else '',
                HTML.div(sentence.description, class_='translation')
                if sentence.description else '',
                class_='body',
            ),
            class_="sentence",
        ),
        class_="sentence-wrapper",
    )