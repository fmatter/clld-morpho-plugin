from sqlalchemy.orm import joinedload
from sqlalchemy import and_
from clld.web import datatables
from clld.web.datatables.base import (
    DataTable,
    LinkCol,
    Col,
    LinkToMapCol,
    IdCol,
    RefsCol,
)
from clld_morpho_plugin import models
from clld.db.models.common import (
    Contribution,
    Language,
    Parameter,
    Sentence_files,
    Sentence,
)
from clld.web.datatables.sentence import TsvCol, TypeCol, DetailsRowLinkCol


class DescriptionLinkCol(LinkCol):

    """Render a link to the unit using the description as label."""

    def get_attrs(self, item):
        return {"label": item.description}


class Morphs(DataTable):

    __constraints__ = [Language]

    def base_query(self, query):
        query = query.join(Language).options(joinedload(models.Morph.language))

        if self.language:
            return query.filter(models.Morph.language == self.language)
        return query

    def col_defs(self):
        return [
            LinkCol(self, "name"),
            DescriptionLinkCol(self, "description"),
            LinkCol(
                self, "language", model_col=Language.name, get_obj=lambda i: i.language
            ),
        ]


class Morphemes(DataTable):
    __constraints__ = [Language]

    def base_query(self, query):
        print(query)
        query = query.join(Language).options(joinedload(models.Morpheme.language))

        if self.language:
            return query.filter(models.Morpheme.language == self.language)
        return query

    def col_defs(self):
        return [
            LinkCol(self, "name"),
            Col(self, "meaning"),
            DescriptionLinkCol(self, "description"),
            LinkCol(
                self, "language", model_col=Language.name, get_obj=lambda i: i.language
            ),
        ]


class Meanings(DataTable):
    def col_defs(self):
        return [
            LinkCol(self, "name"),
        ]


def includeme(config):
    config.register_datatable("meanings", Meanings)
    config.register_datatable("morphs", Morphs)
    config.register_datatable("morphemes", Morphemes)
