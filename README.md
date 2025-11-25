# Clash Royale Merge Tactics — Best Team Composition Finder

This Python script calculates the **best team compositions** in *Clash Royale: Merge Tactics* based on origin-role synergies and tier bonuses. It evaluates all X-character combinations to find the ones that yield the **highest synergy score**.

---

## 🧩 Overview

The script systematically goes through every possible team of X characters, and writes the best combinations to a text file.

It uses the synergy logic between **Origins** and **Roles**, assigning scores to teams that meet specific thresholds (tier levels).

---

## ⚙️ How It Works

### 1. **Scoring System**

Each team is scored based on how many synergies they activate.
The following constants define how scoring works:

```python
NUM_CHARACTERS = int       # Team size
DUMMY = [Trait1, Trait2]   # dummy's trait
```

For example:
NUM_CHARACTERS = 7
DUMMY = [NOBLE, UNDEAD]

### 2. **Origins and Roles**

Each character has two attributes: an *Origin* and a *Role*.
When enough team members share the same attribute, a synergy tier is activated.

Example:

```python
"goblins": [GOBLIN, ASSASSIN],
"spear_gobs": [GOBLIN, BLASTER],
```

---

## 📊 Output Files

The script writes results to text files depending on the scoring configuration:

| File                             | Description                           |
| -------------------------------- | ------------------------------------- |
| `7chars_0_l2.csv`                | Only Tier 1 synergies                 |
| `7chars_dummy_0_l2.csv`          | Only Tier 1 synergies, with dummy     |
| `7chars_1_l2.csv`                | Tier 2 + Tier 1 synergies             |
| `7chars_dummy_1_l2.csv`          | Tier 2 + Tier 1 synergies, with dummy | 
| `7chars_2_l2.csv`                | 2 Tier 2 synergies                    |
| `7chars_dummy_2_l2.csv`          | 2 Tier 2 synergies, with dummy        |

Each line in these files lists:

```
[team of X characters] ,->, [synergies activated]
```

Example:

```
gob_machine,mega_knight,pekka,prince,spear_gobs,valkyrie,witch,noble+undead,->,ace_2,avenger_2,brawler_2,goblin_2,juggernaut_2,noble_2,undead_2
```

---

## 🚀 How to Run

1. **Install Python 3.10+**
2. **Run the script:**

   ```bash
   python mergeTactic.py
   ```
3. The program prints:
   * Grid of Characters
   * The **best synergy score**
   * A **ranking of most frequently used characters** in top teams
4. The full list of top-scoring teams is saved to the output files defined in:

   ```python
   filename = f"{base_filename}_{category}.csv"
   ```

---

## 🧠 Example Console Output

```
================================================================================
CHARACTER TRAIT GRID
================================================================================
          brutalist     assassin        ranger      blaster      brawler   superstar
noble             -  gold_knight             -     princess       prince   musketeer
goblin  gob_machine      goblins   dart_goblin   spear_gobs            -           -
clan       valkyrie            -  archer_queen       wizard   barbarians           -
undead   skele_king  royal_ghost    skele_drag            -            -       witch
ace               -       bandit             -  executioner  mega_knight        monk
pekka    mini_pekka            -             -            -        pekka           -
giant             -            -   royal_giant            -            -  elec_giant
================================================================================
TRAIT OPTIMIZATION - SEARCH ALGORITHM APPROACH
================================================================================
Number of characters: 7
Dummy: None
================================================================================

Maximum possible L2 traits: 2

Searching for 0 L2 teams...
  Explored 287758 states
  Found 5772 optimal teams with 6 traits

Searching for 1 L2 teams...
  Explored 789411 states
  Found 412 optimal teams with 5 traits

Searching for 2 L2 teams...
  Explored 1525985 states
  Found 20 optimal teams with 2 traits

================================================================================
RESULTS BY L2 TRAIT COUNT
================================================================================

0L2: 5772 teams
  Composition: 6 L1 = 6 total

  Example 1:
    Characters: archer_queen, bandit, barbarians, dart_goblin, elec_giant, goblins, mega_knight
    Active Traits: ace_2, assassin_2, brawler_2, clan_2, goblin_2, ranger_2

  Example 2:
    Characters: archer_queen, bandit, barbarians, dart_goblin, elec_giant, goblins, monk
    Active Traits: ace_2, assassin_2, clan_2, goblin_2, ranger_2, superstar_2

  Example 3:
    Characters: archer_queen, bandit, barbarians, dart_goblin, executioner, goblins, pekka
    Active Traits: ace_2, assassin_2, brawler_2, clan_2, goblin_2, ranger_2

1L2: 412 teams
  Composition: 4 L1 + 1 L2 = 5 total

  Example 1:
    Characters: archer_queen, bandit, dart_goblin, executioner, gob_machine, goblins, spear_gobs
    Active Traits: ace_2, assassin_2, blaster_2, goblin_4, ranger_2

  Example 2:
    Characters: archer_queen, bandit, dart_goblin, gob_machine, goblins, spear_gobs, valkyrie
    Active Traits: assassin_2, brutalist_2, clan_2, goblin_4, ranger_2

  Example 3:
    Characters: archer_queen, bandit, dart_goblin, gob_machine, goblins, spear_gobs, wizard
    Active Traits: assassin_2, blaster_2, clan_2, goblin_4, ranger_2

2L2: 20 teams
  Composition: 2 L2 = 2 total

  Example 1:
    Characters: bandit, dart_goblin, gob_machine, goblins, gold_knight, royal_ghost, spear_gobs
    Active Traits: assassin_4, goblin_4

  Example 2:
    Characters: dart_goblin, executioner, gob_machine, goblins, princess, spear_gobs, wizard
    Active Traits: blaster_4, goblin_4

  Example 3:
    Characters: archer_queen, dart_goblin, gob_machine, goblins, royal_giant, skele_drag, spear_gobs
    Active Traits: goblin_4, ranger_4

================================================================================
EXPORTING TO CSV
================================================================================
  Exported 5772 teams to 7chars_0l2.csv
  Exported 412 teams to 7chars_1l2.csv
  Exported 20 teams to 7chars_2l2.csv

================================================================================
COMPLETE
================================================================================
```

---

## 🛠️ Customize

You can adjust:

* `NUM_CHARACTERS` for other team sizes.
* `CHARACTERS` or `LEVELS` dictionaries to reflect new updates.

---

## 📁 File Structure

```
merge_tactic_traits
├── 6chars_0l2.csv              # Precomputed 6 characters Tier 1 only results
├── 6chars_1l2.csv              # Precomputed 6 characters 1 Tier 2 results
├── 7chars_0l2.csv              # Precomputed 7 characters Tier 1 only results
├── 7chars_1l2.csv              # Precomputed 7 characters 1 Tier 2 results
├── 7chars_2l2.csv              # Precomputed 7 characters 2 Tier 2 results
├── mergeTactic.py              # Main script
├── mergeTacticL3.py            # Old script (with L3)
└── README.md
```

---

## 🧩 Notes

* Depending on your hardware, execution time can vary, since there are thousands of combinations.
* Output files can be large if many teams tie for top score.

---
