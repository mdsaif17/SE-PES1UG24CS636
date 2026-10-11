# Name: T Mohammed Saif
# SRN : PES1UG24CS636

# Lab 4: VibeCoding - Dig Dug Repair

A Python/Pygame Dig Dug clone (`game.py`) with one deliberate bug fixed and three missing features implemented, using an AI assistant (Claude) as a pair-programming partner.

## Submission contents

| File | Description |
|---|---|
| `before.mp4` | 10-second gameplay video of the original game, before any changes |
| `after.mp4` | 10-second gameplay video of the completed game |
| `game.py` | Final source code |
| `chat-history.pdf` | Exported complete AI chat history |

## How to run

Requires Python 3.10 or newer.

```bash
python -m pip install pygame
python game.py
```

Controls: arrow keys to dig/move, Space to pump, `R` to reset.

## The bug

**Location:** `bfs_path()` in `game.py`.

**Problem:** the search used `queue.pop()`, which removes from the **right** end of the deque. New cells are also added on the right (`queue.append`), so the queue behaved like a stack (last in, first out). That made the search depth-first, and enemies took long, winding routes through the tunnels.

**Fix:** use `queue.popleft()`, which removes from the **left** end (first in, first out). Breadth-first search then explores all cells 1 step away, then 2 steps away, and so on, so the first time it reaches the player it has found the shortest route.

In a test on a cleared room, routes of 12, 22, 22 and 9 steps became 4, 10, 10 and 5, which are the shortest possible.

## Features implemented

### 1. `dirt_color(row)`
Returns one flat color for each underground depth band, or `None` outside the bands so the default gradient is still used.

| Rows | Color | Meaning |
|---|---|---|
| 1-3 | `(196, 152, 92)` | topsoil (sandy tan) |
| 4-6 | `(176, 106, 48)` | clay (orange-brown) |
| 7-9 | `(128, 60, 80)` | deep rock (maroon) |
| 10-13 | `(70, 85, 130)` | bedrock (slate blue) |

All values are valid RGB (0-255). The colors stay clearly different from the dark tunnels and the red enemies, so gameplay stays readable.

### 2. `on_enemy_popped(enemy, score)`
When an enemy pops, a burst of 26 colored particles flies out from the enemy's cell.

- Particles are stored in a module-level `PARTICLES` list and updated every frame using the game's own `dt` (no `time.sleep()`, nothing blocks).
- Each particle moves, falls slightly, shrinks, and is removed when its life runs out (about 0.4-0.9 seconds).
- The list is capped at 400 particles, so many pops at once cannot crash or slow the game.
- The effect runs inside the existing update and draw loop, using the same pixel formula as the rest of the game (`col * TILE + TILE // 2`).
- The callback awards no points. The existing scoring line is unchanged, so points are never counted twice.

### 3. `enemy_speed_multiplier(level)`
Returns `max(0.1, 1 + 0.1 * level)`, so enemies are 10% faster per level (1.1x at level 1, 1.5x at level 5, 2.0x at level 10). The `max()` guard keeps the value positive for any input. The ghost slowdown and the locked (inflated) enemy behavior are unchanged.

## Tests performed

Automated checks, run headless with `SDL_VIDEODRIVER=dummy`:

- **Pathfinding:** 4 start/goal pairs compared against an independent shortest-path calculation, all shortest after the fix.
- **Dirt colors:** rows 1-13 return valid RGB tuples, rows outside the range return `None`, the 4 bands are distinct, and rendered pixels match.
- **Particles:** spawn position, animation over many frames, expiry, 100 simultaneous pops (capped at 400), exact score awarded once (+300 for a row-5 enemy), level change on the last pop, reset, and game-over behavior.
- **Speed:** values for levels 1-10 strictly increase and stay positive, step delay shrinks with level, ghosts keep their 1.6x slowdown, and locked enemies are unaffected.
- **Gameplay regression:** player movement and digging, pump inflating and deflating, lives, game over, reset, level progression, and an enemy chasing the player through a tunnel.
- **Smoke test:** the real `main()` loop ran for about 1.5 seconds and exited cleanly.

Manual verification (visual): see `after.mp4`. Run `python game.py` and check that:

1. The dirt shows four color bands from top to bottom.
2. Enemies take short routes through dug tunnels.
3. Pumping an enemy 4 times pops it, shows a particle burst and adds score.
4. Stopping the pump lets an enemy deflate.
5. Enemies move faster on higher levels.
6. Losing all 3 lives shows GAME OVER, and `R` resets the game.

## Git commit history

One commit per task, in this order:

1. `Fix bfs_path: use popleft() so BFS explores in FIFO order`
2. `Implement dirt_color: distinct colour band per underground depth`
3. `Implement on_enemy_popped: animated particle burst when an enemy pops`
4. `Implement enemy_speed_multiplier: enemies get 10% faster each level`

Run `git log --oneline` to see the hashes in this repository.
