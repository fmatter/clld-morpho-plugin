from clld_morpho_plugin import models, interfaces


def includeme(config):
    config.registry.settings["mako.directories"].insert(
        1, "clld_morpho_plugin:templates"
    )
    config.register_resource("morph", models.Morph, interfaces.IMorph, with_index=True)
    config.register_resource(
        "morpheme",
        models.Morpheme,
        interfaces.IMorphset,
        with_index=True,
        with_detail=True,
    )
    config.register_resource(
        "meaning", models.Meaning, interfaces.IMeaning, with_index=True
    )
    config.register_resource(
        "wordform", models.Wordform, interfaces.IWordform, with_index=True
    )
