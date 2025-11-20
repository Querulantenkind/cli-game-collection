# CLI Game Collection - User Guide

Welcome to the CLI Game Collection! This guide will help you get the most out of your gaming experience.

## Table of Contents
- [Getting Started](#getting-started)
- [Playing Games](#playing-games)
- [Progression Systems](#progression-systems)
- [Customization](#customization)
- [Tips & Tricks](#tips--tricks)
- [Troubleshooting](#troubleshooting)

---

## Getting Started

### First Launch

1. Run the game collection:
   ```bash
   python3 main.py
   ```

2. You'll see an animated splash screen, then the main menu

3. Use **↑↓** arrow keys to navigate, **Enter** to select

### Main Menu Options

- **Play Games** - Choose from 13 classic games
- **Settings** - Customize your experience
- **Statistics** - View your gaming stats
- **Achievements** - See unlocked achievements
- **Help** - Game instructions and tips
- **Load Game** - Continue a saved game
- **Daily Challenges** - Today's challenges
- **Quit** - Exit the collection

---

## Playing Games

### Universal Controls

**In Any Game:**
- **P** - Pause/Resume
- **Q** - Quit to menu
- **Arrow Keys** - Navigate/Move (in most games)

**In Menus:**
- **↑↓** - Navigate options
- **Enter** - Select
- **Q** - Go back

### Game-Specific Guides

#### 🐍 Snake
**Objective:** Eat food to grow, avoid walls and yourself

**Controls:**
- Arrow Keys - Change direction
- P - Pause
- Q - Quit

**Tips:**
- Plan your path ahead
- Use the edges to turn around
- Speed increases with score
- Try to spiral inward for safety

**Scoring:**
- +10 per food eaten
- Bonus for consecutive foods
- Speed multiplier for higher difficulties

---

#### 🧱 Tetris
**Objective:** Clear lines by filling rows with blocks

**Controls:**
- ← → - Move piece
- ↓ - Soft drop (fast fall)
- ↑ or Space - Rotate
- P - Pause
- Q - Quit

**Tips:**
- Save space for the long piece (I-block)
- Clear multiple lines at once for bonus points
- Try to keep the stack low
- Plan piece placement 2-3 pieces ahead

**Scoring:**
- Single line: 100 × level
- Double line: 300 × level
- Triple line: 500 × level
- Tetris (4 lines): 800 × level

---

#### 👻 Pac-Man
**Objective:** Collect all dots while avoiding ghosts

**Controls:**
- Arrow Keys - Move
- P - Pause
- Q - Quit

**Tips:**
- Eat power pellets to turn the tables on ghosts
- Clear corners first for escape routes
- Ghosts have predictable patterns
- Frightened ghosts give bonus points

**Scoring:**
- Dot: 10 points
- Power pellet: 50 points
- Ghost (frightened): 200-1600 points
- Clear all dots: +1000 bonus

---

#### 🏓 Pong
**Objective:** Score 5 points before your opponent

**Controls:**
- W/S or ↑↓ - Move paddle
- A - Toggle AI/2-player mode
- P - Pause
- Q - Quit

**Tips:**
- Hit the ball with paddle edges for angles
- Predict ball trajectory
- Watch opponent's position
- Use angles to your advantage

**Modes:**
- **vs AI** - Three difficulty levels
- **2-Player** - Local multiplayer (I/K keys for P2)

---

#### 2️⃣0️⃣4️⃣8️⃣
**Objective:** Combine tiles to reach 2048

**Controls:**
- Arrow Keys - Slide tiles
- R - Restart
- Q - Quit

**Tips:**
- Keep highest tile in a corner
- Build numbers in one direction
- Don't move aimlessly - plan ahead
- Keep the board organized

**Strategy:**
- Pick a corner (bottom-right recommended)
- Build a "snake" pattern
- Avoid moving in the fourth direction

---

#### 💣 Minesweeper
**Objective:** Reveal all cells without hitting mines

**Controls:**
- Arrow Keys - Move cursor
- Space/Enter - Reveal cell
- F - Toggle flag
- Q - Quit

**Tips:**
- Start with corners and edges
- Numbers show adjacent mine count
- Flag suspected mines
- Use logic, not luck
- 6 wrong guesses allowed

**Patterns to Learn:**
- 1-2-1 = mine in middle
- 1-1 at edge = mines on sides
- Numbers touching flags = solved

---

#### 👾 Space Invaders
**Objective:** Destroy all aliens before they reach you

**Controls:**
- ← → or A/D - Move ship
- Space - Shoot
- P - Pause
- Q - Quit

**Tips:**
- Take cover behind shields
- Eliminate bottom row first
- Watch for alien shots
- Speed increases as you clear aliens
- 3 lives to complete the wave

---

#### 🧱 Breakout
**Objective:** Break all bricks with the ball

**Controls:**
- ← → or A/D - Move paddle
- Space - Launch ball
- P - Pause
- Q - Quit

**Tips:**
- Aim for top bricks for higher scores
- Use paddle angles to control ball
- Watch ball trajectory
- Break sides first for easier access
- 3 lives - don't miss the ball!

---

#### 📝 Hangman
**Objective:** Guess the word before 6 wrong guesses

**Controls:**
- A-Z - Guess letters
- Q - Quit

**Tips:**
- Start with common letters (E, A, R, T)
- Look for word patterns
- All words are programming/tech related
- Fewer wrong guesses = higher score

**Word Categories:**
- Programming languages
- Tech companies
- Computer terms
- Developer tools

---

#### ❌⭕ Tic-Tac-Toe
**Objective:** Get three in a row (horizontal, vertical, or diagonal)

**Controls:**
- Arrow Keys - Move cursor
- Space/Enter - Place mark
- M - Toggle AI/2-player mode
- P - Pause
- Q - Quit

**Tips:**
- Control the center
- Block opponent's winning moves
- Create double-threat scenarios
- AI has three difficulty levels

**Strategy:**
- Center is most valuable
- Corners are second best
- Edges are least valuable

---

#### 🔤 Wordle
**Objective:** Guess the 5-letter word in 6 tries

**Controls:**
- A-Z - Type letters
- Enter - Submit guess
- Backspace - Delete letter
- Q - Quit

**Tips:**
- Start with vowel-heavy words
- Use common letters (E, A, R, T, O)
- All words are programming/tech related
- Pay attention to letter positions

**Color Coding:**
- **[X]** - Correct letter, correct position (green)
- **X** - Correct letter, wrong position (yellow)
- **·X·** - Letter not in word (gray)

**Good Starting Words:**
- REACT
- ARRAY
- REGEX
- PARSE

---

#### 🐸 Frogger
**Objective:** Cross the road and river to reach goals

**Controls:**
- Arrow Keys - Move
- P - Pause
- Q - Quit

**Tips:**
- Time your movements carefully
- Watch traffic patterns
- Jump on logs and turtles
- Avoid water and cars
- Reach 5 goals to complete level

**Scoring:**
- Goal reached: +50 points
- Time bonus: Faster is better
- Level completion: +200 points

---

#### 🔢 Sudoku
**Objective:** Fill the 9x9 grid with numbers 1-9

**Controls:**
- Arrow Keys - Move cursor
- 1-9 - Enter number
- Delete/0 - Clear cell
- Q - Quit

**Tips:**
- Start with rows/cols with most numbers
- Look for single candidates
- Use process of elimination
- Check rows, columns, and 3x3 boxes
- No guessing - pure logic

**Techniques:**
- Naked singles
- Hidden singles
- Pointing pairs
- Box/line reduction

---

## Progression Systems

### 🏆 High Scores

- **Automatic Tracking** - Top 10 scores per game
- **Timestamps** - See when you achieved each score
- **New High Indicator** - Celebrate your achievements
- **Persistent** - Scores saved between sessions

**View High Scores:**
- From game over screen
- In Statistics menu
- Press H during any game

---

### 🎖️ Achievements

**34 Achievements to Unlock!**

**Categories:**
- **Milestone** - Reach score thresholds
- **Mastery** - Perfect performance
- **Challenge** - Difficult feats
- **Explorer** - Try all games
- **Special** - Unique accomplishments

**Viewing Achievements:**
1. Main Menu → Achievements
2. Browse unlocked/locked achievements
3. See point values and progress
4. Total points displayed

**Tips for Achievement Hunting:**
- Try all games for Explorer achievements
- Focus on one game for Mastery
- Daily play helps with Special achievements
- Check requirements in achievement list

---

### 📊 Statistics

**Comprehensive Tracking:**
- Games played, won, lost
- Win rates and streaks
- Total play time
- Score trends with graphs
- Session history

**Viewing Statistics:**
1. Main Menu → Statistics
2. Choose "Overall" or specific game
3. View detailed metrics
4. See ASCII graphs of performance

**Statistics Include:**
- Current win streak
- Best score
- Average score
- Score improvement trend
- Recent session history

---

### 📅 Daily Challenges

**3 New Challenges Every Day!**

**Features:**
- Rotates at midnight
- Track daily streak
- Earn challenge points
- Different games each day

**Viewing Challenges:**
1. Main Menu → Daily Challenges
2. See today's 3 challenges
3. Complete them by playing games
4. Track your streak

**Challenge Types:**
- Score targets
- Time limits
- Special conditions
- Win requirements

**Tips:**
- Complete all 3 for maximum points
- Streaks add multipliers
- Challenges reset daily
- Plan your gaming session

---

## Customization

### ⚙️ Settings

**Access:** Main Menu → Settings

#### General Settings
- **Sound** - Toggle sound (if available)
- **Theme** - Choose visual style
  - Classic (default)
  - Dark (high contrast)
  - Neon (colorful)
  - Retro (vintage)
  - Minimal (clean)
- **Show High Scores** - Display during game

#### Per-Game Settings
- **Speed** - Slow, Medium, Fast
- **Difficulty** - Easy, Normal, Hard
- **Starting Level** - For progressive games

**Reset Settings:**
- Press R in Settings menu
- Confirms before resetting
- Restores all defaults

---

### 🎨 Themes

**5 Visual Themes:**

1. **Classic**
   - Traditional look
   - Single-line borders
   - Standard colors

2. **Dark**
   - High contrast
   - Easy on eyes
   - Double-line borders

3. **Neon**
   - Bright colors
   - Cyberpunk vibe
   - Rounded borders

4. **Retro**
   - Vintage terminal
   - ASCII borders
   - Nostalgic feel

5. **Minimal**
   - Clean design
   - Thin borders
   - Distraction-free

**Change Theme:**
1. Settings → General → Theme
2. Use ← → to browse
3. Changes apply immediately

---

### 💾 Save & Load

**5 Save Slots Per Game**

**Saving:**
- Automatic at pause
- Manual save on quit
- Saves score, progress, state

**Loading:**
1. Main Menu → Load Game
2. Choose game
3. Select save slot
4. Resume where you left off

**Save Info Shows:**
- Save date/time
- Current score
- Game progress
- Custom metadata

**Deleting Saves:**
- Select slot
- Press D to delete
- Confirms before deletion

---

## Tips & Tricks

### General Tips

1. **Start with Easy Games**
   - Try Snake or Tic-Tac-Toe first
   - Build confidence
   - Learn controls

2. **Use Practice Mode**
   - Set difficulty to Easy
   - Learn game mechanics
   - Increase difficulty gradually

3. **Complete Daily Challenges**
   - Free rewards
   - Try different games
   - Build streaks

4. **Check Achievements**
   - Natural goals
   - Varied gameplay
   - Sense of progression

5. **Customize Settings**
   - Find your preferred speed
   - Choose comfortable theme
   - Adjust difficulty as you improve

### Advanced Strategies

1. **Master One Game**
   - Deep understanding
   - High score potential
   - Mastery achievements

2. **Rotate Games**
   - Prevents burnout
   - Varied skills
   - More achievements

3. **Track Your Progress**
   - Review statistics
   - Identify improvements
   - Set goals

4. **Save Before Risky Moves**
   - Experiment safely
   - Learn patterns
   - Try new strategies

### Performance Optimization

1. **Terminal Size**
   - Use at least 80x24
   - Larger is better for some games
   - Adjust font size if needed

2. **Terminal Emulator**
   - Use modern emulator
   - Enable colors
   - Smooth rendering

3. **Performance**
   - Close background apps
   - Reduce terminal transparency
   - Lower animation settings if laggy

---

## Troubleshooting

### Common Issues

#### Terminal Too Small
**Problem:** Error message about terminal size

**Solution:**
- Resize terminal to at least 80x24
- Reduce font size
- Maximize terminal window
- Check minimum size for specific game

#### Colors Not Showing
**Problem:** Games appear in black and white

**Solution:**
- Verify terminal supports colors
- Check terminal settings
- Try different theme
- Enable color support in terminal

#### Game Crashes
**Problem:** Game exits unexpectedly

**Solution:**
- Update Python to latest version
- Check terminal compatibility
- Verify curses support
- Report issue with error message

#### Data Not Saving
**Problem:** Scores/settings not persisting

**Solution:**
- Check write permissions in directory
- Verify `data/` directory exists
- Check disk space
- Review error logs

#### Slow Performance
**Problem:** Lag or slow rendering

**Solution:**
- Close other applications
- Reduce terminal transparency
- Use simpler theme
- Lower game speed setting

### Error Messages

#### "Terminal too small"
- Resize terminal
- Game shows required size

#### "Failed to initialize curses"
- Terminal doesn't support curses
- Try different terminal emulator

#### "Unable to save data"
- Check file permissions
- Verify disk space
- Check data directory

### Getting Help

1. **In-Game Help**
   - Press H during games
   - Access Help menu
   - View controls and tips

2. **Documentation**
   - Read README.md
   - Check API.md for technical details
   - Review CHANGELOG.md for updates

3. **Report Issues**
   - Note error message
   - Include terminal info
   - Describe steps to reproduce

---

## Keyboard Reference Card

### Universal Controls
| Key | Action |
|-----|--------|
| ↑↓← → | Navigate/Move |
| Enter | Select/Confirm |
| Space | Action/Select |
| P | Pause |
| Q | Quit |
| H | Help (in some games) |

### Game-Specific
| Game | Special Keys |
|------|--------------|
| Tetris | ↑/Space = Rotate |
| 2048 | R = Restart |
| Minesweeper | F = Flag |
| Pong | A = Toggle AI |
| Tic-Tac-Toe | M = Toggle Mode |
| Wordle | Backspace = Delete |
| Hangman | A-Z = Guess |
| Sudoku | 1-9 = Numbers |

---

## Quick Start Checklist

- [ ] Launch game collection
- [ ] Try a simple game (Snake or Tic-Tac-Toe)
- [ ] Check out Settings menu
- [ ] View your Statistics
- [ ] Browse Achievements
- [ ] Complete a Daily Challenge
- [ ] Save a game
- [ ] Try different themes
- [ ] Aim for a high score!

---

**Enjoy your gaming experience!** 🎮

For more information:
- [README.md](README.md) - Project overview
- [DEVELOPER.md](DEVELOPER.md) - For contributors
- [API.md](API.md) - Technical documentation

*Have fun and game on!*

