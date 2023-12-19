from enum import Enum, auto
from dataclasses import dataclass


@dataclass(frozen=True)
class Mod:
    name: str
    description: str


type ModRow = dict[str, Mod]
type ModTree = dict[str, ModRow]
type ModSelection = tuple[Mod | None, Mod | None, Mod | None, Mod | None, Mod | None]


class OverclockType(Enum):
    CLEAN = auto()
    BALANCED = auto()
    UNSTABLE = auto()


@dataclass(frozen=True)
class Overclock:
    type_: OverclockType | None
    name: str
    description: str


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
        t1_A = Mod("Gyro Stabilisation", "x0 Base Spread")
        t1_B = Mod("Supercharged Feed Mechanism", "+1 Rate of Fire")
        t1_C = Mod("Quickfire Ejector", "x0.73 Reload Time")
        t1 = {"A": t1_A, "B": t1_B, "C": t1_C}
        t2_A = Mod("Increased Caliber Rounds", "+3 Damage")
        t2_B = Mod("Expanded Ammo Bags", "+120 Max Ammo")
        t2 = {"A": t2_A, "B": t2_B}
        t3_A = Mod("Floating Barrel", "x0.5 Recoil, -0.65 Max Spread")
        t3_B = Mod("High Capacity Magazine", "+10 Magazine Size")
        t3 = {"A": t3_A, "B": t3_B}
        t4_A = Mod("Hollow-Point Bullets", "+20% Weakspot Damage Bonus")
        t4_B = Mod("Hardened Rounds", "+500% Armor Break Bonus")
        t4 = {"A": t4_A, "B": t4_B}
        t5_A = Mod("Battle Frenzy", "+Battle Frenzy")
        t5_B = Mod("Improved Gas System", "+2 Rate of Fire")
        t5_C = Mod("Stun", "+35% Stun Chance")
        t5 = {"A": t5_A, "B": t5_B, "C": t5_C}
        return {"T1": t1, "T2": t2, "T3": t3, "T4": t4, "T5": t5}

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
        self._overclock = None
        self._mod_selection = None

    @staticmethod
    def is_overclock_valid(oc: str) -> bool:
        return oc == "-" or int(oc) in range(len(DeepcoreGK2.OVERCLOCK_LIST))

    @staticmethod
    def is_mod_valid(mod: str, tier: str) -> bool:
        return mod in DeepcoreGK2.MOD_TREE[tier] or mod == "-"

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
                elif acc == "OC" and not DeepcoreGK2.is_overclock_valid(mod):
                    raise ValueError("Invalid Overclock number")
        except ValueError as err:
            print(err)
            return False
        return True

    @staticmethod
    def get_overclock(oc: str) -> Overclock | None:
        if oc == "-":
            return
        elif DeepcoreGK2.is_build_valid("-----" + oc):
            return DeepcoreGK2.OVERCLOCK_LIST[int(oc) - 1]

    @staticmethod
    def get_mod_selection(mods: str) -> ModSelection | None:
        if mods == "-----":
            return None
        elif DeepcoreGK2.is_build_valid(mods + "-"):
            out: list[Mod | None] = []
            tiers = ("T1", "T2", "T3", "T4", "T5")
            for tier, mod in zip(tiers, mods):
                if mod == "-":
                    out.append(None)
                else:
                    out.append(DeepcoreGK2.MOD_TREE[tier][mod])
            return (out[0], out[1], out[2], out[3], out[4])

    @property
    def build(self):
        build = ""
        mods = self._mod_selection
        if mods:
            tiers = ("T1", "T2", "T3", "T4", "T5")
            for tier, mod in zip(tiers, mods):
                for k, v in DeepcoreGK2.MOD_TREE[tier].items():
                    if v == mod:
                        build += k
        else:
            build = "-----"
        overclock = self._overclock
        if overclock:
            for i, test_oc in enumerate(DeepcoreGK2.OVERCLOCK_LIST, 1):
                if overclock == test_oc:
                    build += str(i)
        else:
            build += "-"
        return build

    @build.setter
    def build(self, build) -> None:
        build = build.upper()
        if DeepcoreGK2.is_build_valid(build):
            mods = build[:5]
            oc = build[5:]
            self._mod_selection = DeepcoreGK2.get_mod_selection(mods)
            self._overclock = DeepcoreGK2.get_overclock(oc)

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
