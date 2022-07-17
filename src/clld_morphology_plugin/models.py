from clld.db.meta import Base
from clld.db.meta import PolymorphicBaseMixin
from clld.db.models.common import Contribution
from clld.db.models.common import FilesMixin
from clld.db.models.common import HasFilesMixin
from clld.db.models.common import HasSourceMixin
from clld.db.models.common import IdNameDescriptionMixin
from clld.db.models.common import Language
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from zope.interface import implementer
from clld_morphology_plugin.interfaces import IPOS
from clld_morphology_plugin.interfaces import ILexeme
from clld_morphology_plugin.interfaces import IMeaning
from clld_morphology_plugin.interfaces import IMorph
from clld_morphology_plugin.interfaces import IMorphset
from clld_morphology_plugin.interfaces import IWordform


@implementer(IMeaning)
class Meaning(Base, PolymorphicBaseMixin, IdNameDescriptionMixin):
    pass


@implementer(IMorphset)
class Morpheme(Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin):
    __table_args__ = (UniqueConstraint("language_pk", "id"),)

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="morphemes")
    comment = Column(Unicode)


@implementer(IMorph)
class Morph(Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin):
    __table_args__ = (
        UniqueConstraint("language_pk", "id"),
        UniqueConstraint("morpheme_pk", "id"),
    )

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)
    morpheme_pk = Column(Integer, ForeignKey("morpheme.pk"), nullable=False)
    morpheme = relationship(Morpheme, innerjoin=True, backref="allomorphs")


class MorphemeMeaning(Base):
    id = Column(String, unique=True)
    morpheme_pk = Column(Integer, ForeignKey("morpheme.pk"), nullable=False)
    meaning_pk = Column(Integer, ForeignKey("meaning.pk"), nullable=False)
    morpheme = relationship(Morpheme, innerjoin=True, backref="meanings")
    meaning = relationship(Meaning, innerjoin=True, backref="morphemes")


@implementer(IPOS)
class POS(Base, IdNameDescriptionMixin):
    pass


@implementer(IWordform)
class Wordform(
    Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin, HasFilesMixin
):
    __table_args__ = (
        UniqueConstraint("language_pk", "id"),
        UniqueConstraint("pos_pk", "id"),
    )

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="wordforms")

    pos_pk = Column(Integer, ForeignKey("pos.pk"))
    pos = relationship(POS, backref="wordforms", innerjoin=True)

    segmented = Column(String)

    @property
    def audio(self):
        for f in self._files:
            if f.mime_type.split("/")[0] == "audio":
                return f
        return None

    @property
    def lexeme(self):
        if len(self.lexemes) == 0:
            return None
        return self.lexemes[0].lexeme


class FormMeaning(Base):
    id = Column(String, unique=True)
    form_pk = Column(Integer, ForeignKey("wordform.pk"), nullable=False)
    meaning_pk = Column(Integer, ForeignKey("meaning.pk"), nullable=False)
    form = relationship(Wordform, innerjoin=True, backref="meanings")
    meaning = relationship(Meaning, innerjoin=True, backref="forms")


class FormSlice(Base):
    form_pk = Column(Integer, ForeignKey("wordform.pk"))
    morph_pk = Column(Integer, ForeignKey("morph.pk"))
    morpheme_meaning_pk = Column(Integer, ForeignKey("morphememeaning.pk"))
    form_meaning_pk = Column(Integer, ForeignKey("formmeaning.pk"))
    form = relationship(Wordform, backref="morphs")
    morph = relationship(Morph, backref="forms")
    index = Column(Integer)
    form_meaning = relationship(FormMeaning)
    morpheme_meaning = relationship(MorphemeMeaning, backref="morph_tokens")


class Wordform_files(Base, FilesMixin):  # noqa: N801
    pass


@implementer(ILexeme)
class Lexeme(Base, IdNameDescriptionMixin):
    __table_args__ = (UniqueConstraint("language_pk", "id"),)

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)

    morpheme_pk = Column(Integer, ForeignKey("morpheme.pk"))
    root_morpheme = relationship(Morpheme, innerjoin=True, backref="lexemes")

    comment = Column(Unicode)

    @property
    def form_count(self):
        return len(self.forms)


class Inflection(Base):
    form_pk = Column(Integer, ForeignKey("wordform.pk"), nullable=False)
    lexeme_pk = Column(Integer, ForeignKey("lexeme.pk"), nullable=False)
    form = relationship(Wordform, innerjoin=True, backref="lexemes")
    lexeme = relationship(Lexeme, innerjoin=True, backref="forms")


class LexemeLexemePart(Base):
    derived_pk = Column(Integer, ForeignKey("lexeme.pk"), nullable=False)
    base_pk = Column(Integer, ForeignKey("lexeme.pk"), nullable=True)
    derived_lexeme = relationship(
        Lexeme, innerjoin=True, backref="base_lexemes", foreign_keys=derived_pk
    )
    base_lexeme = relationship(
        Lexeme, innerjoin=True, backref="derived_lexemes", foreign_keys=base_pk
    )


class LexemeMorphemePart(Base):
    morpheme_pk = Column(Integer, ForeignKey("morpheme.pk"), nullable=False)
    lexeme_pk = Column(Integer, ForeignKey("lexeme.pk"), nullable=False)
    morpheme = relationship(Morpheme, innerjoin=True, backref="derived_lexemes")
    lexeme = relationship(Lexeme, innerjoin=True, backref="derivational_morphemes")
