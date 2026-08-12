# !/usr/bin/env python3

import sys
import os

# Force reload of the module
if 'shared.models' in sys.modules:
    del sys.modules['shared.models']

# Import fresh
from shared.models import ConversionArgs

print("=" * 60)
print("DEBUG: Field Order & Defaults")
print("=" * 60)

for name, field_obj in ConversionArgs.__dataclass_fields__.items():
    has_default = field_obj.default is not field_obj._FIELD_TYPE._HAS_DEFAULT_VALUE_SENTINEL
    default_val = repr(field_obj.default) if has_default else "(no default)"
    print(f"{name:20s} | {default_val}")

print("=" * 60)

# Find the FIRST field with a default
fields_with_defaults = []
for name, field_obj in ConversionArgs.__dataclass_fields__.items():
    has_default = field_obj.default is not field_obj._FIELD_TYPE._HAS_DEFAULT_VALUE_SENTINEL
    if has_default:
        fields_with_defaults.append(name)

if fields_with_defaults:
    first_default_idx = None
    for idx, (name, _) in enumerate(ConversionArgs.__dataclass_fields__.items()):
        if name == fields_with_defaults[0]:
            first_default_idx = idx
            break

    print(f"\n⚠️  First default found at position {first_default_idx}: '{fields_with_defaults[0]}'")
    print(f"   Any non-default fields AFTER position {first_default_idx} will cause TypeError!")

    print("\nNon-default fields that come AFTER the first default:")
    for idx, (name, _) in enumerate(ConversionArgs.__dataclass_fields__.items()):
        if idx > first_default_idx:
            field_obj = list(ConversionArgs.__dataclass_fields__.values())[idx]
            has_default = field_obj.default is not field_obj._FIELD_TYPE._HAS_DEFAULT_VALUE_SENTINEL
            if not has_default:
                print(f"   ❌ Position {idx}: {name}")

print("=" * 60)