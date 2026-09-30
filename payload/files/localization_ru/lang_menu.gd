extends Node
# Russian localization: language selector injected into the game's options menu (GAME section).
# The choice is stored in user://language.cfg, which the engine reads at startup through
# application/config/project_settings_override, so a change applies after a restart.

const LANG_FILE := "user://language.cfg"
const OPTION_SCENE := "res://Scenes/UI/option_dropdown.tscn"
const LANGS := [["ru", "РУССКИЙ"], ["en", "ENGLISH"]]


func _ready() -> void:
	if not FileAccess.file_exists(LANG_FILE):
		_save_lang(_running_lang())
	get_tree().node_added.connect(_on_node_added)


func _running_lang() -> String:
	return "ru" if TranslationServer.get_locale().begins_with("ru") else "en"


func _saved_lang() -> String:
	var cf := ConfigFile.new()
	if cf.load(LANG_FILE) == OK:
		return str(cf.get_value("internationalization", "locale/test", _running_lang()))
	return _running_lang()


func _save_lang(code: String) -> void:
	var f := FileAccess.open(LANG_FILE, FileAccess.WRITE)
	if f:
		f.store_string("[internationalization]\n\nlocale/test=\"%s\"\n" % code)


func _on_node_added(n: Node) -> void:
	if n.name == "Options" and n is Control and n.has_node("Game") and n.has_node("MainSelect"):
		_inject.call_deferred(n)


func _inject(opt: Node) -> void:
	if not is_instance_valid(opt):
		return
	var game := opt.get_node_or_null("Game")
	if game == null or game.has_node("LanguageOption"):
		return
	var scene: PackedScene = load(OPTION_SCENE)
	if scene == null:
		return
	var row := scene.instantiate()
	row.name = "LanguageOption"
	row.set("_text", "ЯЗЫК / LANGUAGE")
	row.set("_description", "Язык игры. Применяется после перезапуска. / Game language. Applies after restart.")
	game.add_child(row)
	var b: OptionButton = row.get("button")
	if b == null:
		return
	b.clear()
	for i in LANGS.size():
		b.add_item(LANGS[i][1], i)
	b.select(0 if _saved_lang() == "ru" else 1)
	b.item_selected.connect(_on_selected)


func _on_selected(i: int) -> void:
	var code: String = LANGS[i][0]
	_save_lang(code)
	if code == _running_lang():
		return
	var notif := get_node_or_null("/root/UnlockNotif")
	if notif and notif.has_method("_notif"):
		if code == "ru":
			notif._notif("ЯЗЫК: РУССКИЙ", "Перезапусти игру, чтобы применить.")
		else:
			notif._notif("LANGUAGE: ENGLISH", "Restart the game to apply.")
