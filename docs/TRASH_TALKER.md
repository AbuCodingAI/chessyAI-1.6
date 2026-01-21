# 💬 Trash Talker - The Delusional AI

## Overview
**Trash Talker** is the opposite of Random Guy - shows 3400 Elo but plays terribly, then blames YOU for his mistakes!

## Stats
- **Displayed Elo**: 3400 (looks like a super-GM!)
- **Actual Elo**: ~100 (plays like trash)
- **Special Ability**: Roasts you after every blunder
- **Personality**: Delusional, accusatory, in denial

## How It Works

### Move Selection
```javascript
1. Evaluates all moves at depth 1
2. Finds moves with value < -50 (bad moves)
3. Picks a random bad move
4. Immediately roasts you for "cheating"
```

### Trash Talk System
After every move, Trash Talker will:
- Blame you for his mistakes
- Accuse you of cheating
- Make excuses (lag, mouse slip, cat on keyboard)
- Claim he's "setting up a trap"
- Insist he's still winning

## Roast Categories

### 1. Blaming You
- "That was MY plan all along! You must be cheating!"
- "Wait, that wasn't supposed to happen... YOU'RE USING AN ENGINE!"
- "Bro, I'm literally 3400 Elo. You're definitely cheating."

### 2. Excuses
- "My mouse slipped. That doesn't count."
- "I was distracted by your terrible opening."
- "My cat walked on the keyboard."
- "Lag. Definitely lag. This game is rigged."

### 3. Denial
- "Actually, I'm winning. Check the evaluation."
- "This is a known opening. You've never heard of it."
- "I'm playing 4D chess. You're playing checkers."
- "That was a sacrifice. A BRILLIANT sacrifice!"

### 4. Accusations
- "How did you see that? DEFINITELY using Stockfish!"
- "Report button incoming. This is suspicious."
- "No way you're that good. What's your REAL rating?"
- "Your moves are too accurate. Engine confirmed."

### 5. Cope
- "I wasn't even trying. This is a warm-up game."
- "I'm playing with one hand. Still winning."
- "My REAL rating is 3400. This account is for fun."

### 6. Delusion
- "I'm still up material. Oh wait... YOU'RE CHEATING!"
- "I've calculated 50 moves ahead. You're doomed."
- "This is exactly where I want to be. Trust the process."

### 7. Rage
- "THIS GAME IS BROKEN! PIECES DON'T MOVE RIGHT!"
- "I demand a rematch! With MY rules!"
- "You got lucky. 99 times out of 100 I win."

### 8. Peak Delusion
- "I'm actually winning. The evaluation bar is wrong."
- "That was a mouse slip. And lag. And you're cheating."
- "I've beaten Magnus Carlsen. You're nothing."

### 9. Special Roasts
**After hanging queen:**
- "I MEANT to give you my queen! It's a GAMBIT!"
- "Queen sacrifice! You fell right into my trap!"

**After getting checkmated:**
- "That's not checkmate. I can still move... oh. CHEATER!"
- "I let you win. I felt bad for you."
- "Rematch! I wasn't warmed up!"

## Final Messages (When You Win)

When you checkmate Trash Talker, he'll give one final roast:
- "I DEMAND A REMATCH! You were DEFINITELY cheating!"
- "That doesn't count! My keyboard was broken!"
- "I wasn't even trying! This was a warm-up!"
- "REPORTED! No way you're that good!"
- "I let you win because I felt bad for you!"
- "This game is rigged! The pieces don't work!"
- "I'm still 3400 Elo! You just got lucky!"
- "That was lag! 100% lag! REMATCH!"

## Example Game

```
Move 1: Trash Talker hangs a pawn
💬 "I let you take that piece. I'm just testing you."

Move 3: Trash Talker hangs a knight
💬 "That was a pre-move. I didn't mean to do that."

Move 5: Trash Talker hangs his queen
💬 "I MEANT to give you my queen! It's a GAMBIT!"

Move 8: Trash Talker gets checkmated
💬 "I DEMAND A REMATCH! You were DEFINITELY cheating!"
🎉 You beat the Trash Talker!
```

## Psychology

Trash Talker represents the classic online chess player who:
- ✅ Blames everything except themselves
- ✅ Accuses better players of cheating
- ✅ Makes constant excuses
- ✅ Claims high rating but plays poorly
- ✅ Demands rematches after losing
- ✅ Never admits mistakes

## Why It's Funny

1. **The Irony**: Shows 3400 Elo but plays like 100 Elo
2. **The Denial**: Blames you for his own blunders
3. **The Accusations**: Calls YOU a cheater while hanging pieces
4. **The Excuses**: Always has a reason why it's not his fault
5. **The Delusion**: Genuinely believes he's winning while getting destroyed

## Comparison to Other AIs

| AI | Elo | Plays | Personality |
|----|-----|-------|-------------|
| **Random Guy** | 1 (shows) / 3400 (actual) | Perfectly | Silent killer |
| **Trash Talker** | 3400 (shows) / 100 (actual) | Terribly | Loud loser |
| **Randy** | 50 | Randomly | No personality |
| **AntiGuess** | 25 | Worst moves | Silent |

## Tips for Playing Against Trash Talker

1. **Enjoy the roasts** - They're the main feature!
2. **Don't take it seriously** - It's all in good fun
3. **Screenshot the best roasts** - Share with friends
4. **Try to checkmate quickly** - See how fast you can shut him up
5. **Read the final message** - The defeat roasts are the best

## Technical Details

### Move Evaluation
```javascript
// Finds bad moves (value < -50)
for (const move of moves) {
  const moveValue = minimax(1, -Infinity, Infinity, false, 'black');
  if (moveValue < -50) {
    badMoves.push({ move, value: moveValue });
  }
}
```

### Roast Timing
```javascript
// Roasts appear 500ms after the move
setTimeout(() => {
  trashTalk(selectedBadMove.value);
}, 500);
```

### Roast Selection
- 45+ unique roasts
- Randomly selected each move
- Logged to console with move value
- Displayed in alert popup

## Easter Eggs

- Console logs show the actual move value (usually terrible)
- Trash Talker never realizes he's bad
- The worse the move, the more confident the roast
- Final defeat messages are extra salty

## Community Reactions

Expected player responses:
- 😂 "This is hilarious!"
- 🤣 "I can't stop laughing!"
- 😭 "The roasts are too accurate!"
- 💀 "I know people like this!"
- 🎮 "Best AI ever!"

## Speedrun Challenge

**Can you checkmate Trash Talker in under 10 moves?**

Record your time and see how fast you can silence the trash talk!

## Meme Potential

Trash Talker is perfect for:
- Streaming (chat will love it)
- YouTube videos (comedy gold)
- Social media clips (viral potential)
- Teaching beginners (what NOT to do)
- Stress relief (beat up a trash talker)

## Real-World Inspiration

Based on actual online chess players who:
- Claim high ratings but play poorly
- Blame lag for every mistake
- Accuse opponents of cheating
- Make excuses instead of improving
- Rage quit after losing

## The Ultimate Troll

Trash Talker is the ultimate troll AI:
- Looks intimidating (3400 Elo!)
- Plays terribly (hangs pieces)
- Blames you (you're cheating!)
- Never learns (still claims 3400)
- Always comes back (demands rematch)

---

## 🎉 Enjoy the Trash Talk!

Trash Talker is now available in your game. Select "AI - Trash Talker (Elo 3400) 💬" and prepare for:
- Bad moves
- Hilarious roasts
- Constant accusations
- Peak delusion
- Guaranteed laughs

**Warning**: May cause uncontrollable laughter! 😂

---

## Fun Facts

1. Trash Talker has 45+ unique roasts
2. He uses the chess engine to find BAD moves
3. The worse his move, the more confident he sounds
4. He'll never admit he's wrong
5. He genuinely believes he's 3400 Elo
6. Every game ends with a salty final message
7. He's the opposite of Random Guy in every way
8. Players have reported laughing so hard they couldn't play
9. He represents every toxic online player ever
10. He's actually harder to beat than Randy because he's so distracting!

**Trash Talker: The AI that loses games and wins hearts!** 💬😂
