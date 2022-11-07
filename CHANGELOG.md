# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Changed
* only requiring `zope.interface` instead of everything

## [0.0.6] - 2022-11-05

### Fixed
* wordform template does not require a meaning
* CLDF data in MANIFEST.in

## [0.0.5] -- 2022-07-19

### Added
* show lexeme meanings (`description`) in views

### Changed
* derived lexemes need not have a base lexeme
* if the first word has no POS, let's assume none do.

### Fixed
* errors for wordforms with fewer formslices than morphemes

## [0.0.4] -- 2022-06-10

### Added
* lexemes
* tabs in morpheme and morph detail views

### Removed
* bugs

### Changed
* missing POS are rendered as `*`
* wordform structure links to morphemes even in detail view
* allow missing FormSlices in wordforms

## [0.0.3] - 2022-06-03

### Added
* parts of speech
* button for copying sentence IDs

### Changed
* glossed morphs in examples link directly to morphemes instead of morphs

## [0.0.2] - 2022-05-27

### Added
* polysemy
* highlighting
* corresponding CLDF table metadata
* wordform audio

### Changed
* example rendering, now with g-words

## [0.0.1] - 2022-05-02

* Initial release

[Unreleased]: https://github.com/fmatter/clld-morphology-plugin/compare/0.0.6...HEAD
[0.0.6]: https://github.com/fmatter/clld-morphology-plugin/compare/0.0.5...0.0.6
[0.0.5]: https://github.com/fmatter/clld-morphology-plugin/releases/tag/0.0.5
[0.0.4]: https://github.com/fmatter/clld-morphology-plugin/releases/tag/0.0.4
[0.0.3]: https://github.com/fmatter/clld-morphology-plugin/releases/tag/0.0.3
[0.0.2]: https://github.com/fmatter/clld-morphology-plugin/releases/tag/0.0.2
[0.0.1]: https://github.com/fmatter/clld-morphology-plugin/releases/tag/v0.0.1
