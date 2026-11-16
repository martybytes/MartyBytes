<h1 align="center">Marty Sampson</h1>

<p align="center">
  <em>Building software with AI agents, writing down what works, and running 37Metrics and Dimension42.</em>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
    <img alt="The Marty M beside the wordmark MARTY SAMPSON and the line MARTYBYTES, building software with agents" src="assets/banner-light.svg" width="900">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/martybytes/MartyBytes/actions/workflows/readme.yml"><img alt="README refresh status" src="https://img.shields.io/github/actions/workflow/status/martybytes/MartyBytes/readme.yml?branch=main&style=flat-square&label=readme"></a>
  <a href="https://github.com/martybytes/MartyBytes/actions/workflows/metrics.yml"><img alt="Metrics refresh status" src="https://img.shields.io/github/actions/workflow/status/martybytes/MartyBytes/metrics.yml?branch=main&style=flat-square&label=metrics"></a>
  <a href="https://github.com/martybytes/MartyBytes/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/martybytes/MartyBytes?style=flat-square"></a>
</p>

<p align="center">
  <a href="#sites">Sites</a> &middot;
  <a href="#featured-projects">Projects</a> &middot;
  <a href="#activity">Activity</a> &middot;
  <a href="#contact">Contact</a>
</p>

---

## About

I build software with AI agents across the whole delivery lifecycle — planning,
code, review, release — and publish the field notes as I go. Most of what is
public here is tooling that came out of that work: one terminal setup across four
operating systems, a README standard a linter can enforce, and a meeting archive
an agent can grep.

## Sites

| Site | What you will find there |
|---|---|
| [martybytes.com](https://martybytes.com) | Practical field notes for building software with agents across the delivery lifecycle |
| [martysampson.ai](https://martysampson.ai) | Source-backed explainers about AI systems, memory, context and evaluation |
| [martysampson.com](https://martysampson.com) | My personal site: physics, technology, interests and professional lessons |
| [37metrics.com](https://37metrics.com) | 37Metrics, the independent technology holding company I founded |
| [dimension42.ai](https://dimension42.ai) | Dimension42, technology advisory and implementation for business decision-makers |

## Featured projects

| Project | What it does |
|---|---|
| [terminal-stack](https://github.com/martybytes/terminal-stack) | One terminal setup — WezTerm, tmux, Starship, zsh and PowerShell — deployed to Windows, WSL, Linux and macOS from a single chezmoi repo, so every machine gets the same prompt, keys and fonts |
| [awesome-github-readme](https://github.com/martybytes/awesome-github-readme) | A 40-rule README rubric with a one-file linter, five Claude Code skills and advisory hooks; this page is checked against it |
| [fathom-clerk](https://github.com/martybytes/fathom-clerk) | Syncs every Fathom meeting to disk — transcript, summary, action items, raw JSON — in predictable folders, so an agent or `grep` can read your meetings without the API |
| [get-computer-info](https://github.com/martybytes/get-computer-info) | Gathers system information on Linux, macOS and Windows and prints it in a form ready to hand an AI as context, rather than retyping specs into a prompt |
| [resurrect.wezterm](https://github.com/martybytes/resurrect.wezterm) | Saves and restores WezTerm windows, tabs and panes, in the spirit of tmux-resurrect |
| [alt-h](https://github.com/martybytes/alt-h) | A Windows tray utility that binds Alt+H to minimise the focused window |

## Activity

<p align="left"><img alt="GitHub metrics for martybytes: contribution calendar, activity, repositories and coding time" src="https://raw.githubusercontent.com/martybytes/MartyBytes/main/github-metrics.svg"></p>

### Currently working on

- [martybytes/awesome-github-readme](https://github.com/martybytes/awesome-github-readme) — Write, audit and maintain READMEs that earn a reader's second minute. A scored rubric, five Claude Code skills, advisory hooks and a template library.
- [martybytes/agent007memory](https://github.com/martybytes/agent007memory) — An improved UI for agent007memory so you can see health and real-time information
- [martybytes/get-computer-info](https://github.com/martybytes/get-computer-info) — Retrieves information about computers (linux, mac, PC) and produces output ready for consumption by AI for context
- [martybytes/alt-h](https://github.com/martybytes/alt-h) — A small Windows tray utility that registers Alt+H as a global hotkey and minimizes the currently focused window.
- [martybytes/terminal-stack](https://github.com/martybytes/terminal-stack) — One terminal setup - WezTerm, tmux, Starship, zsh and PowerShell - deployed to Windows, WSL, native Linux and macOS from a single chezmoi repo.

### Latest projects

- [martybytes/fathom-clerk](https://github.com/martybytes/fathom-clerk) — Sync every Fathom meeting to disk, one folder per meeting, each holding the transcript, summary, action items and raw JSON. Folder names are predictable, so an agent or grep can read them. It stays under Fathom's 10-requests-a-minute limit and adds full-text search, a Windows scheduled sync, and terminal and browser dashboards.

### Recent pull requests

- [feat(prompt): collapse finished prompts to \`❯ cmd\`, with no blank line](https://github.com/martybytes/terminal-stack/pull/67) on [martybytes/terminal-stack](https://github.com/martybytes/terminal-stack)
- [fix(install): the workspace question only saves a real directory](https://github.com/martybytes/terminal-stack/pull/66) on [martybytes/terminal-stack](https://github.com/martybytes/terminal-stack)
- [docs(agentmemory): legacy graph files and post-hang dead letters](https://github.com/martybytes/terminal-stack/pull/65) on [martybytes/terminal-stack](https://github.com/martybytes/terminal-stack)
- [fix: AgentMemory engine memory (mem:insights) and Ctrl+Enter send-now in WezTerm](https://github.com/martybytes/terminal-stack/pull/64) on [martybytes/terminal-stack](https://github.com/martybytes/terminal-stack)
- [fix(agentmemory): count semantic facts without sending them all](https://github.com/martybytes/terminal-stack/pull/63) on [martybytes/terminal-stack](https://github.com/martybytes/terminal-stack)

### Recently starred

- [pingdotgg/t3code](https://github.com/pingdotgg/t3code) — The best way to control Claude Code, Codex and more from any computer or phone
- [bryantbrock/cursor-background-agents-mcp](https://github.com/bryantbrock/cursor-background-agents-mcp) — Kick off Cursor background agents via MCP

> [!NOTE]
> These four lists are regenerated daily by [a workflow](.github/workflows/readme.yml)
> from public activity only — private repositories, forks and this repository are
> left out, and a project already under "Currently working on" is not repeated
> under "Latest projects". Most of my client and company work is private, so this
> is a sample rather than the whole picture.

## Contact

<p align="left">
  <a href="https://github.com/martybytes"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/github-dark.svg"><img alt="GitHub" src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/github.svg" width="32" height="32"></picture></a>
  <a href="https://www.linkedin.com/in/martysampson/"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/linkedin-dark.svg"><img alt="LinkedIn" src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/linkedin.svg" width="32" height="32"></picture></a>
  <a href="https://x.com/martybytes"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/twitter-dark.svg"><img alt="X" src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/twitter.svg" width="32" height="32"></picture></a>
  <a href="https://www.youtube.com/@MartyBytes"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/youtube-dark.svg"><img alt="YouTube" src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/youtube.svg" width="32" height="32"></picture></a>
</p>

- Writing: [martybytes.com](https://martybytes.com) and [martysampson.ai](https://martysampson.ai)
- Video: [youtube.com/@MartyBytes](https://www.youtube.com/@MartyBytes)
- Professional: [linkedin.com/in/martysampson](https://www.linkedin.com/in/martysampson/)
- Short posts: [x.com/martybytes](https://x.com/martybytes)
- Advisory work: [dimension42.ai](https://dimension42.ai)
