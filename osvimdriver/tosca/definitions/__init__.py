import pathlib
import os
package_path = str(pathlib.Path(__file__).parent.resolve())

TYPE_EXTENSIONS_FILE = os.path.join(package_path, 'type_extensions.yaml')
ETSI_COMMON_TYPES_FILE = os.path.join(package_path, 'etsi_nfv_sol001_common_types.yaml')
ETSI_VNFD_TYPES_FILE = os.path.join(package_path, 'etsi_nfv_sol001_vnfd_types.yaml')
NFV_EXTENSIONS_FILE = os.path.join(package_path, 'nfv_extensions.yaml')