from collections import Counter
from typing import List, Tuple, Dict, Optional
import pandas as pd
import csv

# ============================================================================
# Constants (Change these on updates)
# ============================================================================
# Origin
ORIGIN = NOBLE, GOBLIN, CLAN, UNDEAD, ACE, PEKKA, GIANT = (
    "noble",
    "goblin",
    "clan",
    "undead",
    "ace",
    "pekka",
    "giant",
)

# Roles
ROLE = BRUTALIST, ASSASSIN, RANGER, BLASTER, BRAWLER, SUPERSTAR = (
    "brutalist",
    "assassin",
    "ranger",
    "blaster",
    "brawler",
    "superstar",
)

LEVELS = {
    GOBLIN: [2, 4],
    ASSASSIN: [2, 4],
    PEKKA: [2],
    BRAWLER: [2, 4],
    UNDEAD: [2, 4],
    SUPERSTAR: [2, 4],
    CLAN: [2, 4],
    BRUTALIST: [2, 4],
    NOBLE: [2, 4],
    BLASTER: [2, 4],
    GIANT: [2],
    RANGER: [2, 4],
    ACE: [2, 4],
}

CHARACTERS = {
    "goblins": [GOBLIN, ASSASSIN],
    "spear_gobs": [GOBLIN, BLASTER],
    "barbarians": [CLAN, BRAWLER],
    "skele_drag": [UNDEAD, RANGER],
    "musketeer": [NOBLE, SUPERSTAR],
    "valkyrie": [CLAN, BRUTALIST],
    "pekka": [PEKKA, BRAWLER],
    "wizard": [CLAN, BLASTER],
    "mini_pekka": [PEKKA, BRUTALIST],
    "prince": [NOBLE, BRAWLER],
    "dart_goblin": [GOBLIN, RANGER],
    "elec_giant": [GIANT, SUPERSTAR],
    "executioner": [ACE, BLASTER],
    "princess": [NOBLE, BLASTER],
    "mega_knight": [ACE, BRAWLER],
    "royal_ghost": [UNDEAD, ASSASSIN],
    "bandit": [ACE, ASSASSIN],
    "gob_machine": [GOBLIN, BRUTALIST],
    "skele_king": [UNDEAD, BRUTALIST],
    "gold_knight": [NOBLE, ASSASSIN],
    "archer_queen": [CLAN, RANGER],
    "monk": [ACE, SUPERSTAR],
    "royal_giant": [GIANT, RANGER],
    "witch": [UNDEAD, SUPERSTAR],
}

# ============================================================================
# CONFIGURATION
# ============================================================================
NUM_CHARACTERS = 6
# Example: DUMMY = [NOBLE, UNDEAD] OR DUMMY = None
DUMMY = None
# ============================================================================


class SearchOptimizer:
    def __init__(self, characters: Dict[str, List[str]], levels: Dict[str, List[int]]):
        self.characters = characters
        self.levels = levels
        self.l2_capable_traits = {trait for trait, lvls in levels.items() if max(lvls) >= 4}
        self.explored_count = 0

    def calculate_active_traits(self, trait_counts: Counter) -> Tuple[List[str], int, int]:
        """
        Calculate active traits (only highest level per trait)
        Returns: (trait_list, num_l1, num_l2)
        """
        active_traits = {}

        for trait, count in trait_counts.items():
            if trait in self.levels:
                highest_level = None
                for level_req in sorted(self.levels[trait], reverse=True):
                    if count >= level_req:
                        highest_level = level_req
                        break

                if highest_level:
                    active_traits[trait] = highest_level

        # Count traits by level
        num_l1 = sum(1 for level in active_traits.values() if level == 2)
        num_l2 = sum(1 for level in active_traits.values() if level == 4)

        trait_list = sorted([f"{trait}_{level}" for trait, level in active_traits.items()])

        return trait_list, num_l1, num_l2

    def search_0_l2(self, num_chars: int, dummy: Optional[List[str]] = None) -> List[Dict]:
        """
        Search for teams with 0 L2 traits (each trait appears at most 2 times)
        Strategy: DFS with constraint that no trait exceeds 2 occurrences
        """
        print(f"\nSearching for 0 L2 teams...")
        self.explored_count = 0
        best_teams = []
        max_traits = 0

        def get_trait_counts(team):
            counts = Counter()
            for char in team:
                for trait in self.characters[char]:
                    counts[trait] += 1
            if dummy:
                for trait in dummy:
                    counts[trait] += 1
            return counts

        def dfs(team: List[str], remaining: List[str], trait_counts: Counter):
            nonlocal max_traits, best_teams
            self.explored_count += 1

            # Base case: team is full
            if len(team) == num_chars:
                active_traits, num_l1, num_l2 = self.calculate_active_traits(trait_counts)
                if num_l2 == 0:  # Pure L1
                    total = len(active_traits)
                    if total > max_traits:
                        max_traits = total
                        best_teams = [
                            {
                                "characters": sorted(team),
                                "dummy": dummy,
                                "active_traits": active_traits,
                                "num_l1": num_l1,
                                "num_l2": num_l2,
                                "total_traits": total,
                                "trait_counts": dict(trait_counts),
                            }
                        ]
                    elif total == max_traits:
                        best_teams.append(
                            {
                                "characters": sorted(team),
                                "dummy": dummy,
                                "active_traits": active_traits,
                                "num_l1": num_l1,
                                "num_l2": num_l2,
                                "total_traits": total,
                                "trait_counts": dict(trait_counts),
                            }
                        )
                return

            # Pruning: if we can't possibly beat max_traits, stop
            slots_left = num_chars - len(team)
            max_possible = len([t for t in trait_counts if trait_counts[t] > 0]) + slots_left * 2
            if max_possible <= max_traits:
                return

            # Try adding each remaining character
            for i, char in enumerate(remaining):
                origin, role = self.characters[char]

                # Constraint: no trait should exceed 2 (to avoid L2)
                if trait_counts[origin] >= 2 or trait_counts[role] >= 2:
                    continue

                # Add character
                new_counts = trait_counts.copy()
                new_counts[origin] += 1
                new_counts[role] += 1

                dfs(team + [char], remaining[i + 1 :], new_counts)

        # Start DFS
        all_chars = sorted(self.characters.keys())
        initial_counts = Counter()
        if dummy:
            for trait in dummy:
                initial_counts[trait] += 1

        dfs([], all_chars, initial_counts)

        print(f"  Explored {self.explored_count} states")
        print(f"  Found {len(best_teams)} optimal teams with {max_traits} traits")

        # Deduplicate by character set
        seen = set()
        unique_teams = []
        for team in best_teams:
            team_id = tuple(sorted(team["characters"]))
            if team_id not in seen:
                seen.add(team_id)
                unique_teams.append(team)

        return unique_teams

    def search_n_l2(self, num_chars: int, target_l2_count: int, dummy: Optional[List[str]] = None) -> List[Dict]:
        """
        Search for teams with exactly target_l2_count L2 traits (level 4)
        """
        print(f"\nSearching for {target_l2_count} L2 teams...")
        self.explored_count = 0
        all_teams = {}  # Use dict to deduplicate
        max_traits = 0

        # Get traits that can reach L2 (level 4)
        l2_candidates = [(t, 4) for t in self.l2_capable_traits]

        def get_trait_counts(team):
            counts = Counter()
            for char in team:
                for trait in self.characters[char]:
                    counts[trait] += 1
            if dummy:
                for trait in dummy:
                    counts[trait] += 1
            return counts

        def search_with_l2_targets(l2_targets: List[Tuple[str, int]]):
            """Search for teams achieving specific L2 targets"""
            nonlocal max_traits, all_teams

            target_traits = {t[0]: t[1] for t in l2_targets}

            def dfs(team: List[str], remaining: List[str], trait_counts: Counter):
                nonlocal max_traits, all_teams
                self.explored_count += 1

                # Base case
                if len(team) == num_chars:
                    # Check if we achieved all L2 targets (exactly 4+)
                    achieved = True
                    for trait, req in target_traits.items():
                        if trait_counts[trait] < 4:
                            achieved = False
                            break

                    if achieved:
                        active_traits, num_l1, num_l2 = self.calculate_active_traits(trait_counts)
                        if num_l2 == target_l2_count:
                            total = len(active_traits)
                            team_id = tuple(sorted(team))

                            # Only add if new team
                            if team_id not in all_teams:
                                if total > max_traits:
                                    max_traits = total

                                all_teams[team_id] = {
                                    "characters": sorted(team),
                                    "dummy": dummy,
                                    "active_traits": active_traits,
                                    "num_l1": num_l1,
                                    "num_l2": num_l2,
                                    "total_traits": total,
                                    "trait_counts": dict(trait_counts),
                                }
                    return

                # Pruning
                slots_left = num_chars - len(team)

                # Check if we can still achieve L2 targets
                for trait, req in target_traits.items():
                    if trait_counts[trait] + slots_left < req:
                        return  # Can't reach target

                # Try adding characters
                for i, char in enumerate(remaining):
                    origin, role = self.characters[char]

                    # Add character
                    new_counts = trait_counts.copy()
                    new_counts[origin] += 1
                    new_counts[role] += 1

                    dfs(team + [char], remaining[i + 1 :], new_counts)

            all_chars = sorted(self.characters.keys())
            initial_counts = Counter()
            if dummy:
                for trait in dummy:
                    initial_counts[trait] += 1

            dfs([], all_chars, initial_counts)

        # Try different combinations of L2 target traits
        from itertools import combinations

        for l2_combo in combinations(l2_candidates, target_l2_count):
            search_with_l2_targets(list(l2_combo))

        # Filter to only max traits
        best_teams = [team for team in all_teams.values() if team["total_traits"] == max_traits]

        print(f"  Explored {self.explored_count} states")
        print(f"  Found {len(best_teams)} optimal teams with {max_traits} traits")

        return best_teams

    def calculate_max_l2_traits(self, num_chars: int, dummy: Optional[List[str]] = None) -> int:
        """
        Calculate maximum possible L2 traits
        Each L2 requires 4 characters minimum
        Max intersections:
        - Without dummy: 2 (one L2 origin can share with one L2 role)
        - With dummy: 3 (dummy can bridge both)
        Formula: For N L2 traits, need at least 4*N - max_intersections characters
        """
        total_chars = num_chars
        if dummy:
            total_chars += 1

        max_intersections = 3 if dummy else 2
        max_l2 = (total_chars + max_intersections) // 4
        max_l2 = min(max_l2, len(self.l2_capable_traits))

        return max_l2

    def find_all_optimal_teams(self, num_chars: int, dummy: Optional[List[str]] = None) -> Dict[str, List[Dict]]:
        """Find all optimal teams for each L1/L2 category"""
        result = {}

        # Calculate maximum possible L2 traits
        max_l2 = self.calculate_max_l2_traits(num_chars, dummy)
        print(f"\nMaximum possible L2 traits: {max_l2}")

        # Search for 0 L2 (pure L1)
        teams_0 = self.search_0_l2(num_chars, dummy)
        if teams_0:
            result["0l2"] = teams_0

        # Search for L2
        for l2_count in range(1, max_l2 + 1):
            teams = self.search_n_l2(num_chars, l2_count, dummy)
            if teams:
                result[f"{l2_count}l2"] = teams

        return result

    def export_to_csv(self, teams_dict: Dict[str, List[Dict]], base_filename: str = "teams"):
        """Export teams to CSV files"""
        for category, teams in sorted(teams_dict.items()):
            if not teams:
                continue

            filename = f"{base_filename}_{category}.csv"

            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)

                max_troops = max(len(team["characters"]) for team in teams)
                max_traits = max(len(team["active_traits"]) for team in teams)

                troop_headers = [f"troop{i+1}" for i in range(max_troops)]
                trait_headers = [f"trait{i+1}" for i in range(max_traits)]

                if teams[0]["dummy"]:
                    troop_headers.append("dummy")

                header = troop_headers + ["->"] + trait_headers
                writer.writerow(header)

                for team in teams:
                    row = []
                    row.extend(team["characters"])
                    row.extend([""] * (max_troops - len(team["characters"])))

                    if team["dummy"]:
                        dummy_str = f"{team['dummy'][0]}+{team['dummy'][1]}"
                        row.append(dummy_str)

                    row.append("->")
                    row.extend(team["active_traits"])
                    row.extend([""] * (max_traits - len(team["active_traits"])))

                    writer.writerow(row)

            print(f"  Exported {len(teams)} teams to {filename}")


def main():

    print("=" * 80)
    print("CHARACTER TRAIT GRID")
    print("=" * 80)
    trait_grid = pd.DataFrame(index=ORIGIN, columns=ROLE, dtype="string")
    for char in CHARACTERS:
        o,r = CHARACTERS[char]
        trait_grid.at[o,r] = char
    print(trait_grid.fillna("-"))

    optimizer = SearchOptimizer(CHARACTERS, LEVELS)

    print("=" * 80)
    print("TRAIT OPTIMIZATION - SEARCH ALGORITHM APPROACH")
    print("=" * 80)
    print(f"Number of characters: {NUM_CHARACTERS}")
    print(f"Dummy: {DUMMY if DUMMY else 'None'}")
    print("=" * 80)

    # Find optimal teams
    optimal_teams = optimizer.find_all_optimal_teams(NUM_CHARACTERS, DUMMY)

    print("\n" + "=" * 80)
    print("RESULTS BY L2 TRAIT COUNT")
    print("=" * 80)

    for category in sorted(optimal_teams.keys()):
        teams = optimal_teams[category]
        if teams:
            num_l1 = teams[0]["num_l1"]
            num_l2 = teams[0]["num_l2"]
            total = teams[0]["total_traits"]

            # Build composition string
            parts = []
            if num_l1 > 0:
                parts.append(f"{num_l1} L1")
            if num_l2 > 0:
                parts.append(f"{num_l2} L2")
            trait_breakdown = " + ".join(parts) + f" = {total} total"

            print(f"\n{category.upper()}: {len(teams)} teams")
            print(f"  Composition: {trait_breakdown}")

            for i, team in enumerate(teams[:3], 1):
                print(f"\n  Example {i}:")
                print(f"    Characters: {', '.join(team['characters'])}")
                if team["dummy"]:
                    print(f"    Dummy: {team['dummy'][0]} + {team['dummy'][1]}")
                print(f"    Active Traits: {', '.join(team['active_traits'])}")

    print("\n" + "=" * 80)
    print("EXPORTING TO CSV")
    print("=" * 80)
    base_filename = f"{NUM_CHARACTERS}chars{'_with_dummy' if DUMMY else ''}"

    optimizer.export_to_csv(optimal_teams, base_filename)

    print("\n" + "=" * 80)
    print("COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
