from clldutils import jsonlib


try:
    from importlib.resources import files  # pragma: no cover
except ImportError:  # pragma: no cover
    from importlib_resources import files  # pragma: no cover


cldf_path = files("clld_morphology_plugin") / "cldf"
FormSlices = jsonlib.load(cldf_path / "FormSlices-metadata.json")
MorphsetTable = jsonlib.load(cldf_path / "MorphsetTable-metadata.json")
MorphTable = jsonlib.load(cldf_path / "MorphTable-metadata.json")
POSTable = jsonlib.load(cldf_path / "POSTable-metadata.json")
LexemeTable = jsonlib.load(cldf_path / "LexemeTable-metadata.json")
InflectionTable = jsonlib.load(cldf_path / "InflectionTable-metadata.json")
LexemeLexemeParts = jsonlib.load(cldf_path / "LexemeLexemeParts-metadata.json")
LexemeMorphemeParts = jsonlib.load(cldf_path / "LexemeMorphemeParts-metadata.json")
