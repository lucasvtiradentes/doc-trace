from __future__ import annotations

from doctrace.cmd_registry import COMMANDS, DIR_COMMANDS
from doctrace.core.constants import APP_NAME, CLI_ALIASES


def _get_zsh_completion() -> str:
    cmd_lines = "\n        ".join(f"'{name}:{info['desc']}'" for name, info in COMMANDS.items())
    aliases_str = " ".join(CLI_ALIASES)

    case_blocks = []
    for name, info in COMMANDS.items():
        flags = info["flags"]
        subcommands = info["subcommands"]
        is_dir_cmd = name in DIR_COMMANDS

        conditions = []
        if subcommands:
            subs = " ".join(f"'{s}'" for s in subcommands)
            conditions.append(f"(( CURRENT == 3 )) && _values 'subcommand' {subs}")
        if is_dir_cmd:
            conditions.append("(( CURRENT == 3 )) && _files -/")
        if flags:
            flags_str = " ".join(f"'{f}'" for f in flags)
            conditions.append(f'[[ "$cur" == -* ]] && _values "flag" {flags_str}')
        if is_dir_cmd and flags:
            conditions.append("(( CURRENT > 3 )) && _files -/")

        if conditions:
            body = "\n            ".join(conditions)
            case_blocks.append(f"        {name})\n            {body}\n            ;;")

    cases_str = "\n".join(case_blocks)

    return f"""#compdef {APP_NAME}

_{APP_NAME}() {{
    local -a commands
    local cur="${{words[CURRENT]}}"

    commands=(
        {cmd_lines}
    )

    case "$words[2]" in
{cases_str}
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

    case_blocks = []
    for name, info in COMMANDS.items():
        flags = info["flags"]
        subcommands = info["subcommands"]
        is_dir_cmd = name in DIR_COMMANDS

        if subcommands:
            subs_str = " ".join(subcommands)
            case_blocks.append(f'''        {name})
            if [[ "$cur" == -* ]]; then
                COMPREPLY=( $(compgen -W "{" ".join(flags)}" -- "$cur") )
            else
                COMPREPLY=( $(compgen -W "{subs_str}" -- "$cur") )
            fi
            return 0
            ;;''')
        elif is_dir_cmd:
            flags_str = " ".join(flags) if flags else ""
            case_blocks.append(f'''        {name})
            if [[ "$cur" == -* ]]; then
                COMPREPLY=( $(compgen -W "{flags_str}" -- "$cur") )
            else
                COMPREPLY=( $(compgen -d -- "$cur") )
            fi
            return 0
            ;;''')

    cases_str = "\n".join(case_blocks)

    return f'''_{APP_NAME}() {{
    local cur prev words cword
    _init_completion || return

    cur="${{COMP_WORDS[COMP_CWORD]}}"
    prev="${{COMP_WORDS[COMP_CWORD-1]}}"
    local cmd="${{COMP_WORDS[1]}}"

    if [[ $COMP_CWORD -eq 1 ]]; then
        COMPREPLY=( $(compgen -W "{cmd_names}" -- "$cur") )
        return 0
    fi

    case "$cmd" in
{cases_str}
    esac
}}

{complete_lines}
'''


def _get_fish_completion() -> str:
    lines = []

    for a in CLI_ALIASES:
        lines.append(f"complete -c {a} -f")

    for name, info in COMMANDS.items():
        for a in CLI_ALIASES:
            lines.append(f'complete -c {a} -n "__fish_use_subcommand" -a {name} -d "{info["desc"]}"')

    for name, info in COMMANDS.items():
        subcommands = info["subcommands"]
        flags = info["flags"]
        is_dir_cmd = name in DIR_COMMANDS

        for sub in subcommands:
            for a in CLI_ALIASES:
                lines.append(f'complete -c {a} -n "__fish_seen_subcommand_from {name}" -a "{sub}"')

        for flag in flags:
            for a in CLI_ALIASES:
                if flag.startswith("--"):
                    lines.append(f'complete -c {a} -n "__fish_seen_subcommand_from {name}" -l {flag[2:]}')
                elif flag.startswith("-") and len(flag) == 2:
                    lines.append(f'complete -c {a} -n "__fish_seen_subcommand_from {name}" -s {flag[1:]}')

        if is_dir_cmd:
            for a in CLI_ALIASES:
                lines.append(
                    f'complete -c {a} -n "__fish_seen_subcommand_from {name}" -a "(__fish_complete_directories)"'
                )

    return "\n".join(lines) + "\n"


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
