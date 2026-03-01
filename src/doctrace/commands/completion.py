from __future__ import annotations

from doctrace.core.constants import APP_NAME, CLI_ALIASES

COMMANDS = {
    "info": "show docs phases and warnings",
    "affected": "list docs affected by git diff",
    "preview": "interactive docs explorer in browser",
    "base": "manage base commit state",
    "init": "create doctrace.json",
    "index": "generate index.md from frontmatter",
    "completion": "generate shell completion",
}

DIR_COMMANDS = [c for c in COMMANDS if c not in ("base", "init", "completion")]


def _get_zsh_completion() -> str:
    cmd_lines = "\n        ".join(f"'{name}:{desc}'" for name, desc in COMMANDS.items())
    aliases_str = " ".join(CLI_ALIASES)

    return f"""#compdef {APP_NAME}

_{APP_NAME}() {{
    local -a commands

    commands=(
        {cmd_lines}
    )

    case "$words[2]" in
        base)
            if (( CURRENT == 3 )); then
                _values 'subcommand' 'update' 'show'
            fi
            ;;
        completion)
            if (( CURRENT == 3 )); then
                _values 'shell' 'zsh' 'bash' 'fish'
            fi
            ;;
        {"|".join(DIR_COMMANDS)})
            if (( CURRENT == 3 )); then
                _files -/
            fi
            ;;
        *)
            if (( CURRENT == 2 )); then
                _describe -t commands 'command' commands
            fi
            ;;
    esac
}}

compdef _{APP_NAME} {aliases_str}
"""


def _get_bash_completion() -> str:
    cmd_names = " ".join(COMMANDS.keys())
    complete_lines = "\n".join(f"complete -F _{APP_NAME} {alias}" for alias in CLI_ALIASES)
    case_aliases = "|".join(CLI_ALIASES)

    return f'''_{APP_NAME}() {{
    local cur prev commands
    COMPREPLY=()
    cur="${{COMP_WORDS[COMP_CWORD]}}"
    prev="${{COMP_WORDS[COMP_CWORD-1]}}"
    commands="{cmd_names}"

    case "$prev" in
        base)
            COMPREPLY=( $(compgen -W "update show" -- "$cur") )
            return 0
            ;;
        completion)
            COMPREPLY=( $(compgen -W "zsh bash fish" -- "$cur") )
            return 0
            ;;
        {"|".join(DIR_COMMANDS)})
            COMPREPLY=( $(compgen -d -- "$cur") )
            return 0
            ;;
        {case_aliases})
            COMPREPLY=( $(compgen -W "$commands" -- "$cur") )
            return 0
            ;;
    esac
}}

{complete_lines}
'''


def _get_fish_completion() -> str:
    cmd_lines = "\n".join(
        "\n".join(f'complete -c {a} -n "__fish_use_subcommand" -a {name} -d "{desc}"' for a in CLI_ALIASES)
        for name, desc in COMMANDS.items()
    )

    init_lines = "\n".join(f"complete -c {a} -f" for a in CLI_ALIASES)
    completion_lines = "\n".join(
        f'complete -c {a} -n "__fish_seen_subcommand_from completion" -a "zsh bash fish"' for a in CLI_ALIASES
    )
    base_lines = "\n".join(
        f'complete -c {a} -n "__fish_seen_subcommand_from base" -a "update show"' for a in CLI_ALIASES
    )
    dir_cmds_str = " ".join(DIR_COMMANDS)
    dir_lines = "\n".join(
        f'complete -c {a} -n "__fish_seen_subcommand_from {dir_cmds_str}" -a "(__fish_complete_directories)"'
        for a in CLI_ALIASES
    )

    return f"""{init_lines}

{cmd_lines}

{completion_lines}

{base_lines}

{dir_lines}
"""


def run(shell: str | None) -> int:
    if not shell:
        print(f"usage: {APP_NAME} completion <shell>")
        print("shells: zsh, bash, fish")
        print()
        print("Add to your shell config:")
        print(f'  zsh:  eval "$({APP_NAME} completion zsh)"')
        print(f'  bash: eval "$({APP_NAME} completion bash)"')
        print(f"  fish: {APP_NAME} completion fish | source")
        return 1

    shell = shell.lower()

    generators = {
        "zsh": _get_zsh_completion,
        "bash": _get_bash_completion,
        "fish": _get_fish_completion,
    }

    if shell not in generators:
        print(f"error: unknown shell '{shell}'")
        print("supported: zsh, bash, fish")
        return 1

    print(generators[shell]())
    return 0
