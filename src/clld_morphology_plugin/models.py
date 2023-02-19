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
from clld_morphology_plugin import interfaces
from sqlalchemy.ext.hybrid import hybrid_property
import pandas as pd
from math import floor


@implementer(interfaces.IMeaning)
class Meaning(Base, PolymorphicBaseMixin, IdNameDescriptionMixin):
    pass


@implementer(interfaces.IGloss)
class Gloss(Base):
    id = Column(String, unique=True)
    name = Column(String, unique=True)
    meaning_pk = Column(Integer, ForeignKey("meaning.pk"), nullable=True)
    meaning = relationship(Meaning, innerjoin=True, backref="glosses")

    @property
    def morphs(self):
        return list(
            dict.fromkeys(
                [s.formpart.morph for s in self.formglosses if s.formpart.morph]
            )
        )


@implementer(interfaces.IMorpheme)
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
            for glosses in m.glosses:
                if glosses not in glosslist:
                    glosslist.append(glosses)
        return glosslist

    @property
    def forms(self):
        formlist = []
        for m in self.allomorphs:
            for fslice in m.formslices:
                formlist.append(fslice.form)
        return list(set(formlist))


@implementer(interfaces.IMorph)
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
        glosslist = []
        for fslice in self.formslices:
            if fslice.glosses not in glosslist:
                glosslist.append(fslice.glosses)
        return glosslist

    @property
    def inflectionalvalues(self):
        infllist = []
        for fslice in self.formslices:
            for partinflection in fslice.inflections:
                if partinflection.inflection.value not in infllist:
                    infllist.append(partinflection.inflection.value)
        return infllist

    @property
    def wordforms(self):
        formlist = [x.form for x in self.formslices]
        for x in self.stemslices:
            for form in x.stem.wordforms:
                if form not in formlist:
                    formlist.append(form)
        return formlist


@implementer(interfaces.IPOS)
class POS(Base, IdNameDescriptionMixin):
    pass


@implementer(interfaces.IWordform)
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
    def lexeme(self):
        if len(self.formstems) > 0:
            return self.formstems[0].stem.lexeme
        return None

    @property
    def audio(self):
        for f in self._files:
            if f.mime_type.split("/")[0] == "audio":
                return f
        return None

    @property
    def inflections(self):
        for s in self.slices:
            for infl in s.inflections:
                yield infl.inflection

    @property
    def stem(self):
        if self.formstems:
            return self.formstems[0].stem
        if self.inflections:
            for infl in self.inflections:
                if infl.stem:
                    return infl.stem
        return None


@implementer(interfaces.IForm)
class Form(
    Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin, HasFilesMixin
):
    __table_args__ = (UniqueConstraint("language_pk", "id"),)

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True, backref="forms")

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="forms")

    parts = Column(MutableList.as_mutable(PickleType), default=[])

    @property
    def link_form(self):
        if len(self.formslices) > 1:
            print(self)
            print(self.formslices)
            return self
        else:
            return self.formslices[0].wordform

    @property
    def audio(self):
        for f in self._files:
            if f.mime_type.split("/")[0] == "audio":
                return f
        return None


class FormPart(Base):
    id = Column(String, unique=True)
    form_pk = Column(Integer, ForeignKey("form.pk"), nullable=False)
    wordform_pk = Column(Integer, ForeignKey("wordform.pk"), nullable=False)
    form = relationship(Form, innerjoin=True, backref="formslices")
    wordform = relationship(Wordform, innerjoin=True, backref="multiforms")
    index = Column(Integer, nullable=True)


class Form_files(Base, FilesMixin):  # noqa: N801
    pass


class Wordform_files(Base, FilesMixin):  # noqa: N801
    pass


@implementer(interfaces.ILexeme)
class Lexeme(Base, IdNameDescriptionMixin):
    __table_args__ = (UniqueConstraint("language_pk", "id"),)

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)

    comment = Column(Unicode)

    paradigm_x = Column(MutableList.as_mutable(PickleType), default=[])
    paradigm_y = Column(MutableList.as_mutable(PickleType), default=[])

    @hybrid_property
    def inflections(self):
        infl_list = []
        for stem in self.stems:
            infl_list.extend(stem.inflections)
        return infl_list

    @property
    def inflectionalcategories(self):
        infl_list = []
        for stem in self.stems:
            infl_list.extend(stem.inflectionalcategories)
        return list(dict.fromkeys(infl_list))


@implementer(interfaces.IStem)
class Stem(Base, IdNameDescriptionMixin):
    __table_args__ = (UniqueConstraint("language_pk", "id"),)

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)

    lexeme_pk = Column(Integer, ForeignKey("lexeme.pk"))
    lexeme = relationship(Lexeme, innerjoin=True, backref="stems")
    comment = Column(Unicode)

    parts = Column(MutableList.as_mutable(PickleType), default=[])

    rsep = Column(String, nullable=True)
    lsep = Column(String, nullable=True)

    @property
    def inflectionalcategories(self):
        return list(dict.fromkeys([x.value.category for x in self.inflections]))

    @property
    def glosses(self):
        return [x.gloss for x in self.stemglosses]

    @property
    def gloss(self):
        if self.glosses:
            return ".".join([x.name for x in self.glosses])
        return self.description

    @property
    def wordforms(self):
        return [x.form for x in self.stemforms]


class StemGloss(Base):
    stem_pk = Column(Integer, ForeignKey("stem.pk"), nullable=False)
    stem = relationship(Stem, innerjoin=True, backref="stemglosses")
    gloss_pk = Column(Integer, ForeignKey("gloss.pk"), nullable=False)
    gloss = relationship(Gloss, innerjoin=True, backref="stemglosses")


class WordformPart(Base):
    id = Column(String, unique=True, nullable=False)
    form_pk = Column(Integer, ForeignKey("wordform.pk"), nullable=False)
    morph_pk = Column(Integer, ForeignKey("morph.pk"), nullable=True)
    form = relationship(Wordform, innerjoin=True, backref="slices")
    morph = relationship(Morph, innerjoin=True, backref="formslices")
    index = Column(Integer, nullable=True)


class WordformPartGloss(Base):
    formpart_pk = Column(Integer, ForeignKey("wordformpart.pk"), nullable=False)
    formpart = relationship(WordformPart, innerjoin=True, backref="glosses")
    gloss_pk = Column(Integer, ForeignKey("gloss.pk"), nullable=False)
    gloss = relationship(Gloss, innerjoin=True, backref="formglosses")


@implementer(interfaces.IInflCategory)
class InflectionalCategory(Base, IdNameDescriptionMixin):
    value_order = Column(MutableList.as_mutable(PickleType), default=[])

    @property
    def ordered(self):
        order = {val: pos for pos, val in enumerate(self.value_order)}
        sort_count = len(order)
        for plus, val in enumerate(self.values):
            if val.id not in order:
                order[val.id] = sort_count + plus
        if self.value_order[0] == "-":
            return ["-"] + sorted(self.values, key=lambda x: order[x.id])
        return sorted(self.values, key=lambda x: order[x.id]) + ["-"]


@implementer(interfaces.IInflValue)
class InflectionalValue(Base, IdNameDescriptionMixin):
    category_pk = Column(Integer, ForeignKey("inflectionalcategory.pk"), nullable=False)
    category = relationship(InflectionalCategory, innerjoin=True, backref="values")
    gloss_pk = Column(Integer, ForeignKey("gloss.pk"), nullable=True)
    gloss = relationship(Gloss, innerjoin=True, backref="values")

    def __str__(self):
        if self.gloss:
            return self.gloss.name
        return self.name

    def __lt__(self, other):
        if isinstance(other, str):
            return self.name < other
        return self.name < other.name

    @property
    def morphs(self):
        morphlist = []
        for inflection in self.inflections:
            morphlist.extend(inflection.morphs)
        return list(dict.fromkeys(morphlist))

    @property
    def exponents(self):
        res = {}
        for inflection in self.inflections:
            res[
                tuple([formpart.formpart.morph for formpart in inflection.formparts])
            ] = []
        for inflection in self.inflections:
            res[
                tuple([formpart.formpart.morph for formpart in inflection.formparts])
            ].append(inflection.form)
        print(res)
        return res


class StemPart(Base):
    id = Column(String, unique=True)
    stem_pk = Column(Integer, ForeignKey("stem.pk"), nullable=False)
    morph_pk = Column(Integer, ForeignKey("morph.pk"), nullable=False)
    stem = relationship(Stem, innerjoin=True, backref="slices")
    morph = relationship(Morph, innerjoin=True, backref="stemslices")
    index = Column(Integer, nullable=True)


@implementer(interfaces.IDerivProcess)
class DerivationalProcess(Base, IdNameDescriptionMixin):
    pass


class Derivation(Base):
    process_pk = Column(Integer, ForeignKey("derivationalprocess.pk"), nullable=False)
    process = relationship(DerivationalProcess, innerjoin=True, backref="derivations")
    source_root_pk = Column(Integer, ForeignKey("morph.pk"), nullable=True)
    source_root = relationship(
        Morph, innerjoin=True, backref="derivations", foreign_keys=[source_root_pk]
    )
    source_stem_pk = Column(Integer, ForeignKey("stem.pk"), nullable=True)
    source_stem = relationship(
        Stem, innerjoin=True, backref="derivations", foreign_keys=[source_stem_pk]
    )
    target_pk = Column(Integer, ForeignKey("stem.pk"), nullable=False)
    target = relationship(
        Stem, innerjoin=True, backref="derived_from", foreign_keys=[target_pk]
    )

    @property
    def source(self):
        if self.source_stem:
            return self.source_stem
        if self.source_root:
            return self.source_root
        return None


class StemPartDerivation(Base):
    stempart_pk = Column(Integer, ForeignKey("stempart.pk"), nullable=False)
    stempart = relationship(StemPart, innerjoin=True, backref="derivations")
    derivation_pk = Column(Integer, ForeignKey("derivation.pk"), nullable=False)
    derivation = relationship(Derivation, innerjoin=True, backref="stemparts")


class Inflection(Base):
    value_pk = Column(Integer, ForeignKey("inflectionalvalue.pk"), nullable=False)
    stem_pk = Column(Integer, ForeignKey("stem.pk"), nullable=False)
    value = relationship(InflectionalValue, innerjoin=True, backref="inflections")
    stem = relationship(Stem, innerjoin=True, backref="inflections")

    @property
    def form(self):
        if self.formparts[0].form:
            return self.formparts[0].form
        return self.formparts[0].formpart.form

    @property
    def morphs(self):
        return [x.formpart.morph for x in self.formparts]


class WordformPartInflection(Base):
    form_pk = Column(Integer, ForeignKey("form.pk"), nullable=True)
    form = relationship(Form, innerjoin=True, backref="inflections")
    formpart_pk = Column(Integer, ForeignKey("wordformpart.pk"), nullable=False)
    formpart = relationship(WordformPart, innerjoin=True, backref="inflections")
    value_pk = Column(Integer, ForeignKey("inflection.pk"), nullable=False)
    inflection = relationship(Inflection, innerjoin=True, backref="formparts")


class StemPartGloss(Base):
    stempart_pk = Column(Integer, ForeignKey("stempart.pk"), nullable=False)
    stempart = relationship(StemPart, innerjoin=True, backref="glosses")
    gloss_pk = Column(Integer, ForeignKey("gloss.pk"), nullable=False)
    gloss = relationship(Gloss, innerjoin=True, backref="stempartglosses")


class WordformStem(Base):
    form_pk = Column(Integer, ForeignKey("wordform.pk"), nullable=False)
    stem_pk = Column(Integer, ForeignKey("stem.pk"), nullable=False)
    form = relationship(Wordform, innerjoin=True, backref="formstems")
    stem = relationship(Stem, innerjoin=True, backref="stemforms")
    index = Column(MutableList.as_mutable(PickleType), default=[])


class WordformMeaning(Base):
    form_pk = Column(Integer, ForeignKey("wordform.pk"), nullable=False)
    meaning_pk = Column(Integer, ForeignKey("meaning.pk"), nullable=False)
    form = relationship(Wordform, innerjoin=True, backref="meanings")
    meaning = relationship(Meaning, innerjoin=True, backref="forms")
