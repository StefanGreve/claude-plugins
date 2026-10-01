# Claude Plugins

This project is a personal [Claude Code](https://claude.com/claude-code) plugin
marketplace.

They have been open-sourced for my own convenience, so you may use anything you
see here at your own risk. Some rules are tailored to meet my personal needs and
will not match your own house style out of the box.

## Usage

Register the marketplace, then install the plugin:

```sh
claude plugin marketplace add StefanGreve/claude-plugins
claude plugin install devkit@stefangreve-plugins
```

## Plugins

| Plugin   | Skill                      | Purpose                                            |
| -------- | -------------------------- | -------------------------------------------------- |
| `devkit` | `/devkit:commit-message`   | Write a commit message in my conventions           |

Claude loads a skill on its own when the request matches its description, so the
slash command is a shortcut rather than the only entry point.

## Development

Validate both manifests before pushing, and treat warnings as errors:

```text
claude plugin validate . --strict
claude plugin validate ./plugins/devkit --strict
```

To debug a skill against the live source:

```sh
claude --plugin-dir ./plugins/devkit
```

It loads as `devkit@inline` and overrides an installed
`devkit@stefangreve-plugins`. Edits apply on `/reload-plugins`, and the override
is silent: `claude plugin list` still shows the marketplace row, since that row
reflects settings rather than what loaded.

Prefer this over `claude plugin marketplace add .`, which claims the same
`stefangreve-plugins` name as the GitHub source and is refused once both exist.

A plugin installed from the GitHub source stays on the version declared in
`plugin.json` until that number changes, so bump it with every release.
