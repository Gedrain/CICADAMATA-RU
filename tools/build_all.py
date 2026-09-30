#!/usr/bin/env python3
"""Rebuilds the whole Russian localization from a clean copy of the game.

    python3 tools/build_all.py [--pck PATH] [--installers] [--clean]

Steps: extract pck -> decompile with GDRE Tools -> analyse scripts/scenes -> build v2 translation data
-> patch compiled scripts -> Cyrillic fonts -> ru.translation + remaps -> project.binary -> payload
(+ with --installers: Godot export of the Windows installer, Linux AppImage, Windows zip).

Requirements: Python 3.14+ (compression.zstd), fontTools, Pillow, Godot 4.7.2 as `godot` in PATH
(export templates for --installers), internet on first run (downloads GDRE Tools 2.6.4).
Intermediate files go to ./work (override with $CICADA_WORK).
"""
import argparse, glob, hashlib, json, os, shutil, struct, subprocess, sys, urllib.request, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import KIT, WORK, SRC, PAYLOAD, DEFAULT_PCK
import pck, projbin, n4_cyrillic

GDRE_URL = 'https://github.com/GDRETools/gdsdecomp/releases/download/v2.6.4/GDRE_tools-v2.6.4-linux.zip'
MEDIA = ('.ctex', '.sample', '.oggvorbisstr', '.ogv', '.mp3str')
TOOLS = os.path.join(KIT, 'tools')


def step(msg): print('\n== ' + msg, flush=True)
def run(cmd, **kw):
    print('   $ ' + ' '.join(cmd), flush=True)
    subprocess.run(cmd, check=True, **kw)
def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for c in iter(lambda: f.read(1 << 24), b''): h.update(c)
    return h.hexdigest()
def godot(script, *args):
    proj = os.path.join(WORK, 'godot_stub')
    os.makedirs(proj, exist_ok=True)
    open(os.path.join(proj, 'project.godot'), 'w').write('config_version=5\n[application]\nconfig/name="stub"\n')
    out = subprocess.run(['godot', '--headless', '--path', proj, '--script', script, '--', *args],
                         capture_output=True, text=True)
    lines = [l for l in out.stdout.splitlines() if l.startswith(('FONT', 'TRANSLATION', 'REMAPS'))]
    print('\n'.join('   ' + l for l in lines))
    return lines


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pck', default=None, help='clean CICADAMATA.pck (default: the .orig backup or the Steam copy)')
    ap.add_argument('--installers', action='store_true', help='also export installers into dist/')
    ap.add_argument('--clean', action='store_true', help='re-extract and re-decompile even if work/ exists')
    a = ap.parse_args()
    src_pck = a.pck or (DEFAULT_PCK + '.orig' if os.path.exists(DEFAULT_PCK + '.orig') else DEFAULT_PCK)
    want = open(os.path.join(KIT, 'original_pck.md5')).read().strip()
    os.makedirs(WORK, exist_ok=True)

    step('check game archive: ' + src_pck)
    got = md5(src_pck)
    if got != want:
        print('   ! md5 %s differs from the version the translation was made for (%s).' % (got, want))
        print('   ! Continuing: expect untranslated/new strings; update original_pck.md5 when done.')
    hdr, ents = pck.read_dir(src_pck)
    print('   files in pck:', len(ents))
    if any(p.startswith('localization_ru/') for p, *_ in ents):
        sys.exit('this pck is already patched - use the clean original')

    X = os.path.join(WORK, 'x')
    if a.clean or not os.path.isdir(X):
        step('extract scripts/scenes/resources -> work/x')
        shutil.rmtree(X, ignore_errors=True)
        pck.extract(src_pck, ents, lambda p: not p.endswith(MEDIA), X)

    gdre = os.path.join(WORK, 'gdre', 'gdre_tools.x86_64')
    if not os.path.exists(gdre):
        step('download GDRE Tools')
        z = os.path.join(WORK, 'gdre.zip')
        urllib.request.urlretrieve(GDRE_URL, z)
        zipfile.ZipFile(z).extractall(os.path.join(WORK, 'gdre'))
        os.chmod(gdre, 0o755)
    for out, extra in (('src', ['--scripts-only']), ('src2', ['--exclude=**/*' + e for e in MEDIA + ('.scn.mesh',)])):
        d = os.path.join(WORK, out)
        if a.clean or not os.path.isdir(d):
            step('decompile with GDRE Tools -> work/' + out)
            shutil.rmtree(d, ignore_errors=True)
            run([gdre, '--headless', '--recover=' + src_pck, *extra, '--output=' + d], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    step('analyse scripts and scenes')
    run([sys.executable, os.path.join(TOOLS, 'usage.py')])
    run([sys.executable, os.path.join(TOOLS, 'scene_nodes.py'), os.path.join(WORK, 'src2'), os.path.join(WORK, 'nodes.json')])
    run([sys.executable, os.path.join(TOOLS, 'anim_tracks.py')])

    step('build v2 translation data')
    run([sys.executable, os.path.join(TOOLS, 'build_v2.py')])
    run([sys.executable, os.path.join(TOOLS, 'latin_check.py')])

    step('patch compiled scripts')
    shutil.rmtree(os.path.join(WORK, 'out_v2'), ignore_errors=True)
    run([sys.executable, os.path.join(TOOLS, 'patch_gdc.py')])

    step('fonts with Cyrillic')
    F = os.path.join(WORK, 'fonts'); os.makedirs(F, exist_ok=True)
    imported = {os.path.basename(p): p for p in glob.glob(os.path.join(X, '.godot/imported/*.fontdata'))}
    jobs = []
    for font in ('bitpop.otf', 'N4NOOSE-Macaroni.ttf', 'N4NOOSE-Block.ttf', 'n4noose.ttf'):
        orig = [p for n, p in imported.items() if n.startswith(font + '-')]
        assert len(orig) == 1, font
        if font == 'bitpop.otf':
            cyr = os.path.join(SRC, 'fonts', 'bitpop_cyr.otf')
        else:
            cyr = os.path.join(F, font.replace('.ttf', '_cyr.ttf'))
            n4_cyrillic.patch(os.path.join(WORK, 'src2', 'Assets', 'Fonts', font), cyr)
        jobs += [orig[0], cyr, os.path.join(F, 'new_' + os.path.basename(orig[0]))]
    lines = godot(os.path.join(TOOLS, 'godot', 'conv_fonts.gd'), *jobs)
    assert len([l for l in lines if 'cyrillic=true' in l]) == 4, 'font conversion failed'

    step('ru.translation + script remaps')
    G = os.path.join(WORK, 'gp2'); os.makedirs(G, exist_ok=True)
    out_v2 = os.path.join(WORK, 'out_v2')
    scripts = sorted(os.path.relpath(p, out_v2) for p in glob.glob(out_v2 + '/**/*.gdc', recursive=True))
    open(os.path.join(G, 'ru_scripts.txt'), 'w').write('\n'.join(scripts) + '\n')
    lines = godot(os.path.join(TOOLS, 'godot', 'make_translation.gd'), os.path.join(WORK, 'catalog_v2.json'),
                  os.path.join(G, 'ru_scripts.txt'), os.path.join(G, 'ru.translation'), os.path.join(G, 'remaps.bin'))
    assert any('mismatches=0' in l for l in lines), 'translation build failed'

    step('project.binary')
    e = projbin.read(os.path.join(X, 'project.binary'))
    add = {'internationalization/locale/translations': projbin.psa_enc(['res://localization_ru/ru.translation']),
           'internationalization/locale/test': projbin.s_enc('ru'),
           'internationalization/locale/translation_remaps': open(os.path.join(G, 'remaps.bin'), 'rb').read(),
           'application/config/project_settings_override': projbin.s_enc('user://language.cfg'),
           'autoload/RuLang': projbin.s_enc('*res://localization_ru/lang_menu.gd')}
    e = [(k, v) for k, v in e if k not in add] + list(add.items())
    projbin.write(os.path.join(G, 'project.binary'), e)

    step('payload')
    shutil.rmtree(os.path.join(PAYLOAD, 'files'), ignore_errors=True)
    files = {}
    def put(pck_path, src):
        dst = os.path.join(PAYLOAD, 'files', pck_path); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst); files[pck_path] = md5(src)
    put('project.binary', os.path.join(G, 'project.binary'))
    put('localization_ru/ru.translation', os.path.join(G, 'ru.translation'))
    put('localization_ru/lang_menu.gd', os.path.join(SRC, 'lang_menu.gd'))
    ver = os.path.join(WORK, 'version.txt'); open(ver, 'w').write('2.0\n')
    put('localization_ru/version.txt', ver)
    for s in scripts:
        put('localization_ru/' + s, os.path.join(out_v2, s))
    for p in glob.glob(os.path.join(F, 'new_*.fontdata')):
        put('.godot/imported/' + os.path.basename(p)[4:], p)
    man = {'game': 'CICADAMATA', 'steam_appid': 3817250, 'godot': '4.7.2', 'original_pck_md5': want,
           'original_pck_size': os.path.getsize(src_pck), 'version': '2.0', 'files': files}
    json.dump(man, open(os.path.join(PAYLOAD, 'manifest.json'), 'w'), indent=1)
    ents2 = [('manifest.json', json.dumps(man).encode())] + [(k, open(os.path.join(PAYLOAD, 'files', k), 'rb').read()) for k in sorted(files)]
    blob = bytearray(b'RUPL' + struct.pack('<I', len(ents2)))
    for n, d in ents2:
        nb = n.encode(); blob += struct.pack('<I', len(nb)) + nb + struct.pack('<I', len(d)) + d
    os.makedirs(os.path.join(KIT, 'installer_src', 'payload'), exist_ok=True)
    open(os.path.join(KIT, 'installer_src', 'payload', 'payload.dat'), 'wb').write(blob)
    print('   payload files:', len(files), ' installer payload:', len(blob), 'bytes')

    if a.installers:
        step('installers')
        inst = os.path.join(KIT, 'installer_src'); dist = os.path.join(KIT, 'dist'); os.makedirs(dist, exist_ok=True)
        run(['godot', '--headless', '--path', inst, '--import'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        exe = os.path.join(dist, 'CICADAMATA_RU_Installer_Windows.exe')
        run(['godot', '--headless', '--path', inst, '--export-release', 'Windows', exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        run(['sh', os.path.join(inst, 'build_appimage.sh'), '--export'])
        with zipfile.ZipFile(os.path.join(dist, 'CICADAMATA_RU_v2.0_Windows.zip'), 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            z.write(exe, 'CICADAMATA_RU_v2.0/CICADAMATA_RU_Installer_Windows.exe')
            z.write(os.path.join(KIT, 'docs', 'README_RU.txt'), 'CICADAMATA_RU_v2.0/README_RU.txt')
    print('\nDone.')


if __name__ == '__main__':
    main()
