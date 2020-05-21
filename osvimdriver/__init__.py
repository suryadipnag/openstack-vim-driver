import json
import os

with open(os.path.join(os.path.dirname(__file__), 'pkg_info.json')) as fp:
    _pkg_info = json.load(fp)

__version__ = _pkg_info['version']

def _configure_translator_conf():
    # Set the environment variable (read by our fork of the translator) to set the translator conf
    # IMPORT: this must happen before the heat-translator module is imported, otherwise it's too late and the default config is used
    translator_conf_path = os.path.join(os.path.dirname(__file__), 'translator.conf')
    os.environ['TRANSLATOR_CONF'] = translator_conf_path

_configure_translator_conf()

from .app import create_app

def create_wsgi_app():
    ignition_app = create_app()
    # For wsgi deployments
    return ignition_app.connexion_app
