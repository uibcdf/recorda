"""Small standalone capture selection; semantic labels do not define routing."""

from dataclasses import dataclass

from .capture import label


@dataclass(frozen=True)
class CapturePolicy:
    """Select declared profiles and payload groups; lifecycle facts stay mandatory."""

    profiles: tuple[str, ...] | None = None
    inputs: bool = True
    parameters: bool = True
    outputs: bool = True
    exception_references: bool = True

    def __post_init__(self):
        if self.profiles is not None:
            if type(self.profiles) not in {tuple, list, set, frozenset}:
                raise TypeError("profiles must be a bounded collection of semantic labels")
            if len(self.profiles) > 64:
                raise ValueError("at most 64 profiles may be selected")
            object.__setattr__(self, "profiles", tuple(sorted({label(p) for p in self.profiles})))
        for name in ("inputs", "parameters", "outputs", "exception_references"):
            if type(getattr(self, name)) is not bool:
                raise TypeError("capture detail switches must be bool")

    def accepts(self, profile):
        return self.profiles is None or profile in self.profiles

    def describe(self):
        return {
            "profiles": None if self.profiles is None else list(self.profiles),
            **self.detail(),
        }

    def detail(self):
        return {
            name: "enabled" if getattr(self, name) else "omitted_by_policy"
            for name in ("inputs", "parameters", "outputs", "exception_references")
        }
