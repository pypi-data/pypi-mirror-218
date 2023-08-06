# tui-typer-tutor

![.github/assets/demo.gif](https://raw.githubusercontent.com/KyleKing/tui-typer-tutor/main/.github/assets/demo.gif)

Uncomplicated terminal typing practice.

Fork of `kraanzu/termtyper` with a focus on special characters. Inspired by `climech/typing-practice` and `justinsgithub/terminal-typing-tutor`.

## Installation

[Install with `pipx`](https://pypi.org/project/pipx/)

```sh
pipx install tui-typer-tutor
```

## Usage

Launch a typing session with the default text:

```sh
ttt
```

Or specify custom files with:

```sh
ttt --seed-file='./any-file.txt'
```

To uninstall run:

```sh
ttt --uninstall && pipx uninstall tui-typer-tutor
```

### Keys

This app supports a few unicode characters when found in the seed file:

- tab: `→`
- shift+tab: `←`
- enter/return: `⏎`
- escape: `␛`

[All supported characters are documented here](https://github.com/KyleKing/tui-typer-tutor/blob/main/tui_typer_tutor/constants/display_to_textual.py). `Ctrl` key combinations aren't yet supported and appear as an unknown character.

### Seed File

The algorithm for generating the expected text is:

1. Load each line of the seed file
1. Reorder randomly (keeping each line of text together)
1. Join without a delimeter keeping any leading white space per line

The default seed file is here: [./tui_typer_tutor/core/seed_data.txt](https://github.com/KyleKing/tui-typer-tutor/blob/main/tui_typer_tutor/core/seed_data.txt)

Ideas for better seed text generation are welcome!

## Project Status

See the `Open Issues` and/or the [CODE_TAG_SUMMARY]. For release history, see the [CHANGELOG].

## Contributing

We welcome pull requests! For your pull request to be accepted smoothly, we suggest that you first open a GitHub issue to discuss your idea. For resources on getting started with the code base, see the below documentation:

- [DEVELOPER_GUIDE]
- [STYLE_GUIDE]

## Code of Conduct

We follow the [Contributor Covenant Code of Conduct][contributor-covenant].

### Open Source Status

We try to reasonably meet most aspects of the "OpenSSF scorecard" from [Open Source Insights](https://deps.dev/pypi/tui-typer-tutor)

## Responsible Disclosure

If you have any security issue to report, please contact the project maintainers privately. You can reach us at [dev.act.kyle@gmail.com](mailto:dev.act.kyle@gmail.com).

## License

[LICENSE]

[changelog]: https://tui-typer-tutor.kyleking.me/docs/CHANGELOG
[code_tag_summary]: https://tui-typer-tutor.kyleking.me/docs/CODE_TAG_SUMMARY
[contributor-covenant]: https://www.contributor-covenant.org
[developer_guide]: https://tui-typer-tutor.kyleking.me/docs/DEVELOPER_GUIDE
[license]: https://github.com/kyleking/tui-typer-tutor/blob/main/LICENSE
[style_guide]: https://tui-typer-tutor.kyleking.me/docs/STYLE_GUIDE
