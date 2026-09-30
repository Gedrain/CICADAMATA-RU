extends SceneTree
func _init():
	var P = load("res://patcher.gd").new()
	P.on_progress = func(f, l): pass
	P.on_log = func(t, k): print("LOG ", t)
	P.load_payload("res://payload/payload.dat")
	var g := OS.get_cmdline_user_args()[0]
	print("state=", P.pck_state(g + "/CICADAMATA.pck"))
	print("restore err='", P.restore(g), "'")
	print("state after=", P.pck_state(g + "/CICADAMATA.pck"), " orig exists=", FileAccess.file_exists(g + "/CICADAMATA.pck.orig"))
	print("restore again err='", P.restore(g), "'")
	quit()
