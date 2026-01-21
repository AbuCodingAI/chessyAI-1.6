# Chessy - Full-Featured Chess Platform

**📚 [Full Documentation](docs/README.md)** | **🚀 [Quick Start](docs/QUICK_START.md)** | **📊 [Training Status](docs/training/TRAINING_STATUS.md)** | **📖 [Index](docs/INDEX.md)**

**🎮 [Play Chessy Now!](PLAY_CHESSY.bat)** ← Double-click to start playing!

A complete, fully functional chess platform inspired by Chess.com. Built with vanilla HTML, CSS, and JavaScript - completely free and open source!

## 🎮 Features

### Core Gameplay
- **Fully Functional Chess Engine** - Complete chess rules implementation
- **Multiple AI Opponents** - 11 difficulty levels from Noob (100 Elo) to Super GM (2700 Elo)
- **Secret Boss** - "Random Guy" appears weak but plays at 3400 Elo!
- **Local 2-Player Mode** - Play against friends on the same device
- **Legal Move Highlighting** - See all possible moves for selected pieces
- **Move History** - Complete game notation tracking
- **Undo Moves** - Take back your last move
- **Captured Pieces Display** - Track material advantage

### Learning & Puzzles
- **Daily Puzzles** - Solve tactical puzzles to improve
- **Puzzle Rating System** - Track your puzzle-solving skill
- **Puzzle Streak** - Build winning streaks
- **Interactive Lessons** - Learn chess fundamentals (6 lesson categories)
- **Opening Principles** - Master the opening phase
- **Tactical Patterns** - Forks, pins, skewers, and more
- **Endgame Training** - King and pawn endgames
- **Checkmate Patterns** - Learn common mating patterns

### Achievements System
- **18 Unique Achievements** - Unlock badges as you play
- **Progress Tracking** - See your journey from beginner to master
- **Achievement Categories**:
  - First milestones (first game, first win)
  - Game count achievements (10, 50, 100 games)
  - Win achievements (10, 25, 50 wins)
  - Move count achievements (100, 500, 1000 moves)
  - AI victories (beat specific difficulty levels)
  - Puzzle achievements (solve 10, 50 puzzles)
  - Streak achievements (win/puzzle streaks)

### Profile & Personalization
- **Custom Avatars** - Choose from 20 emoji avatars
- **Username Customization** - Set your player name
- **Rating System** - Separate ratings for Rapid, Blitz, and Bullet
- **Statistics Dashboard** - Track games, wins, losses, draws, win rate
- **Member Since** - See when you joined
- **Recent Achievements Display** - Show off your latest unlocks

### Appearance & Settings
- **🌙 Dark Mode** - Easy on the eyes for night play
- **5 Board Themes** - Classic, Modern, Wood, Blue, Green
- **3 Piece Styles** - Classic, Modern, Alpha
- **Sound Effects** - Move sounds with toggle
- **Board Coordinates** - Show/hide file and rank labels
- **Piece Animations** - Smooth movement animations
- **Auto-Promotion** - Choose auto-queen or manual selection

### Statistics & Progress
- **Comprehensive Stats** - Games played, wins, losses, draws
- **Win Rate Calculation** - Track your success percentage
- **Total Moves Counter** - See how many moves you've made
- **Puzzle Statistics** - Puzzles solved, rating, current streak
- **Rating Progress** - Watch your skill improve over time
- **Persistent Storage** - All progress saved locally

## 🎯 Why Chessy?

Based on research of what makes Chess.com the #1 chess platform (see `chesscom.log`), Chessy implements:

1. **Accessibility** - Easy for beginners, challenging for experts
2. **Variety** - Multiple ways to play and learn
3. **Gamification** - Achievements, ratings, and progression
4. **Personalization** - Customize your experience
5. **Free Forever** - All features completely free
6. **No Account Required** - Play immediately
7. **Offline Capable** - Works without internet
8. **Privacy Focused** - All data stored locally

## 🚀 Quick Start

## 📁 Project Structure
- `index.html` – Complete UI with all game modes, puzzles, learning, achievements, profile, and settings
- `style.css` – Responsive styling with dark mode support and multiple themes
- `script.js` – Full chess engine, AI opponents, achievements system, and all game logic
- `chesscom.log` – Analysis of Chess.com features and what makes it successful
- `README.md` – This file

## 🎮 Game Modes

### AI Opponents (11 Levels)
1. **Noob** (Elo 100) - Random moves, perfect for absolute beginners
2. **Beginner** (Elo 400) - Understands basic captures
3. **Average** (Elo 1200) - Decent strategy and tactics
4. **Good** (Elo 1500) - Balanced, positional play
5. **Awesome** (Elo 1800) - Strong tactical awareness
6. **Master** (Elo 2000) - Very strong play
7. **IM** (Elo 2500) - International Master level
8. **GM** (Elo 2500) - Grandmaster level
9. **Super GM** (Elo 2700) - Elite world-class play
10. **Random Guy** (Elo 1) 🔥 - SECRET BOSS! Appears weak but plays at 3400 Elo
11. **Mystery** (Elo ??) - Random strength each game

### Local 2-Player
Play against a friend on the same device with full chess rules.

## GitHub Steps (Explained Like You’re 5)
1. **Go to the page.** Open your web browser, type `github.com`, and press Enter.
2. **Find this project.** Search for the Chessy project or open the link someone gave you.
3. **Look for the big green “Code” button.** Click it.
4. **Pick how to get the files.**
   - Easiest: click **Download ZIP**. Your computer will save a copy of the project.
   - If you use VS Code, you can click **Open with GitHub Desktop** and follow the little helper boxes.
5. **Open the folder.** After the ZIP finishes downloading, double-click it and drag the inside folder somewhere easy, like your Desktop. Make sure you unzip it before opening the files.
6. **Launch the site.** Double-click the new `open-site.bat` helper or the `index.html` file to open the chess page in your browser.
7. **Change things if you want.** Right-click any file and open it in a text editor (Notepad, VS Code, etc.). When you press Save, the browser will show your changes the next time you refresh.

> **Tip:** If GitHub only shows you the README page online, that’s normal. You need to download the files (steps 4–6) to see the full website.

## How to Test
Because the site is a static build, you only need a modern web browser to preview it. You can open the `index.html` file directly or serve the folder with a lightweight HTTP server.

### Option 1: Open the file directly
1. Locate the `index.html` file in the repository root.
2. Double-click it (or right-click → “Open with”) to launch it in your preferred browser.
3. Verify the following behaviours:
   - The navigation bar shows the tabs **Home**, **Play**, **AI PvP**, **Puzzles**, **Achievements**, **Stats**, and **Profile**.
   - The hero section displays the chess board from White’s perspective (white pieces at the bottom) with rank/file labels.
   - Scrolling reveals the feature panels, including puzzles, achievements, and player stats.
   - The footer year reflects the current calendar year.

### Option 1A: Launch from Git Bash on Windows
If you are in Git Bash and want to open the page without hunting for the file in Explorer, run:

```bash
# Step into the folder (adjust the path to where you saved the project)
cd /c/Users/<YourName>/Downloads/Chessy

# Ask Windows to open the file in your default browser
cmd.exe /c start "" index.html
```

Git Bash passes the command to Windows, which pops open `index.html` in your default browser. You can also run `explorer.exe "$(pwd)/index.html"` if you prefer using File Explorer.

### Option 2: Serve with a local HTTP server
Serving over HTTP is closer to how the page will behave in production and is recommended if you are testing on Chrome (which blocks some features when opening files via the `file://` protocol).

1. Ensure you have Node.js (16+) installed.
2. From the project root, run one of the following commands:
   - `npx serve` (installs a temporary static server)
   - `npx http-server .`
3. Open the URL shown in the terminal (typically `http://localhost:3000` or `http://127.0.0.1:8080`).
4. Repeat the verification checklist from Option 1.

## Additional Notes
- The AI PvP list is generated at runtime. Reloading the page randomises the “Mystery” opponent’s Elo. The hidden “Random Guy” boss keeps a public Elo of 1 but secretly plays at a 3400 rating.
- The layout is responsive; resize the browser window or use device emulation tools to check the mobile presentation.

## How to push your changes to GitHub (Git Bash commands)
Follow these steps in Git Bash after you have edited any files. Replace `main` with your branch name if you are pushing to a different branch.

1. **Check where you are.** Make sure you are inside the project folder:
   ```bash
   cd /c/Users/<YourName>/Downloads/Chessy
   ```

2. **See what changed.** This shows you which files are ready to save:
   ```bash
   git status
   ```

3. **Stage the updates.** Add everything you changed (or list files individually):
   ```bash
   git add .
   ```

4. **Write a commit message.** This records a checkpoint of your work:
   ```bash
   git commit -m "Describe what you changed"
   ```

5. **Send the commit to GitHub.** This is the actual `git push` command:
   ```bash
   git push origin main
   ```

6. **Confirm it worked.** Visit your repository page on GitHub and refresh. You should now see the new files and commits listed.

> Tip: If `git push` asks you to log in, follow the on-screen instructions to authenticate with GitHub (using a browser or a personal access token). You only need to do this the first time on a new computer.

### If you prefer to upload through the GitHub website
If `git push` still feels tricky, you can also copy the finished files into your repository directly from the browser:

1. Open your repository on GitHub and click the **Add file** button near the top right.
2. Choose **Upload files**. This opens a drag-and-drop panel.
3. In File Explorer, highlight `index.html`, `styles.css`, `script.js`, and any other files you want to copy (like `open-site.bat`).
4. Drag them into the upload panel, or click **choose your files** and select them one by one.
5. Scroll down to the **Commit changes** section. Enter a short summary (for example, “Add chess site files”).
6. Make sure **Commit directly to the `main` branch** is selected, then press **Commit changes**.
7. After the page refreshes, the files will appear in your GitHub repository—no command line needed.

> You can repeat these steps any time you want to update the site. Just upload the new versions of the files and commit them again.
