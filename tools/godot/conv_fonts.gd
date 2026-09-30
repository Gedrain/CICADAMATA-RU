extends SceneTree
# Args: <original.fontdata> <font file with Cyrillic> <out.fontdata> [... repeated]
# Keeps every import setting of the game's font resource and only swaps the font data.
func _init():
	var a := OS.get_cmdline_user_args()
	var i := 0
	while i + 2 < a.size():
		var f: FontFile = ResourceLoader.load(a[i], "", ResourceLoader.CACHE_MODE_IGNORE)
		f.data = FileAccess.get_file_as_bytes(a[i + 1])
		var err := ResourceSaver.save(f, a[i + 2])
		var g: FontFile = ResourceLoader.load(a[i + 2], "", ResourceLoader.CACHE_MODE_IGNORE)
		print("FONT ", a[i + 1].get_file(), " err=", err, " cyrillic=", g.has_char(0x416))
		i += 3
	quit()
