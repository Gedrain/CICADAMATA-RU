# Shared paths for the build tools. WORK (decompiled game, intermediates) can be moved with $CICADA_WORK.
import os
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.environ.get('CICADA_WORK', os.path.join(KIT, 'work'))
SRC = os.path.join(KIT, 'translations_src')
PAYLOAD = os.path.join(KIT, 'payload')
DEFAULT_PCK = os.path.expanduser('~/.local/share/Steam/steamapps/common/CICADAMATA/CICADAMATA.pck')
