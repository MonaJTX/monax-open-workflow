# MonaX Open Workflow

**English** · [简体中文](README.zh-CN.md)

**Pick up a project in a fresh AI chat without explaining it all over again.** MonaX gives you a few Markdown files for the decisions you’ve made, where you stopped, and what still needs checking. Your assistant can read them before it starts. So can the next person who works on the project.

Say you ask for an *Unread* filter a week after designing a reading list. The assistant can look up two earlier decisions: search matches titles, and the newest items come first. You can spend the next conversation designing the filter instead of reconstructing the last one.

[Use it in your project](#use-it-in-your-project) · [Try a fresh-chat handoff](#try-a-fresh-chat-handoff) · [MIT license](LICENSE)

## What can I do with it?

| If you’re asking… | What you can take away |
| --- | --- |
| “Where did we leave off?” | A handoff that lists the current goal, past decisions, and next check. Ask a fresh chat which file supports its answer. [Reading list example](examples/general/README.md) |
| “Can I trust this change?” | A handoff from your coding assistant with the files changed, checks it ran, results, and the behavior you still need to test. [Development workflow](plugins/monax-open-workflow/rules/development.md) |
| “Can players claim the same reward twice?” | Trace a button click to the reward service and its configuration. Run `python -B examples/game/reward_demo.py` from this repo. The first successful claim earns 3 tokens, a repeat earns 0, and the balance stays at 3. [Runnable game example](examples/game/reward_demo.py) |
| “How do I keep two AI video shots consistent?” | Give the next artist a shot plan they can use. In shot one a hand releases a blue paper boat moving right. Shot two opens with that same boat already drifting right. Each shot has still, storyboard, and motion prompts, plus a record of which references still need review. [Shot pack](examples/ai-video/shots.md) · [Production record](examples/ai-video/ledger.md) |

## Use it in your project

You need Python 3.10+ and an AI assistant that can read and edit files in a project folder. The steps below work with the Markdown files directly. The templates and some linked guides are in Chinese. You can give the assistant instructions and keep your project notes in English.

**1. Get the workflow.** Open a terminal where you keep your tools and run:

```sh
git clone https://github.com/MonaJTX/monax-open-workflow.git
cd monax-open-workflow
python --version
```

You can also choose **Code → Download ZIP** and open a terminal in the extracted folder containing `plugins`. If your Python command is `python3` or `py -3`, use it in the commands below. **Keep the terminal in the workflow folder. Open your own project in the AI assistant.**

**2. Preview the files.** Replace `../my-project` with the path to your existing project. For a throwaway trial, run `mkdir ../my-project` first, choosing a fresh directory.

```sh
python -B plugins/monax-open-workflow/scripts/project.py init --project-root "../my-project"
```

With `Planned`, review the paths and then apply. With `Conflict`, check the listed paths first. If only `AGENTS.md` exists, initialize a fresh temporary folder, copy its new `.monax-workflow` and `PROJECT_CONTEXT` folders into your project, and append its full entry (including the HTML comment) to your existing `AGENTS.md`. For other overlaps, compare files individually and preserve your team’s instructions. [Detailed merge guide in Chinese](docs/USAGE.md#已有项目合并)

```sh
python -B plugins/monax-open-workflow/scripts/project.py init --project-root "../my-project" --apply
python -B plugins/monax-open-workflow/scripts/project.py check --project-root "../my-project"
```

After a clean setup, expect `Created`, then `NeedsProjectFacts`. That means the files are there and ready for your project details. For a project already using MonaX, go straight to the check.

**3. Give your assistant its first task.** Open the target project in your assistant and paste:

> Read AGENTS.md and PROJECT_CONTEXT/README.md. Using my README, project files, and what I tell you, write down the project goal, where work stopped, constraints to preserve, and decisions already made. Write in English. Ask me about missing facts. Replace the relevant TODOs and clear each resolved blocking item in PROJECT_CONTEXT/workflow_activation_profile.json after checking it. Only edit the project notes for this step.

Back in the workflow terminal, run:

```sh
python -B plugins/monax-open-workflow/scripts/project.py check --project-root "../my-project" --require-ready
```

`Ready` means the project entry, rule files, and required notes pass the setup checks. Use `pending` for outstanding project facts and `issues` for broken or conflicting files. To check the actual handoff, open a fresh chat **in your project** and ask: *“What should I work on next, which earlier decision affects it, and where is that written down?”* Open the file it cites and compare the answer.

## Try a fresh-chat handoff

To try this with fictional data, use the throwaway directory from step 2. Give your assistant the following brief **along with the prompt in step 3**:

> I’m designing a local reading list. Each item has a stable ID, title, date added, and read status. We’ve agreed that search matches titles only, the Unread filter shows unread items only, and the default sort is newest added first. Keep that order when filtering. We’re planning the interaction and haven’t started coding. Next I want to decide how search and Unread work together.

Once the check reports `Ready`, open a fresh chat in that folder. Ask *“If I search while Unread is on, what should I see, and in what order? Cite the project file.”* A good answer gives all three behaviors and points to the saved decision. If your assistant misses the file, ask it to read `AGENTS.md` in the target folder first.

## Optional plugin and maintenance

The optional Codex plugin adds skill discovery and reminders for setup, memory, development, games, and video. To use it, run `codex plugin marketplace add .` in this repo, then select and enable `monax-open-workflow` from the local marketplace in your client and review its hooks. For a team handoff, share the project notes your team has reviewed. [Setup, sharing, and upgrades](docs/USAGE.md)

To check a local copy of the distribution, run `python -B tools/run_checks.py`. To build its ZIP and SHA-256 manifest, run `python -B tools/package_release.py --output ../releases`. The examples use fictional data. The game demo runs locally, and the video example supplies prompts and planning documents for your own production tools.

[Validation and tested environments](VALIDATION.md) · [Distribution scope](docs/DISTRIBUTION.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md)
