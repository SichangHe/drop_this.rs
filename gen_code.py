from typing import Final
import os
import re

SRC_LIB: Final = "src/lib.rs"
NOTICE: Final = "DO NOT modify manually! Generate with `gen_code.py`."
TYPES: Final = [
    ("Result", "<T, E>", ""),
    ("bool", "", ""),
    ("JoinHandle", "<T>", "tokio"),
    ("AbortHandle", "", "tokio"),
]
HEADER: Final = f"""// {NOTICE}
//! Traits to provide a method for dropping values of specific types,
//! as an alternative to a type-agnostic [`drop`] or `_ =` assignment.
//! This is useful to avoid dropping the wrong type, e.g.,
//! when sending a message through a channel.
"""
USES: Final = """
#[cfg(feature = "tokio")]
use tokio::task::{AbortHandle, JoinHandle};
"""


def pascal2snake(name: str):
    name = re.sub(r"([A-Z])([A-Z])", r"\1_\2", name)
    name = re.sub(r"([a-z])([A-Z])", r"\1_\2", name)
    return name.lower()


def gen_drop(type_name: str, generic_params: str, feature: str):
    fn_name = pascal2snake(type_name)
    trait_name = f"Drop{type_name[0].upper() + type_name[1:]}"
    method_name = f"drop_{fn_name}"
    attribute = (
        f"""#[cfg(feature = "{feature}")]
"""
        if len(feature) > 0
        else ""
    )
    return f"""
/// Provides [`{trait_name}::{method_name}`] for dropping [`{type_name}`] values.
{attribute}pub trait {trait_name} {{
    /// Drop this [`{type_name}`].
    /// This method prevents dropping a value that is not a [`{type_name}`].
    fn {method_name}(self);
}}

{attribute}impl{generic_params} {trait_name} for {type_name}{generic_params} {{
    fn {method_name}(self) {{}}
}}
"""


def gen_lib_code():
    generated = "\n".join([gen_drop(*t) for t in TYPES])
    return f"""{HEADER}

{USES}

{generated}
"""


def main():
    code = gen_lib_code()
    with open(SRC_LIB, "w") as f:
        _ = f.write(code)
    _ = os.system(
        "cargo clippy --all-targets --fix --allow-dirty --allow-staged --workspace"
    )
    _ = os.system("cargo fmt")


main() if __name__ == "__main__" else None
