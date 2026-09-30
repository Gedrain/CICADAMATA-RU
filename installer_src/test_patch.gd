extends SceneTree
func _init():
	var P = load("res://patcher.gd").new()
	P.on_progress = func(f, l): pass
	P.on_log = func(t, k): print("LOG ", t)
	print("payload ", P.load_payload("res://payload/payload.dat"), " files=", P.files.size())
	var g := OS.get_cmdline_user_args()[0]
	print("state before=", P.pck_state(g + "/CICADAMATA.pck"))
	print("install err='", P.install(g, false), "'")
	print("state after=", P.pck_state(g + "/CICADAMATA.pck"), " orig exists=", FileAccess.file_exists(g + "/CICADAMATA.pck.orig"))
	print("reinstall err='", P.install(g, false), "'")
	quit()
