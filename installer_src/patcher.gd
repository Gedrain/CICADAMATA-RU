extends RefCounted
## CICADAMATA" Russian localization - pck patcher used by the installer UI.
## All heavy work runs on a worker thread; progress/log go through the callables.

const PCK_NAME := "CICADAMATA.pck"
const ORIG_NAME := "CICADAMATA.pck.orig"
const APP_ID := "3817250"
const CHUNK := 8 * 1024 * 1024
const MARKER := "localization_ru/version.txt"

var manifest: Dictionary = {}
var files: Dictionary = {}          # pck path -> PackedByteArray
var on_progress: Callable           # (fraction: float, label: String)
var on_log: Callable                # (text: String, kind: String)  kind: "info" | "ok" | "warn" | "err"


func load_payload(path: String) -> bool:
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null or f.get_buffer(4).get_string_from_ascii() != "RUPL":
		return false
	var n := f.get_32()
	for i in n:
		var name := f.get_buffer(f.get_32()).get_string_from_utf8()
		var data := f.get_buffer(f.get_32())
		if name == "manifest.json":
			manifest = JSON.parse_string(data.get_string_from_utf8())
		else:
			files[name] = data
	return not manifest.is_empty()


# ---------------------------------------------------------------- game search
func find_games() -> PackedStringArray:
	var roots: PackedStringArray = []
	if OS.get_name() == "Windows":
		for key in [["HKCU\\Software\\Valve\\Steam", "SteamPath"], ["HKLM\\SOFTWARE\\WOW6432Node\\Valve\\Steam", "InstallPath"], ["HKLM\\SOFTWARE\\Valve\\Steam", "InstallPath"]]:
			var out := []
			if OS.execute("reg", ["query", key[0], "/v", key[1]], out, true) == 0 and out.size() > 0:
				var m := RegEx.create_from_string("REG_SZ\\s+([^\\r\\n]+)").search(str(out[0]))
				if m:
					roots.append(m.get_string(1).strip_edges().replace("\\", "/"))
		roots.append_array(PackedStringArray(["C:/Program Files (x86)/Steam", "C:/Program Files/Steam"]))
		for d in "DEFGHIJKLMNOPQRSTUVWXYZ":
			for sub in ["SteamLibrary", "Steam", "Games/Steam", "Games/SteamLibrary", "Program Files (x86)/Steam"]:
				roots.append(d + ":/" + sub)
	else:
		var h := OS.get_environment("HOME")
		roots.append_array(PackedStringArray([h + "/.local/share/Steam", h + "/.steam/steam", h + "/.steam/root", h + "/.steam/debian-installation",
			h + "/.var/app/com.valvesoftware.Steam/.local/share/Steam", h + "/.var/app/com.valvesoftware.Steam/data/Steam",
			h + "/snap/steam/common/.local/share/Steam"]))
	var libs: PackedStringArray = []
	for r in roots:
		for vdf in [r + "/steamapps/libraryfolders.vdf", r + "/config/libraryfolders.vdf"]:
			if FileAccess.file_exists(vdf):
				var txt := FileAccess.get_file_as_string(vdf)
				for m in RegEx.create_from_string("\"path\"\\s+\"([^\"]+)\"").search_all(txt):
					libs.append(m.get_string(1).replace("\\\\", "/").replace("\\", "/"))
		libs.append(r)
	var found: PackedStringArray = []
	var seen := {}
	for lib in libs:
		var g := (lib + "/steamapps/common/CICADAMATA").simplify_path()
		var pck := g + "/" + PCK_NAME
		if not FileAccess.file_exists(pck):
			continue
		# the same install is often reachable through symlinks (~/.steam/steam, ~/.steam/root)
		var f := FileAccess.open(pck, FileAccess.READ)
		var key := "%d:%d" % [FileAccess.get_modified_time(pck), f.get_length() if f else 0]
		if seen.has(key):
			continue
		seen[key] = true
		found.append(g)
	return found


func is_game_dir(dir: String) -> bool:
	return FileAccess.file_exists(dir.path_join(PCK_NAME))


# ---------------------------------------------------------------- pck parsing
## Returns {base, diroff, entries:[[path, off, size, md5(PackedByteArray), flags]]} or {} on failure.
func read_dir(path: String) -> Dictionary:
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null or f.get_length() < 0x28 or f.get_buffer(4).get_string_from_ascii() != "GDPC":
		return {}
	f.seek(0x18)
	var base := f.get_64()
	var diroff := f.get_64()
	if diroff <= 0 or diroff >= f.get_length():
		return {}
	f.seek(diroff)
	var n := f.get_32()
	var ents := []
	for i in n:
		var l := f.get_32()
		var p := f.get_buffer(l).get_string_from_utf8()
		var off := f.get_64()
		var size := f.get_64()
		var md5 := f.get_buffer(16)
		var fl := f.get_32()
		ents.append([p, off, size, md5, fl])
	return {"base": base, "diroff": diroff, "entries": ents}


## "original" | "ru1" | "ru2" | "unknown"
func pck_state(path: String) -> String:
	var d := read_dir(path)
	if d.is_empty():
		return "unknown"
	var has_ru := false
	var has_marker := false
	for e in d.entries:
		if e[0] == "localization_ru/ru.translation":
			has_ru = true
		elif e[0] == MARKER:
			has_marker = true
	if has_marker:
		return "ru2"
	return "ru1" if has_ru else "original"


func md5_file(path: String, label: String, p0: float, p1: float) -> String:
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return ""
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_MD5)
	var total := f.get_length()
	var done := 0
	while done < total:
		var n := mini(CHUNK, total - done)
		ctx.update(f.get_buffer(n))
		done += n
		on_progress.call(lerpf(p0, p1, float(done) / total), label)
	return ctx.finish().hex_encode()


func copy_file(src: String, dst: String, label: String, p0: float, p1: float) -> bool:
	var a := FileAccess.open(src, FileAccess.READ)
	var b := FileAccess.open(dst, FileAccess.WRITE)
	if a == null or b == null:
		return false
	var total := a.get_length()
	var done := 0
	while done < total:
		var n := mini(CHUNK, total - done)
		b.store_buffer(a.get_buffer(n))
		done += n
		on_progress.call(lerpf(p0, p1, float(done) / total), label)
	b.close()
	return b.get_error() == OK or FileAccess.file_exists(dst)


func build_pck(orig: String, out: String, p0: float, p1: float) -> String:
	var d := read_dir(orig)
	if d.is_empty():
		return "Не удалось прочитать архив игры."
	var names := {}
	for e in d.entries:
		names[e[0]] = true
	for k in files:
		if not k.begins_with("localization_ru/") and not names.has(k):
			return "В архиве игры нет файла %s — другая версия игры?" % k
	var src := FileAccess.open(orig, FileAccess.READ)
	var dst := FileAccess.open(out, FileAccess.WRITE)
	if src == null or dst == null:
		return "Нет доступа на запись в папку игры (закрой игру или запусти установщик от администратора)."
	var diroff: int = d.diroff
	var base: int = d.base
	var done := 0
	while done < diroff:
		var n := mini(CHUNK, diroff - done)
		dst.store_buffer(src.get_buffer(n))
		done += n
		on_progress.call(lerpf(p0, p1, float(done) / diroff), "ЗАПИСЬ ЛОКАЛИЗАЦИИ")
	var pos := diroff
	var info := {}
	var keys := files.keys()
	keys.sort()
	for k in keys:
		var pad := (32 - pos % 32) % 32
		if pad:
			dst.store_buffer(_zeros(pad))
		pos += pad
		var data: PackedByteArray = files[k]
		dst.store_buffer(data)
		var ctx := HashingContext.new()
		ctx.start(HashingContext.HASH_MD5)
		ctx.update(data)
		info[k] = [pos - base, data.size(), ctx.finish()]
		pos += data.size()
	var pad2 := (32 - pos % 32) % 32
	if pad2:
		dst.store_buffer(_zeros(pad2))
	pos += pad2
	var newdir := pos
	var rows := []
	for e in d.entries:
		if info.has(e[0]):
			rows.append([e[0], info[e[0]][0], info[e[0]][1], info[e[0]][2], 0])
		else:
			rows.append(e)
	for k in keys:
		if not names.has(k):
			rows.append([k, info[k][0], info[k][1], info[k][2], 0])
	dst.store_32(rows.size())
	for r in rows:
		var pb: PackedByteArray = str(r[0]).to_utf8_buffer()
		var padn := (4 - pb.size() % 4) % 4
		if padn:
			pb.append_array(_zeros(padn))
		dst.store_32(pb.size())
		dst.store_buffer(pb)
		dst.store_64(r[1])
		dst.store_64(r[2])
		dst.store_buffer(r[3])
		dst.store_32(r[4])
	dst.seek(0x20)
	dst.store_64(newdir)
	dst.close()
	return ""


func _zeros(n: int) -> PackedByteArray:
	var z := PackedByteArray()
	z.resize(n)
	z.fill(0)
	return z


func _replace(tmp: String, target: String) -> bool:
	if FileAccess.file_exists(target) and DirAccess.remove_absolute(target) != OK:
		return false
	return DirAccess.rename_absolute(tmp, target) == OK


# ---------------------------------------------------------------- actions
## Returns "" on success or an error message.
func install(game: String, set_russian: bool) -> String:
	var pck := game.path_join(PCK_NAME)
	var orig := game.path_join(ORIG_NAME)
	var want: String = manifest.original_pck_md5
	var src := ""
	on_log.call("> проверка оригинального архива игры...", "info")
	if FileAccess.file_exists(orig):
		if md5_file(orig, "ПРОВЕРКА РЕЗЕРВНОЙ КОПИИ", 0.0, 0.3) == want:
			src = orig
			on_log.call("+ резервная копия оригинала: в порядке", "ok")
		else:
			on_log.call("+ резервная копия не совпадает с нужной версией", "warn")
	if src == "":
		var state := pck_state(pck)
		if state != "original":
			return "Архив игры уже изменён, а чистой копии нет. Проверь целостность файлов в Steam (Свойства → Установленные файлы) и запусти установку снова."
		if md5_file(pck, "ПРОВЕРКА ВЕРСИИ ИГРЫ", 0.0, 0.3) != want:
			return "Эта версия игры отличается от той, для которой сделан перевод (обновление игры?). Дождись обновления перевода."
		on_log.call("+ версия игры: подходит", "ok")
		on_log.call("> создание резервной копии оригинала...", "info")
		if not copy_file(pck, orig + ".tmp", "РЕЗЕРВНАЯ КОПИЯ", 0.3, 0.55) or not _replace(orig + ".tmp", orig):
			return "Не удалось создать резервную копию (нет места или прав на запись)."
		src = orig
		on_log.call("+ оригинал сохранён: " + ORIG_NAME, "ok")
	on_log.call("> запись локализации в архив...", "info")
	var err := build_pck(src, pck + ".ru_tmp", 0.55, 0.97)
	if err != "":
		DirAccess.remove_absolute(pck + ".ru_tmp")
		return err
	if not _replace(pck + ".ru_tmp", pck):
		return "Не удалось заменить CICADAMATA.pck — закрой игру и попробуй снова."
	if pck_state(pck) != "ru2":
		return "Проверка после записи не прошла."
	on_log.call("+ локализация записана (%d файлов)" % files.size(), "ok")
	if set_russian:
		var n := write_language(game, "ru")
		if n > 0:
			on_log.call("+ язык игры: РУССКИЙ", "ok")
	on_progress.call(1.0, "ГОТОВО")
	return ""


func restore(game: String) -> String:
	var pck := game.path_join(PCK_NAME)
	var orig := game.path_join(ORIG_NAME)
	if not FileAccess.file_exists(orig):
		if pck_state(pck) == "original":
			return "Перевод не установлен — в игре уже оригинальные файлы."
		return "Резервная копия не найдена. Верни оригинал через Steam: Свойства → Установленные файлы → Проверить целостность."
	on_log.call("> восстановление оригинального архива...", "info")
	if not copy_file(orig, pck + ".ru_tmp", "ВОССТАНОВЛЕНИЕ", 0.0, 0.9) or not _replace(pck + ".ru_tmp", pck):
		return "Не удалось восстановить файл — закрой игру и попробуй снова."
	if pck_state(pck) != "original":
		return "Резервная копия повреждена. Проверь целостность файлов в Steam."
	DirAccess.remove_absolute(orig)
	on_log.call("+ оригинальные файлы восстановлены", "ok")
	on_progress.call(1.0, "ГОТОВО")
	return ""


## Writes the in-game language choice (read by the localization at startup). Returns number of files written.
func write_language(game: String, code: String) -> int:
	var dirs: PackedStringArray = []
	if OS.get_name() == "Windows":
		dirs.append(OS.get_environment("APPDATA").replace("\\", "/") + "/CICADAMATA")
	else:
		# Proton prefix: <library>/steamapps/compatdata/<appid>/pfx/.../AppData/Roaming/CICADAMATA
		var lib := game.get_base_dir().get_base_dir().get_base_dir()
		dirs.append(lib + "/steamapps/compatdata/" + APP_ID + "/pfx/drive_c/users/steamuser/AppData/Roaming/CICADAMATA")
		dirs.append(OS.get_environment("HOME") + "/.local/share/CICADAMATA")
	var n := 0
	for d in dirs:
		if DirAccess.dir_exists_absolute(d):
			var f := FileAccess.open(d + "/language.cfg", FileAccess.WRITE)
			if f:
				f.store_string("[internationalization]\n\nlocale/test=\"%s\"\n" % code)
				n += 1
	return n
