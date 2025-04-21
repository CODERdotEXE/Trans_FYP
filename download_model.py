import argostranslate.package, argostranslate.translate
from pathlib import Path
import os

# Download and install Bengali-Hindi translation model
package_path = "bn_hi.argosmodel"

# If you don’t have the model yet
if not Path(package_path).exists():
    os.system(f"wget https://github.com/argosopentech/argos-translate/releases/download/v1.0/bn_hi.argosmodel")

argostranslate.package.install_from_path(package_path)

