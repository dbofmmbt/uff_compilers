from . import dot
import sys

method_suffix = sys.argv[1]

method = getattr(
    dot,
    f"print_{method_suffix}",
    lambda: print("no method defined. Check the parameter you passed"),
)

method()
