extends SceneTree
# Args: <catalog.json> <ru_scripts.txt> <out ru.translation> <out remaps.bin>
func _init():
	var a := OS.get_cmdline_user_args()
	var d: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(a[0]))
	var t := Translation.new()
	t.locale = "ru"
	for k in d:
		t.add_message(k, d[k])
	var o := OptimizedTranslation.new()
	o.generate(t)
	var err := ResourceSaver.save(o, a[2])
	var r: Translation = ResourceLoader.load(a[2], "", ResourceLoader.CACHE_MODE_IGNORE)
	var bad := 0
	for k in d:
		if r.get_message(k) != d[k]:
			bad += 1
	print("TRANSLATION err=", err, " messages=", d.size(), " mismatches=", bad)
	var remaps := {}
	for line in FileAccess.get_file_as_string(a[1]).split("\n", false):
		remaps["res://" + line.trim_suffix(".gdc") + ".gd"] = PackedStringArray(["res://localization_ru/" + line + ":ru"])
	var f := FileAccess.open(a[3], FileAccess.WRITE)
	f.store_buffer(var_to_bytes(remaps))
	print("REMAPS ", remaps.size())
	quit()
