from zope.interface import implementer
from clld.db.models.common import (
    Contribution,
    IdNameDescriptionMixin,
    HasSourceMixin,
    Language,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from clld_morpho_plugin.interfaces import *
from clld.db.meta import Base, PolymorphicBaseMixin


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
    meaning = Column(String)


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


@implementer(IWordform)
class Wordform(Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin):
    __table_args__ = (UniqueConstraint("language_pk", "id"),)

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="wordforms")

    meaning = Column(String)
    # meaning = relationship(Meaning, innerjoin=True, backref="wordforms")
    # meaning_pk = Column(Integer, ForeignKey("meaning.pk"))
