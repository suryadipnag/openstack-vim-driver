import pathlib
import os
package_path = str(pathlib.Path(__file__).parent.resolve())

TYPE_EXTENSIONS_FILE = os.path.join(package_path, 'type_extensions.yaml')
