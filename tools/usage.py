# Finds string constants that compiled scripts use as keys (comparisons, dict keys, node paths, anim names...).
# Those must never be translated in the .gdc copies -> WORK/unsafe.json
import os, re, json, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gdc
from common import WORK
KEYPAT = [r'[=!]=\s*{L}', r'{L}\s*[=!]=', r'^\s*{L}\s*(,\s*{L2}\s*)*:\s*$', r'{L}\s*:(?!\s*$)', r'\bin\s*\[[^\]]*{L}',
          r'\.(play|play_backwards|queue|get_node|get_node_or_null|has|has_node|emit_signal|call|call_deferred|set|get|connect|is_action_pressed|is_action_just_pressed|is_action_just_released|is_action_released|get_action_strength|has_method|find_child|add_to_group|is_in_group|get_nodes_in_group|get_first_node_in_group|get_setting|set_setting|set_value|get_value|has_section_key|begins_with|ends_with|contains|find|replace|split|erase|get_meta|set_meta|has_meta|seek|animation_set_next|travel|get_animation|getAchievement|setAchievement|indicateAchievementProgress|findLeaderboard|findOrCreateLeaderboard|setStatInt|getStatInt|setStatFloat|storeStats)\s*\([^)]*{L}',
          r'\[\s*{L}\s*\]', r'\$\s*{L}', r'%\s*{L}', r'load\s*\(\s*{L}']
def lit(s): return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t') + '"'
def main():
    X, SRC = os.path.join(WORK, 'x'), os.path.join(WORK, 'src')
    res, unsafe = {}, set()
    for p in sorted(glob.glob(X + '/**/*.gdc', recursive=True)):
        rel = os.path.relpath(p, X)
        if rel.startswith('addons/'): continue
        gd = os.path.join(SRC, rel[:-1])
        src = open(gd, encoding='utf-8').read().split('\n') if os.path.exists(gd) else []
        out = []
        for k, v in gdc.parse(p)['consts']:
            if k != 'str' or not re.search('[A-Za-z]', v): continue
            L = re.escape(lit(v))
            uses = [(i + 1, l.strip()) for i, l in enumerate(src) if lit(v) in l]
            key = any(re.search(pp.format(L=L, L2=r'"[^"]*"'), l) for _, l in uses for pp in KEYPAT)
            if key: unsafe.add(v)
            out.append(dict(s=v, key=key, uses=uses[:6], nuses=len(uses)))
        res[rel] = out
    json.dump(res, open(os.path.join(WORK, 'usage.json'), 'w'), ensure_ascii=False, indent=1)
    json.dump(sorted(unsafe), open(os.path.join(WORK, 'unsafe.json'), 'w'), ensure_ascii=False, indent=0)
    print('script strings', sum(len(v) for v in res.values()), 'used as keys', len(unsafe))
if __name__ == '__main__': main()
