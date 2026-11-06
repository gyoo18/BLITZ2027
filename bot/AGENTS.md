# Blitz registration challenge bot

This folder is a bot for the Blitz registration challenge. The challenge is
solo: in each game the bot plays alone against the game itself, and the goal is
the highest score. Write the bot, upload it, study the games it plays on the
Blitz servers, improve it.

The team's registration score is its best score in a server game the bot played
to the end (`timedOut` false in `games`; a kick or a crash sets it). The user
finishes the registration on the dashboard, which shows what is still missing.

## Working in this folder

| Language   | File you edit                                      | Install / build                   | Run                        |
| ---------- | -------------------------------------------------- | --------------------------------- | -------------------------- |
| C#         | `Bot.cs`                                           | `dotnet build`                    | `dotnet run`               |
| Java       | `src/main/java/codes/blitz/game/bot/Bot.java`      | `mvn package`                     | `java -jar target/bot.jar` |
| Python     | `bot.py`                                           | `pip install -r requirements.txt` | `python application.py`    |
| TypeScript | `Bot.ts`                                           | `npm install`                     | `npm start`                |

- Put the strategy in the bot file and in new files next to it.
- Never edit the generated game types (`GameMessage.cs`, `generated/`,
  `game_message.py`, `GameInterface.ts`): they are replaced by every starter kit
  release. They are the reference for what the bot receives each tick and which
  actions it can send, so read them first.
- The rules (how the score is earned, what each action does) are not in this
  folder: they are on the dashboard's Documentation page, so ask the user for
  them.
- Never edit the connection code (`Application.cs`, `GameClient.cs`,
  `Application.java`, `message/`, `websocket/`, `application.py`, `index.ts`).
- Each tick has a time limit, much shorter on the servers than the launcher's
  default (150 ms, with a kick after 50 late answers, when this was written). A
  late answer counts as no action for that tick, and a kick ends the game and
  voids its score, so keep per-tick work bounded and test locally with
  `--timePerTickMs 150 --maxTimeoutsBeforeKick 50`.

## Test locally

The launcher binary (`blitz-challenge-…`, written `<launcher>` below) is the
local game server. Run it from its own folder, in the background since it waits
for the bot, then start the bot from this one:

```bash
<launcher> --keepAlive false --delayBetweenTicksMs 0 --recordPath game.json > launcher.log 2>&1 &
```

With `--keepAlive false` the launcher plays one game and exits. It waits for the
bot on `ws://127.0.0.1:8765`, so start the bot (the Run command above) once the
launcher is up. `game.json`, in the launcher's folder, holds `commandsAndTicks`,
the game state of every tick, and `gameResults`; it is large, so query it with
`jq` rather than printing it. `launcher.log` has a `Replay:` line: pass its
`--biome` and `--randomSeed` back to the launcher to play the same map again,
e.g. to compare two versions of the bot. `<launcher> --help` lists the other
options.

## Compete on the servers

The games that count run on the servers, so the real feedback comes from there.
The same launcher talks to them; run these from this folder:

```bash
<launcher> login                  # the user approves it in the browser; lasts 24 h
<launcher> upload ../bot.zip      # upload the zip (below), wait for the build
<launcher> practice               # play a practice game with the active bot
<launcher> download <gameId>      # replay and logs into blitz-games/<gameId>/
<launcher> games                  # your team's games, newest first
<launcher> builds [buildId]       # your builds; with an id, that build's log
```

- `login` opens a browser on this machine, where the user clicks "Authorize";
  it waits up to 5 minutes for that click. When a command says the login is
  missing or expired, ask the user to run `<launcher> login` in their own
  terminal, or run it in the background and ask them to approve it. If the
  browser is on another machine (SSH, a cloud IDE), the user authorizes there and
  then, within a minute, runs `curl "<the 127.0.0.1 address the browser could not
  open>"` on this machine.
- `upload` takes the bot's zip, at most 10 MB, holding only what the server
  needs to build the bot, at the zip's root (subfolders kept):

  | Language   | Put in the zip                                                   |
  | ---------- | ---------------------------------------------------------------- |
  | C#         | `*.cs`, `*.csproj`, `global.json`                                |
  | Java       | `pom.xml`, `src/`                                                |
  | Python     | `*.py`, `requirements.txt`                                       |
  | TypeScript | `*.ts`, `package.json`, `package-lock.json` (if any), `tsconfig.json` |

  Plus any other file the bot reads at run time. Nothing else: no build output
  or dependencies (`bin/`, `obj/`, `target/`, `dist/`, `node_modules/`,
  `venv/`, `.venv/`, `__pycache__/`, even for a matching file inside them), no
  AGENTS.md, logs or downloaded games, and never secrets such as `.env`. Make
  it with whatever zip tool this machine has, outside this folder (e.g.
  `../bot.zip`), and list its contents before uploading.
  `upload` exits 0 once the build passed, or prints the build log and the reason
  and exits 1 (the previous bot stays active).
- `practice` plays a practice game with the active bot and prints its row; on
  failure it prints why and exits 1. Its first column is the id `download` takes,
  and `score` is the bot's score (`rank` is always 1: it plays alone). An empty
  score means the bot never connected: its crash is in `bot.log`.
- Waiting for a build or a game can take several minutes, longer than most tool
  timeouts. Either run the command in the background, or add `--no-wait` (it
  prints the build or game id) and check later: `builds <id>` exits 2 while the
  build is still running, and `games` shows each game's `state`. `upload` and
  `practice` also exit 2 when they stop waiting before the end.
- Any command exits 3 when the servers' rate limit refused it: wait a minute,
  then run it again.
- This launcher only sees the registration challenge (the game's launcher,
  `blitz-game-…`, only sees the game), for `games` and `builds` too.
- `download` writes:
  - `replay.jsonl`: one game state per line, the same shape as a tick in the
    local `game.json`: the whole game as a viewer sees it, not the message the
    bot receives. A line is tens of kilobytes, so never print whole lines: pick
    fields with `jq`: `tail -1 replay.jsonl | jq -c keys` lists them, then e.g.
    `jq -c '{<field>, <field>}' replay.jsonl | tail -5`. Line numbers are not
    tick numbers: find a tick by its `currentTick` field (the line with N is the
    state after the bot's tick-N action).
  - `bot.log`: your bot's own output (prints, errors, crashes) in that game.
  - `game.log`: the game server's log. Its `Replay:` line plays that game's map
    locally.

The loop: change the strategy, check it locally (the same `--biome` and
`--randomSeed` compare two versions on one map), `upload`, `practice`,
`download` the game and compare the replay with what the bot meant to do.
`games` lists the team's latest 100 games: download the lowest scores to see
what went wrong.
