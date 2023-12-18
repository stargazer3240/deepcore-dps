from enum import Enum, auto
from dataclasses import dataclass
from typing import NamedTuple


@dataclass(frozen=True)
class Mod:
    name: str
    description: str


@dataclass(frozen=True)
class ModRow:
    A: Mod
    B: Mod
    C: Mod | None

    def __len__(self) -> int:
        if self.C:
            return 3
        return 2

    def __getitem__(self, mod_number: int) -> Mod:
        if not isinstance(mod_number, int):
            raise TypeError("Index must be an int")
        elif (
            mod_number < 0 or self.C and mod_number > 2 or not self.C and mod_number > 1
        ):
            raise IndexError("Index out of range!")

        if self.C:
            mods = (self.A, self.B, self.C)
        else:
            mods = (self.A, self.B)

        for i, mod in enumerate(mods):
            if i == mod_number:
                return mod

        return Mod("", "")


class ModTree(NamedTuple):
    T1: ModRow
    T2: ModRow
    T3: ModRow
    T4: ModRow
    T5: ModRow


class OverclockType(Enum):
    CLEAN = auto()
    BALANCED = auto()
    UNSTABLE = auto()


@dataclass(frozen=True)
class Overclock:
    type_: OverclockType | None
    name: str
    description: str


@dataclass
class Build:
    mod_selection: tuple[Mod, Mod, Mod, Mod, Mod] | None
    overclock: Overclock | None


type OverclockList = (
    tuple[Overclock, Overclock, Overclock, Overclock, Overclock]
    | tuple[Overclock, Overclock, Overclock, Overclock, Overclock, Overclock]
    | tuple[Overclock, Overclock, Overclock, Overclock, Overclock, Overclock, Overclock]
)


class DeepcoreGK2:
    NAME = "Deepcore GK2"
    DAMAGE = 16.0
    WEAKPOINT_STUN_DURATION = 1.5
    MAGAZINE_SIZE = 30
    MAX_AMMO = 360
    RATE_OF_FIRE = 8
    RELOAD_TIME = 1.8
    WEAKPONT_STUN_CHANCE = 0.15
    BASE_SPREAD = 1.0
    ARMOR_BREAKING = 1.0

    @staticmethod
    def _init_mod_tree() -> ModTree:
        tier1_A = Mod("Gyro Stabilisation", "x0 Base Spread")
        tier1_B = Mod("Supercharged Feed Mechanism", "+1 Rate of Fire")
        tier1_C = Mod("Quickfire Ejector", "x0.73 Reload Time")
        tier1 = ModRow(tier1_A, tier1_B, tier1_C)
        tier2_A = Mod("Increased Caliber Rounds", "+3 Damage")
        tier2_B = Mod("Expanded Ammo Bags", "+120 Max Ammo")
        tier2 = ModRow(tier2_A, tier2_B, None)
        tier3_A = Mod("Floating Barrel", "x0.5 Recoil, -0.65 Max Spread")
        tier3_B = Mod("High Capacity Magazine", "+10 Magazine Size")
        tier3 = ModRow(tier3_A, tier3_B, None)
        tier4_A = Mod("Hollow-Point Bullets", "+20% Weakspot Damage Bonus")
        tier4_B = Mod("Hardened Rounds", "+500% Armor Break Bonus")
        tier4 = ModRow(tier4_A, tier4_B, None)
        tier5_A = Mod("Battle Frenzy", "+Battle Frenzy")
        tier5_B = Mod("Improved Gas System", "+2 Rate of Fire")
        tier5_C = Mod("Stun", "+35% Stun Chance")
        tier5 = ModRow(tier5_A, tier5_B, tier5_C)
        return ModTree(tier1, tier2, tier3, tier4, tier5)

    MOD_TREE = _init_mod_tree()

    @staticmethod
    def _init_overclock_list() -> OverclockList:
        oc1 = Overclock(
            OverclockType.CLEAN,
            "Compact Ammo",
            "+5 Magazine Size, x0.7 Recoil",
        )
        oc2 = Overclock(
            OverclockType.CLEAN,
            "Gas Rerouting",
            "+1 Rate of Fire, x0.84 Reload Time",
        )
        oc3 = Overclock(
            OverclockType.CLEAN,
            "Homebrew Powder",
            "+Randomized Damage (between x0.8 and x1.4 damage)",
        )
        oc4 = Overclock(
            OverclockType.BALANCED,
            "Overclocked Firing Mechanism",
            "+3 Rate of Fire",
        )
        oc5 = Overclock(
            OverclockType.BALANCED,
            "Bullets of Mercy",
            "+50% Bonus Damage to Afflicted Targets (On Fire/Stun/Electrocution/Frozen/Neurotoxin), x0.6 Magazine Size",
        )
        oc6 = Overclock(
            OverclockType.UNSTABLE,
            "AI Stability Engine",
            "x0 Recoil, x9 Spread Recovery Speed, +50% Weakpoint Damage Bonus, -1 Damage, -2 Rate of Fire",
        )
        oc7 = Overclock(
            OverclockType.UNSTABLE,
            "Electrifying Reload",
            "+Electric Reload (100% chance), -60 Max Ammo, -10 Magazine Size",
        )
        return (oc1, oc2, oc3, oc4, oc5, oc6, oc7)

    OVERCLOCK_LIST = _init_overclock_list()

    def __init__(self) -> None:
        self.damage = DeepcoreGK2.DAMAGE
        self.weakpoint_stun_duration = DeepcoreGK2.WEAKPOINT_STUN_DURATION
        self.magazine_size = DeepcoreGK2.MAGAZINE_SIZE
        self.max_ammo = DeepcoreGK2.MAX_AMMO
        self.rate_of_fire = DeepcoreGK2.RATE_OF_FIRE
        self.reload_time = DeepcoreGK2.RELOAD_TIME
        self.weakpoint_stun_chance = DeepcoreGK2.WEAKPONT_STUN_CHANCE
        self.base_spread = DeepcoreGK2.BASE_SPREAD
        self.armor_breaking = DeepcoreGK2.ARMOR_BREAKING
        self._build = Build(None, None)

    @staticmethod
    def _string_to_oc(oc_str: str) -> Overclock:
        for i, oc in enumerate(DeepcoreGK2.OVERCLOCK_LIST):
            if i == int(oc_str):
                return oc
        return Overclock(None, "", "")

    @staticmethod
    def _find_mod(row_number: int, mod: str) -> Mod:
        for i, row in enumerate(DeepcoreGK2.MOD_TREE):
            if i == row_number:
                return row[ord(mod) - ord("A")]
        return Mod("", "")

    @staticmethod
    def _mods_string_to_tuple(mods: str) -> tuple[Mod, Mod, Mod, Mod, Mod]:
        out: list[Mod] = []
        for i, mod in enumerate(mods):
            out.append(DeepcoreGK2._find_mod(i, mod))
        return (out[0], out[1], out[2], out[3], out[4])

    @staticmethod
    def is_overclock_valid(oc: int):
        return oc >= 1 and oc <= len(DeepcoreGK2.OVERCLOCK_LIST)

    @staticmethod
    def is_mod_valid(mod: str, tier: str) -> bool:
        i = int(tier[1]) - 1
        row = DeepcoreGK2.MOD_TREE[i]
        if len(row) == 2:
            return mod in {"-", "A", "B"}
        return mod in {"-", "A", "B", "C"}

    @staticmethod
    def is_build_valid(build: str) -> bool:
        try:
            length = len(build)
            if length != 6:
                raise ValueError("Build input should have a length of 6")
            acronyms = ("T1", "T2", "T3", "T4", "T5", "OC")
            for acc, mod in zip(acronyms, build):
                if acc != "OC" and not DeepcoreGK2.is_mod_valid(mod, acc):
                    raise ValueError(f"Invalid mod in {acc}")
                elif acc == "OC" and not DeepcoreGK2.is_overclock_valid(int(mod)):
                    raise ValueError("Invalid Overclock number")
        except ValueError as err:
            print(err)
            return False
        return True

    def change_build(self, build: str) -> None:
        build = build.upper()
        if DeepcoreGK2.is_build_valid(build):
            mods = build[:5]
            oc = build[5:]
            self._build.mod_selection = DeepcoreGK2._mods_string_to_tuple(mods)
            self._build.overclock = DeepcoreGK2._string_to_oc(oc)

    @property
    def magazine_damage(self) -> float:
        return self.damage * self.magazine_size

    @property
    def magazine_duration(self) -> float:
        return self.magazine_size / self.rate_of_fire

    @property
    def total_damage(self) -> int:
        return int((self.magazine_size + self.max_ammo) * self.damage)

    @property
    def burst_dps(self) -> float:
        return self.magazine_damage / self.magazine_duration

    @property
    def sustained_dps(self) -> float:
        return self.magazine_damage / (self.magazine_duration + self.reload_time)
