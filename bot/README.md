# Blitz starter kits

One folder per language. Pick one, write your bot in its bot file, and run the
commands from inside that folder.

| Language   | Version        | File you edit                                      | Install / build                   | Run                        |
| ---------- | -------------- | -------------------------------------------------- | --------------------------------- | -------------------------- |
| C#         | .NET 10 SDK    | `csharp/Bot.cs`                                    | `dotnet build`                    | `dotnet run`               |
| Java       | JDK 25 + Maven | `java/src/main/java/codes/blitz/game/bot/Bot.java` | `mvn package`                     | `java -jar target/bot.jar` |
| Python     | Python 3.13    | `python/bot.py`                                    | `pip install -r requirements.txt` | `python application.py`    |
| TypeScript | Node.js 26     | `typescript/Bot.ts`                                | `npm install`                     | `npm start`                |

## Running locally

Your bot connects to `ws://127.0.0.1:8765`, so start the local game server
(from the downloaded binaries) before running your bot. Locally, the bot
registers with a default team name; on our servers it is authenticated
automatically (through the `TOKEN` environment variable).

## Files you should not edit

| Language   | Generated game types                        | Connection code                                                                     |
| ---------- | ------------------------------------------- | ----------------------------------------------------------------------------------- |
| C#         | `GameMessage.cs`                            | `Application.cs`, `GameClient.cs`                                                   |
| Java       | `src/main/java/codes/blitz/game/generated/` | `Application.java`, `message/`, `websocket/` (in `src/main/java/codes/blitz/game/`) |
| Python     | `game_message.py`                           | `application.py`                                                                    |
| TypeScript | `GameInterface.ts`                          | `index.ts`                                                                          |

The generated files are replaced by each new starter kit version, and the
connection code is what lets your bot talk to the server. You can add your own
source files next to your bot file.

## Uploading your bot

Upload a zip of one language folder, on the dashboard or with the launcher
(`<launcher> login`, then `<launcher> upload ../bot.zip`). The zip holds that
folder's contents (or the folder itself), must contain the language's marker
file, and stays under 10 MB: leave out build output and dependencies, since the
server builds the bot itself, and never include secrets such as `.env`.

### Make the zip

From the language folder, with git (any system): commit your changes, then

```bash
git archive --format=zip -o ../bot.zip HEAD
```

The zip holds exactly the committed files, and the folder's `.gitignore` already
leaves out build output, downloaded games, the launcher's output and `.env` files.

Without git, on macOS or Linux, from the language folder (if `zip` is missing,
install it, e.g. `sudo apt install zip`):

```bash
rm -f ../bot.zip && zip -r ../bot.zip . -x '.git/*' '.env*' '*/.env*' 'blitz-games/*' game.json game_logs.txt error.log launcher.log <zip excludes>
```

Without git, on Windows 10 or later, in Command Prompt or PowerShell (not Git
Bash, whose `tar` can't write zips), from the folder that holds the language
folder `<bot>`; then upload with `<launcher> upload bot.zip` from there:

```bat
tar -a -c -f bot.zip --exclude .git --exclude .env* --exclude <bot>/blitz-games --exclude <bot>/game.json --exclude <bot>/game_logs.txt --exclude <bot>/error.log --exclude <bot>/launcher.log <tar excludes> <bot>
```

| Language   | Marker file          | zip excludes                         | tar excludes                                                        |
| ---------- | -------------------- | ------------------------------------ | ------------------------------------------------------------------- |
| C#         | `Application.csproj` | `'bin/*' 'obj/*' '.vs/*'`            | `--exclude <bot>/bin --exclude <bot>/obj --exclude <bot>/.vs`       |
| Java       | `pom.xml`            | `'target/*' 'bin/*'`                 | `--exclude <bot>/target --exclude <bot>/bin`                        |
| Python     | `application.py`     | `'*__pycache__*' 'venv/*' '.venv/*'` | `--exclude __pycache__ --exclude <bot>/venv --exclude <bot>/.venv`  |
| TypeScript | `index.ts`           | `'node_modules/*' 'dist/*'`          | `--exclude <bot>/node_modules --exclude <bot>/dist`                 |

The zip goes next to the folder, not in it, so the next zip doesn't contain the
last one. `unzip -l ../bot.zip` (or `tar -tf bot.zip`) shows what is in it.
