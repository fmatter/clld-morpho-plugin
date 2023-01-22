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
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from sqlalchemy import Unicode
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from zope.interface import implementer
from clld_morphology_plugin.interfaces import IPOS
from clld_morphology_plugin.interfaces import ILexeme
from clld_morphology_plugin.interfaces import IMeaning
from clld_morphology_plugin.interfaces import IMorph
from clld_morphology_plugin.interfaces import IMorpheme
from clld_morphology_plugin.interfaces import IWordform
from clld_morphology_plugin.interfaces import IStem, IGloss
from sqlalchemy.ext.hybrid import hybrid_property


@implementer(IMeaning)
class Meaning(Base, PolymorphicBaseMixin, IdNameDescriptionMixin):
    pass


@implementer(IGloss)
class Gloss(Base):
    id = Column(String, unique=True)
    name = Column(String, unique=True)
    meaning_pk = Column(Integer, ForeignKey("meaning.pk"), nullable=True)
    meaning = relationship(Meaning, innerjoin=True, backref="glosses")

    @property
    def morphs(self):
        return list(set([s.morph for s in self.formslices]))


@implementer(IMorpheme)
class Morpheme(Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin):
    __table_args__ = (UniqueConstraint("language_pk", "id"),)

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="morphemes")
    comment = Column(Unicode)

    @property
    def glosses(self):
        glosslist = []
        for m in self.allomorphs:
            glosslist.extend(m.glosses)
        return list(set(glosslist))

    @property
    def forms(self):
        formlist = []
        for m in self.allomorphs:
            for fslice in m.formslices:
                formlist.append(fslice.form)
        return list(set(formlist))


@implementer(IMorph)
class Morph(Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin):
    __table_args__ = (
        UniqueConstraint("language_pk", "id"),
        UniqueConstraint("morpheme_pk", "id"),
    )

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)
    morpheme_pk = Column(Integer, ForeignKey("morpheme.pk"), nullable=True)
    morpheme = relationship(Morpheme, innerjoin=True, backref="allomorphs")
    rsep = Column(String, nullable=True)
    lsep = Column(String, nullable=True)
    morph_type = Column(String, nullable=True)

    @property
    def glosses(self):
        return list(set([s.gloss for s in self.formslices]))


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

    parts = Column(MutableList.as_mutable(PickleType), default=[])

    @property
    def audio(self):
        for f in self._files:
            if f.mime_type.split("/")[0] == "audio":
                return f
        return None


class Wordform_files(Base, FilesMixin):  # noqa: N801
    pass


@implementer(ILexeme)
class Lexeme(Base, IdNameDescriptionMixin):
    __table_args__ = (UniqueConstraint("language_pk", "id"),)

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)

    comment = Column(Unicode)


@implementer(IStem)
class Stem(Base, IdNameDescriptionMixin):
    __table_args__ = (UniqueConstraint("language_pk", "id"),)

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)

    lexeme_pk = Column(Integer, ForeignKey("lexeme.pk"))
    lexeme = relationship(Lexeme, innerjoin=True, backref="stems")
    comment = Column(Unicode)


class Inflection(Base):
    """Inflections link a lexeme with a wordform, adding information about the morph and the inflectional value"""

    form_pk = Column(Integer, ForeignKey("wordform.pk"), nullable=False)
    lexeme_pk = Column(Integer, ForeignKey("lexeme.pk"), nullable=False)
    form = relationship(Wordform, innerjoin=True, backref="lexemes")
    lexeme = relationship(Lexeme, innerjoin=True, backref="forms")


class InflectionalCategory(Base, IdNameDescriptionMixin):
    pass


class InflectionalValue(Base, IdNameDescriptionMixin):
    category_pk = Column(Integer, ForeignKey("inflectionalcategory.pk"), nullable=False)
    category = relationship(InflectionalCategory, innerjoin=True, backref="values")


class FormPart(Base):
    form_pk = Column(Integer, ForeignKey("wordform.pk"), nullable=False)
    morph_pk = Column(Integer, ForeignKey("morph.pk"), nullable=False)
    form = relationship(Wordform, innerjoin=True, backref="morphs")
    morph = relationship(Morph, innerjoin=True, backref="formslices")
    index = Column(Integer, nullable=True)
    gloss_pk = Column(Integer, ForeignKey("gloss.pk"), nullable=False)
    gloss = relationship(Gloss, innerjoin=True, backref="formslices")


class FormMeaning(Base):
    # id = Column(String, unique=True)
    form_pk = Column(Integer, ForeignKey("wordform.pk"), nullable=False)
    meaning_pk = Column(Integer, ForeignKey("meaning.pk"), nullable=False)
    form = relationship(Wordform, innerjoin=True, backref="meanings")
    meaning = relationship(Meaning, innerjoin=True, backref="forms")
