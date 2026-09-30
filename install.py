#!/usr/bin/env python3
# Re-applies the Russian localization v2 to CICADAMATA.pck (e.g. after Steam "verify files" restored the original).
# Same result as the GUI installers in dist/. Usage: install.py [game_dir]
import os, sys
KIT = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(KIT, 'tools'))
import ru_patch
game = sys.argv[1] if len(sys.argv) > 1 else ru_patch.default_game_dir()
if not game: sys.exit('Game folder not found; pass it as an argument.')
ru_patch.install(game, os.path.join(KIT, 'payload'))
