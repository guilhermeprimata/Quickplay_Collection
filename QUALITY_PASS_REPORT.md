# Primata Web Quickplay — quality & balance pass

Automated repository pass applied in-place while preserving one self-contained HTML per game.

## 1. Adivinhe o Número — `advinhe_o_numero.html`
- ✅ timer HUD 180s → 90s (1 replacement)
- ✅ initial timer state 180s → 90s (1 replacement)
- ✅ reset timer state 180s → 90s (1 replacement)
- ✅ timer ring normalized to 90s (1 replacement)
- ✅ input constrained to the documented 0–1000 range
- ✅ invalid guesses no longer consume attempts or start the timer
- ✅ standard pause (Esc + modal with resume/new game/menu)

## 2. Arqueiro do Vale — `bow_and_arrow.html`
- ✅ rocket speed 71 → 66 (1 replacement)
- ✅ meteor speed 60 → 57 (1 replacement)
- ✅ dragon HP 5 → 4 (1 replacement)
- ✅ storm wind softened without removing weather challenge (1 replacement)
- ✅ standard pause (Esc + modal with resume/new game/menu) + toolbar New Game

## 3. Toxic Stench — `campo_minado.html`
- ✅ standard pause (Esc + modal with resume/new game/menu)
- ℹ️ classic minefield rules and current pacing retained; no gratuitous probability change

## 4. Click Speed — `click_speed.html`
- ✅ post-click lockout 1350ms → 750ms (1 replacement)
- ✅ standard pause (Esc + modal with resume/new game/menu) + toolbar New Game

## 5. Hipódromo Estelar — `corrida_de_cavalos.html`
- ✅ standard pause (Esc + modal with resume/new game/menu) + toolbar New Game
- ℹ️ horse variance/odds already bounded; economy retained to avoid converting fair randomness into hidden house bias

## 6. DROPWORKS — `dropworks.html`
- ✅ Reviewed; no source change needed.
- ℹ️ 40-stage moving-container/supply system was recently tuned; native pause/restart retained

## 7. Cosmo Crash — `foguetinho.html`
- ✅ obstacle spawn floor/pacing softened (1 replacement)
- ✅ standard pause (Esc + modal with resume/new game/menu) + toolbar New Game

## 8. Império Financeiro 8-bit — `idle_trader.html`
- ✅ standard pause (Esc + modal with resume/new game/menu)
- ℹ️ long-form economy/prestige curve retained; arbitrary rebalance would invalidate existing saves

## 9. Forca Neon — `jogo_da_forca.html`
- ✅ standard pause (Esc + modal with resume/new game/menu)
- ℹ️ gameplay pacing retained; repository still contains the stale pre-i18n banking dictionary and needs promotion of the already-approved 320-concept File Library version

## 10. Velha Quântica — `jogo_da_velha.html`
- ✅ 4×4 AI upgraded from random to tactical-but-beatable
- ✅ win score now rewards speed (1 replacement)
- ✅ score resets cleanly each round
- ✅ losses/draws no longer pollute the leaderboard
- ✅ record storage migrated away from legacy branded key (2 replacements)
- ✅ new records use neutral storage key (1 replacement)
- ✅ standard pause (Esc + modal with resume/new game/menu)

## 11. Kombo Blocks — `kombo_blocks.html`
- ✅ drop curve softened: .88 → .90 with saner minimum intervals (1 replacement)

## 12. Leaping Into Life — `leaping_into_life.html`
- ✅ standard pause (Esc + modal with resume/new game/menu) + toolbar New Game
- ℹ️ Pond/Marsh/Storm gap-speed matrix is progressive and readable; retained

## 13. Pulso Genius — `memory_genius.html`
- ✅ sequence playback now adapts 620ms → 360ms (1 replacement)
- ✅ mistake damage 34 → 30 (1 replacement)
- ✅ milestone recovery +12 → +15 (1 replacement)
- ✅ mistake recovery pause 650ms → 850ms (1 replacement)
- ✅ standard pause (Esc + modal with resume/new game/menu)

## 14. Pixel Bomber — `pixel_bomberman.html`
- ✅ complete gameplay core rebuild: safe spawn, fair bombs, collision invulnerability, level progression and meaningful scoring
- ✅ visible mobile D-pad + Bomb + Pause controls
- ✅ difficulty curve now scales enemies, pursuit and destructible density gradually
- ✅ standard pause (Esc + modal with resume/new game/menu) + toolbar New Game

## 15. Neon Pong — `pong.html`
- ✅ Strategist AI given slightly more human reaction/error (1 replacement)
- ✅ Master AI remains hard but less robotic (1 replacement)

## 16. Salve os Gatinhos! — `salve_os_gatinhos.html`
- ✅ standard pause (Esc + modal with resume/new game/menu) + toolbar New Game
- ℹ️ existing difficulty director already spaces spawns, adds wind gradually and includes life recovery; retained

## 17. Zen Sudoku — `sudoku.html`
- ✅ Sudoku generator now preserves a unique solution; difficulty targets 30/40/50 blanks
- ✅ standard pause (Esc + modal with resume/new game/menu) + toolbar New Game

## 18. The Worm — `the_worm.html`
- ✅ standard pause (Esc + modal with resume/new game/menu) + toolbar New Game
- ℹ️ Calm/Groove/Frenzy speed, wrap and poison matrix is already well separated; retained

## 19. Torre de Hanói — `torre_de_hanoi.html`
- ✅ standard pause (Esc + modal with resume/new game/menu)
- ℹ️ difficulty is naturally determined by 3–8 discs; no artificial timing pressure added

## 20. Tron: Domínio — `tron.html`
- ✅ standard pause (Esc + modal with resume/new game/menu)
- ℹ️ speed progression, life regeneration and AI randomness already form a controlled curve; retained

## Global checks

- Games audited: **20**
- Standard pause added where missing: **17**
- Native pause preserved without duplication: **DROPWORKS, Kombo Blocks, Neon Pong**
- Pixel Bomber now has keyboard + visible touch controls, staged difficulty and a complete restart flow.
- All changes stay inside each game's own HTML; no external runtime dependency was introduced.
- Known integration debt: **Forca Neon on GitHub is not the approved 320-concept everyday-language build already present in File Library.** This pass flags it rather than pretending the stale banking dictionary is correct.
