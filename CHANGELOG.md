# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/GabrielAmare/Language/compare/v0.0.1...HEAD)

### Added

- `base/`
    - `base/decorators` which implement useful decorators for auto-generation code.
    - `base/models` which implement classes & attributes descriptors.
    - `base/processing` which implement base classes for language processing.
    - `base/building` which implement the builder function that can construct an object from a `base.processing.Element`
      object.
    - `base/groups` which implement `Charset` class representing a group that can be inverted.
      <br>
      <pre>
        obj = Charset({'x', 'y', 'z'}, inverted=True))
        # `obj` represent the set of elements that are <strong>not</strong>
        # in the set {'x', 'y', 'z'}
      </pre>

- `core/`
    - `core/langs` package which contains all the required langs of the project.
    - `core/langs/bnf` which implement the initial version for
      the [bnf](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form)-like language package.
    - `core/langs/python` which implement the initial version for the python language package.
    - `core/langs/regex` which implement the initial version for the regex language package.
    - simple integrity test for `core/langs/bnf`, `core/langs/python` & `core/langs/regex`.
    - `core/builder` which implement the lang package generation
        - `core/builder/loaders` which defines the classes to load files
        - `core/builder/builders` which defines the classes to build files
        - `core/builder/options` module which regroup the possible options for build
        - `core/builder/params` module which regroup the possible params for build (they all have default value)
        - `core/builder/config` module to handle the lang-package build config file (`config.json` by default)
        - `core/builder/package` module which the package entry point, implementing the class `LangPackage` which is
          responsible for the whole package build
- `tools/`
    - `graphs` simple implementation for graphs structure.
    - `queries` simple implementation for queries (js like array) syntax.
    - `console` simple debugging tool to prettify console display.
    - `files` functions & classes to manage files.
    - `style_case` functions to handle string cases (checking & converting)
    - `flow/` package to handle element processing
        - `flow/tokenizer/` package to handle tokenization base on `tools/flow` containing base implementation,
          proxies (to build tokenizers the easy way), and a model function that does not rely on the `tools/flow`
          package and is built only with basic algorithmic statements (easy to rewrite the function in a different
          language). <br><pre>from tools.flow.tokenizer import *
          <br>tokenizer = Flow()
          <br>... # define your tokenizer
          <br>data = tokenizer.data
          <br>... # save the data into a json file<br></pre>

## [0.0.1](https://github.com/GabrielAmare/Language/releases/tag/v0.0.1) - 2022-06-07

### Added

- This `CHANGELOG.md` file.
- The `requirements.txt` file.
- The `.gitignore` file.
- The `.idea` directory.
- The `setup.bat` file which use is to set up the project.

