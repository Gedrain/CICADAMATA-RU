extends Control
## CICADAMATA" — установщик русской локализации. NOTFOUNDVPN.

const Patcher := preload("res://patcher.gd")
const RED := Color("c42b47")
const GOLD := Color("d2b066")
const GREY := Color(0.58, 0.58, 0.62)
const DIM := Color(1, 1, 1, 0.08)
const W := 1120
const H := 640

var F_PIX: Font = preload("res://assets/fonts/bitpop_cyr.otf")
var F_BIG: Font = preload("res://assets/fonts/Jupiteroid-Bold.ttf")
var F_SANS: Font = preload("res://assets/fonts/OverusedGrotesk-Medium.otf")
var F_CIPHER: Font = preload("res://assets/fonts/N4NOOSE-Macaroni_cyr.ttf")

var patcher := Patcher.new()
var game_dir := ""
var state := ""
var busy := false
var worker: Thread

var crt: ShaderMaterial
var glitch := 0.0
var glitch_timer := 3.0
var hero: TextureRect
var hero_base_y := 0.0
var t := 0.0

var log_rt: RichTextLabel
var log_queue: Array[String] = []
var log_speed := 90.0
var path_label: Label
var lang_check: CheckBox
var progress_blocks: Array[ColorRect] = []
var progress_label: Label
var progress_box: Control
var btn_install: Button
var btn_remove: Button
var btn_browse: Button
var btn_show: Button
var game_pick: OptionButton
var found_games: PackedStringArray = []
var btn_launch: Button
var motto: Label
var intro: Control
var sfx := {}
var players: Array[AudioStreamPlayer] = []


func _ready() -> void:
	get_window().title = "CICADAMATA\" — РУССКАЯ ЛОКАЛИЗАЦИЯ // NOTFOUNDVPN"
	_load_sfx()
	_build_ui()
	_build_intro()
	patcher.on_progress = func(f: float, label: String): _set_progress.call_deferred(f, label)
	patcher.on_log = func(text: String, kind: String): _log.call_deferred(text, kind)
	if not patcher.load_payload("res://payload/payload.dat"):
		_log("! ПОВРЕЖДЁН ПАКЕТ ПЕРЕВОДА — СКАЧАЙ УСТАНОВЩИК ЗАНОВО", "err")
		btn_install.disabled = true
		return
	_boot_sequence()


# ------------------------------------------------------------------ building
func _lbl(text: String, font: Font, size: int, color := Color.WHITE, parent: Node = null) -> Label:
	if parent == null:
		parent = self
	var l := Label.new()
	l.text = text
	l.add_theme_font_override("font", font)
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", color)
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(l)
	return l


func _tex(path: String, parent: Node = null) -> TextureRect:
	if parent == null:
		parent = self
	var r := TextureRect.new()
	r.texture = load(path)
	r.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	r.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	r.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(r)
	return r


func _sb(bg: Color, border := Color(0, 0, 0, 0), bw := 0, margin := Vector2(14, 6)) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = bg
	s.border_color = border
	s.set_border_width_all(bw)
	s.content_margin_left = margin.x
	s.content_margin_right = margin.x
	s.content_margin_top = margin.y
	s.content_margin_bottom = margin.y
	return s


func _button(text: String, size: int, primary := false) -> Button:
	var b := Button.new()
	b.text = text
	b.add_theme_font_override("font", F_PIX)
	b.add_theme_font_size_override("font_size", size)
	b.add_theme_color_override("font_color", Color.BLACK if primary else Color.WHITE)
	b.add_theme_color_override("font_hover_color", Color.BLACK)
	b.add_theme_color_override("font_pressed_color", Color.WHITE)
	b.add_theme_color_override("font_focus_color", Color.BLACK if primary else Color.WHITE)
	b.add_theme_color_override("font_disabled_color", Color(1, 1, 1, 0.25))
	b.add_theme_stylebox_override("normal", _sb(Color.WHITE if primary else Color(0, 0, 0, 0.55), Color(1, 1, 1, 0.9), 1))
	b.add_theme_stylebox_override("hover", _sb(GOLD if primary else Color.WHITE, Color.WHITE, 1))
	b.add_theme_stylebox_override("pressed", _sb(RED, RED, 1))
	b.add_theme_stylebox_override("disabled", _sb(Color(0, 0, 0, 0.4), Color(1, 1, 1, 0.15), 1))
	b.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	b.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	b.mouse_entered.connect(func():
		if not b.disabled:
			_play("hover", -14.0))
	b.pressed.connect(func(): _play("press", -10.0))
	return b


func _build_ui() -> void:
	var bg := ColorRect.new()
	bg.color = Color("09090b")
	bg.size = Vector2(W, H)
	add_child(bg)

	# faint line art behind the text column
	var ghost := _tex("res://assets/art/endsplash.png")
	ghost.position = Vector2(-60, -40)
	ghost.size = Vector2(640, 720)
	ghost.modulate = Color(1, 1, 1, 0.045)

	# right side: hero art + pixel strip + barcode + cipher text
	var cipher := _lbl("ЯJOYEUSE ЦИКАДАMATA СДИРАЙПЛОТЬ", F_CIPHER, 96, Color(1, 1, 1, 0.05))
	cipher.position = Vector2(560, 470)
	var strip := _tex("res://assets/art/menuoverlay.png")
	strip.size = Vector2(770, H)
	strip.position = Vector2(W - 770 + 80, 0)
	strip.modulate = Color(1, 1, 1, 0.9)
	hero = _tex("res://assets/art/deployingfawn.png")
	hero.size = Vector2(600, 675)
	hero_base_y = 14
	hero.position = Vector2(W - 560, hero_base_y)
	var bunny := _tex("res://assets/art/SplashScreen__sel_bnu.png")
	bunny.size = Vector2(84, 84)
	bunny.position = Vector2(W - 120, H - 120)
	bunny.modulate = Color(1, 1, 1, 0.85)
	var code := _tex("res://assets/art/fawnid.png")
	code.size = Vector2(240, 45)
	code.position = Vector2(W - 380, H - 62)
	code.modulate = Color(1, 1, 1, 0.7)
	for p in [Vector2(640, 64), Vector2(1060, 64), Vector2(700, 596)]:
		var plus := _lbl("+", F_SANS, 34, Color(1, 1, 1, 0.8))
		plus.position = p

	# left column
	var x := 72.0
	var eg := _tex("res://assets/logo_glow.png")
	eg.size = Vector2(96, 96)
	eg.position = Vector2(x - 21, 13)
	eg.modulate = Color(1, 1, 1, 0.8)
	var emblem := _tex("res://assets/logo_white.png")
	emblem.size = Vector2(54, 54)
	emblem.position = Vector2(x, 34)
	var nf := _lbl("NOTFOUND", F_BIG, 34, Color.WHITE)
	nf.position = Vector2(x + 66, 34)
	var vpn := _lbl("VPN", F_BIG, 16, RED)
	vpn.position = Vector2(x + 66 + F_BIG.get_string_size("NOTFOUND", HORIZONTAL_ALIGNMENT_LEFT, -1, 34).x + 3, 34)
	var pres := _lbl("+ ПРЕДСТАВЛЯЕТ", F_PIX, 12, GREY)
	pres.position = Vector2(x + 68, 72)

	var title := _lbl("CICADAMATA\"", F_BIG, 82, Color.WHITE)
	title.position = Vector2(x - 4, 112)
	var sub := _lbl("РУССКАЯ ЛОКАЛИЗАЦИЯ", F_PIX, 27, RED)
	sub.position = Vector2(x, 202)
	var ver := _lbl("+ ПОЛНЫЙ ПЕРЕВОД + ВЕРСИЯ 2.0 + ДЛЯ STEAM-ВЕРСИИ +", F_PIX, 13, GREY)
	ver.position = Vector2(x, 240)

	# terminal
	var term := Panel.new()
	term.position = Vector2(x, 276)
	term.size = Vector2(540, 158)
	term.add_theme_stylebox_override("panel", _sb(Color(0, 0, 0, 0.72), Color(1, 1, 1, 0.55), 1))
	add_child(term)
	var head := _lbl(" MATA\" VIEWER // ТЕРМИНАЛ ", F_PIX, 11, Color.BLACK, term)
	head.position = Vector2(12, -8)
	head.add_theme_stylebox_override("normal", _sb(Color.WHITE, Color.WHITE, 0, Vector2(2, 0)))
	log_rt = RichTextLabel.new()
	log_rt.bbcode_enabled = true
	log_rt.scroll_following = true
	log_rt.position = Vector2(14, 16)
	log_rt.size = Vector2(516, 136)
	log_rt.add_theme_font_override("normal_font", F_PIX)
	log_rt.add_theme_font_size_override("normal_font_size", 12)
	log_rt.add_theme_constant_override("line_separation", 4)
	log_rt.mouse_filter = Control.MOUSE_FILTER_IGNORE
	term.add_child(log_rt)
	log_rt.visible_characters = 0

	# game location
	var row := HBoxContainer.new()
	row.position = Vector2(x, 444)
	row.size = Vector2(540, 24)
	row.add_theme_constant_override("separation", 8)
	add_child(row)
	var pl := _lbl("> ИГРА НАХОДИТСЯ В:", F_PIX, 12, GREY, row)
	pl.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	pl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	game_pick = OptionButton.new()
	game_pick.add_theme_font_override("font", F_PIX)
	game_pick.add_theme_font_size_override("font_size", 11)
	game_pick.add_theme_stylebox_override("normal", _sb(Color(0, 0, 0, 0.55), Color(1, 1, 1, 0.6), 1, Vector2(8, 3)))
	game_pick.add_theme_stylebox_override("hover", _sb(Color(1, 1, 1, 0.15), Color.WHITE, 1, Vector2(8, 3)))
	game_pick.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	game_pick.visible = false
	game_pick.item_selected.connect(func(i: int): _set_game(found_games[i]))
	row.add_child(game_pick)
	btn_show = _button("ПОКАЗАТЬ", 11)
	row.add_child(btn_show)
	btn_show.pressed.connect(_on_show)
	btn_browse = _button("ИЗМЕНИТЬ", 11)
	row.add_child(btn_browse)
	btn_browse.pressed.connect(_on_browse)
	path_label = _lbl("—", F_PIX, 12, Color.WHITE)
	path_label.position = Vector2(x, 472)
	path_label.size = Vector2(540, 18)

	lang_check = CheckBox.new()
	lang_check.text = "ВКЛЮЧИТЬ РУССКИЙ ЯЗЫК В ИГРЕ"
	lang_check.button_pressed = true
	lang_check.position = Vector2(x - 4, 492)
	lang_check.add_theme_font_override("font", F_PIX)
	lang_check.add_theme_font_size_override("font_size", 12)
	for c in ["font_color", "font_hover_color", "font_pressed_color", "font_focus_color", "font_hover_pressed_color"]:
		lang_check.add_theme_color_override(c, Color.WHITE)
	lang_check.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	lang_check.add_theme_icon_override("checked", _box_icon(true))
	lang_check.add_theme_icon_override("unchecked", _box_icon(false))
	add_child(lang_check)

	# progress
	progress_box = Control.new()
	progress_box.position = Vector2(x, 524)
	add_child(progress_box)
	for i in 36:
		var b := ColorRect.new()
		b.size = Vector2(12, 8)
		b.position = Vector2(i * 15, 0)
		b.color = DIM
		progress_box.add_child(b)
		progress_blocks.append(b)
	progress_label = _lbl("", F_PIX, 10, GREY, progress_box)
	progress_label.position = Vector2(0, 11)

	# buttons
	var brow := HBoxContainer.new()
	brow.position = Vector2(x, 548)
	brow.add_theme_constant_override("separation", 10)
	add_child(brow)
	btn_install = _button("+ УСТАНОВИТЬ +", 17, true)
	brow.add_child(btn_install)
	btn_install.pressed.connect(_on_install)
	btn_launch = _button("+ ЗАПУСТИТЬ ИГРУ +", 17, true)
	btn_launch.visible = false
	brow.add_child(btn_launch)
	btn_launch.pressed.connect(func(): OS.shell_open("steam://rungameid/" + Patcher.APP_ID))
	btn_remove = _button("ВЕРНУТЬ ОРИГИНАЛ", 12)
	btn_remove.size_flags_vertical = Control.SIZE_FILL
	brow.add_child(btn_remove)
	btn_remove.pressed.connect(_on_remove)
	var quit := _button("ВЫХОД", 12)
	brow.add_child(quit)
	quit.pressed.connect(_quit)

	motto = _lbl("СДИРАЙ ПЛОТЬ С КОСТЕЙ", F_PIX, 13, RED)
	motto.position = Vector2(x, 598)
	var fine := _lbl("фанатский перевод · NOTFOUNDVPN · не связан с FLOWERGARDEN", F_PIX, 9, Color(1, 1, 1, 0.35))
	fine.position = Vector2(x, 618)

	# title bar
	var bar := Control.new()
	bar.size = Vector2(W, 30)
	bar.mouse_filter = Control.MOUSE_FILTER_PASS
	bar.gui_input.connect(func(e: InputEvent):
		if e is InputEventMouseButton and e.pressed and e.button_index == MOUSE_BUTTON_LEFT:
			get_window().start_drag())
	add_child(bar)
	var mini_b := _button("_", 11)
	mini_b.position = Vector2(W - 78, 6)
	mini_b.size = Vector2(32, 24)
	add_child(mini_b)
	mini_b.pressed.connect(func(): get_window().mode = Window.MODE_MINIMIZED)
	var close_b := _button("X", 11)
	close_b.position = Vector2(W - 42, 6)
	close_b.size = Vector2(32, 24)
	add_child(close_b)
	close_b.pressed.connect(_quit)

	# frame + CRT post effect
	var frame := Panel.new()
	frame.size = Vector2(W, H)
	frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	frame.add_theme_stylebox_override("panel", _sb(Color(0, 0, 0, 0), Color(1, 1, 1, 0.35), 1))
	add_child(frame)
	var post := ColorRect.new()
	post.size = Vector2(W, H)
	post.mouse_filter = Control.MOUSE_FILTER_IGNORE
	crt = ShaderMaterial.new()
	crt.shader = load("res://crt.gdshader")
	post.material = crt
	add_child(post)


func _box_icon(on: bool) -> Texture2D:
	var img := Image.create(18, 18, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	for i in 18:
		for j in [0, 17]:
			img.set_pixel(i, j, Color.WHITE)
			img.set_pixel(j, i, Color.WHITE)
	if on:
		img.fill_rect(Rect2i(4, 4, 10, 10), RED)
	return ImageTexture.create_from_image(img)


func _build_intro() -> void:
	intro = preload("res://intro.gd").new()
	intro.setup(self, F_BIG, F_PIX, F_CIPHER)
	add_child(intro)
	move_child(intro, get_child_count() - 2)   # under the CRT layer
	intro.finished.connect(_on_intro_done)
	var spec := _arg("--shot-intro=")
	if spec != "":
		var el := 0.0
		for item in spec.split(","):
			var at := float(item.get_slice("@", 1))
			await get_tree().create_timer(at - el).timeout
			el = at
			get_viewport().get_texture().get_image().save_png(item.get_slice("@", 0))


func _on_intro_done() -> void:
	intro = null
	_play("cicadamata", -6.0)
	var shot := _arg("--shot=")
	if shot != "":
		await get_tree().create_timer(4.0).timeout
		get_viewport().get_texture().get_image().save_png(shot)
		get_tree().quit()


func _arg(prefix: String) -> String:
	for a in OS.get_cmdline_user_args():
		if a.begins_with(prefix):
			return a.trim_prefix(prefix)
	return ""


# ------------------------------------------------------------------ effects / sound
func _load_sfx() -> void:
	var m := {"hover": "sndMenuHover", "press": "sndMenuPress", "back": "sndMenuBack", "reveal": "sndIntroReveal",
		"cicadamata": "cicadamata", "tick": "sndDialogueTick", "error": "sndAngelError", "done": "sndLevelUp",
		"unlock": "sndUnlock", "glitch": "uiGlitchShort4", "glitch2": "uiGlitchShort7", "term": "sndTerminalOpen", "exfil": "sndExfil"}
	for k in m:
		var s = load("res://assets/sfx/" + m[k] + ".sample")
		if s:
			sfx[k] = s
	for i in 6:
		var p := AudioStreamPlayer.new()
		add_child(p)
		players.append(p)


func _play(name: String, db := -8.0) -> void:
	if not sfx.has(name):
		return
	for p in players:
		if not p.playing:
			p.stream = sfx[name]
			p.volume_db = db
			p.play()
			return


func _pulse_glitch(amount: float) -> void:
	glitch = maxf(glitch, amount)


func _process(delta: float) -> void:
	t += delta
	glitch = move_toward(glitch, 0.0, delta * 3.0)
	glitch_timer -= delta
	if glitch_timer <= 0.0:
		glitch_timer = randf_range(3.5, 8.0)
		_pulse_glitch(randf_range(0.35, 0.7))
	if crt:
		crt.set_shader_parameter("glitch", glitch)
	if hero:
		hero.position.y = hero_base_y + sin(t * 0.9) * 5.0
		hero.position.x = W - 560 + (randf_range(-6, 6) if glitch > 0.3 else 0.0)
	if motto:
		motto.modulate.a = 0.75 + sin(t * 3.0) * 0.25
	# typewriter
	if log_rt:
		var total := log_rt.get_total_character_count()
		if log_rt.visible_characters < total:
			var before := log_rt.visible_characters
			log_rt.visible_characters = mini(total, before + maxi(1, int(log_speed * delta)))
			if int(t * 20) % 3 == 0:
				_play("tick", -26.0)
		elif not log_queue.is_empty():
			log_rt.append_text(log_queue.pop_front())


# ------------------------------------------------------------------ log / progress
func _log(text: String, kind := "info") -> void:
	var col: String = {"info": "#d8d8de", "ok": "#ffffff", "warn": "#d2b066", "err": "#e2475f", "dim": "#8a8a92"}.get(kind, "#ffffff")
	var line := "[color=%s]%s[/color]\n" % [col, text.replace("[", "[lb]")]
	if kind == "err":
		_play("error", -10.0)
		_pulse_glitch(1.0)
	log_queue.append(line)


func _set_progress(f: float, label: String) -> void:
	var n := int(round(f * progress_blocks.size()))
	for i in progress_blocks.size():
		progress_blocks[i].color = (RED if i == n - 1 and f < 1.0 else Color.WHITE) if i < n else DIM
	progress_label.text = "%s  %d%%" % [label, int(f * 100)]


# ------------------------------------------------------------------ flow
func _boot_sequence() -> void:
	_log("> MATA\" VIEWER: ИНИЦИАЛИЗАЦИЯ...", "dim")
	_log("+ ИНТЕРФЕЙС · ДИАЛОГИ · ТЕРМИНАЛЫ · СУБТИТРЫ · БРИФИНГИ", "dim")
	_log("+ РАНГИ · УРОВНИ · ВРАГИ · ПОЗЫВНЫЕ · ЛОКАЦИИ", "dim")
	_log("> ПОИСК CICADAMATA\" В БИБЛИОТЕКАХ STEAM...", "info")
	found_games = patcher.find_games()
	if found_games.is_empty():
		_log("! ИГРА НЕ НАЙДЕНА. НАЖМИ «ИЗМЕНИТЬ» И УКАЖИ ПАПКУ ИГРЫ", "warn")
		_set_game("")
	else:
		_log("+ НАЙДЕНО УСТАНОВОК: %d" % found_games.size(), "ok")
		_log("+ " + _fit_path(found_games[0], 480.0), "ok")
		if found_games.size() > 1:
			for i in found_games.size():
				game_pick.add_item("УСТАНОВКА %d" % (i + 1), i)
			game_pick.visible = true
		_set_game(found_games[0])


func _set_game(dir: String) -> void:
	game_dir = dir
	path_label.text = _fit_path(dir) if dir != "" else "игра не найдена — нажми «ИЗМЕНИТЬ» и укажи папку"
	path_label.tooltip_text = dir
	btn_show.disabled = dir == ""
	btn_install.visible = true
	btn_launch.visible = false
	if dir == "":
		state = ""
		btn_install.disabled = true
		btn_remove.disabled = true
		return
	state = patcher.pck_state(dir.path_join(Patcher.PCK_NAME))
	var has_orig := FileAccess.file_exists(dir.path_join(Patcher.ORIG_NAME))
	match state:
		"original":
			_log("+ СОСТОЯНИЕ: ОРИГИНАЛ (АНГЛИЙСКИЙ)", "info")
			btn_install.text = "+ УСТАНОВИТЬ +"
		"ru1":
			_log("+ СОСТОЯНИЕ: СТАРЫЙ ПЕРЕВОД v1 (НЕПОЛНЫЙ)", "warn")
			btn_install.text = "+ ОБНОВИТЬ ДО v2 +"
		"ru2":
			_log("+ СОСТОЯНИЕ: ПЕРЕВОД v2 УЖЕ УСТАНОВЛЕН", "ok")
			btn_install.text = "+ ПЕРЕУСТАНОВИТЬ +"
		_:
			_log("! НЕ УДАЛОСЬ ПРОЧИТАТЬ CICADAMATA.pck", "err")
	btn_install.disabled = state == "unknown"
	btn_remove.disabled = state == "original" and not has_orig


func _fit_path(p: String, maxw := 540.0) -> String:
	if F_PIX.get_string_size(p, HORIZONTAL_ALIGNMENT_LEFT, -1, 12).x <= maxw:
		return p
	var s := p
	while s.length() > 4 and F_PIX.get_string_size("…" + s, HORIZONTAL_ALIGNMENT_LEFT, -1, 12).x > maxw:
		s = s.substr(1)
	return "…" + s


func _on_show() -> void:
	if game_dir == "":
		_log("! СНАЧАЛА УКАЖИ ПАПКУ ИГРЫ", "warn")
		return
	_log("> ОТКРЫВАЮ ПАПКУ ИГРЫ", "info")
	var pck := game_dir.path_join(Patcher.PCK_NAME)
	if OS.shell_show_in_file_manager(pck) != OK:
		OS.shell_open(game_dir)


func _on_browse() -> void:
	var fd := FileDialog.new()
	fd.file_mode = FileDialog.FILE_MODE_OPEN_DIR
	fd.access = FileDialog.ACCESS_FILESYSTEM
	fd.use_native_dialog = true
	fd.title = "Папка CICADAMATA (где лежит CICADAMATA.pck)"
	add_child(fd)
	fd.dir_selected.connect(func(d: String):
		if patcher.is_game_dir(d):
			_log("+ ВЫБРАНО: " + _fit_path(d, 400.0), "ok")
			_set_game(d)
		else:
			_log("! В ЭТОЙ ПАПКЕ НЕТ CICADAMATA.pck", "err")
		fd.queue_free())
	fd.canceled.connect(fd.queue_free)
	fd.popup_centered(Vector2i(820, 520))


func _lock(on: bool) -> void:
	busy = on
	for b in [btn_install, btn_remove, btn_browse, btn_show]:
		b.disabled = on
	lang_check.disabled = on


func _on_install() -> void:
	if busy or game_dir == "":
		return
	_lock(true)
	_set_progress(0.0, "ПОДГОТОВКА")
	_play("term", -12.0)
	worker = Thread.new()
	var ru := lang_check.button_pressed
	worker.start(func(): return patcher.install(game_dir, ru))
	_wait_worker("install")


func _on_remove() -> void:
	if busy or game_dir == "":
		return
	_lock(true)
	_set_progress(0.0, "ПОДГОТОВКА")
	worker = Thread.new()
	worker.start(func(): return patcher.restore(game_dir))
	_wait_worker("remove")


func _wait_worker(kind: String) -> void:
	while worker.is_alive():
		await get_tree().process_frame
	var err: String = worker.wait_to_finish()
	worker = null
	_lock(false)
	if err != "":
		_log("! " + err, "err")
		_set_progress(0.0, "ОШИБКА")
		_set_game(game_dir)
		return
	if kind == "install":
		_log("+ ГОТОВО. ПЕРЕВОД УСТАНОВЛЕН", "ok")
		_log("+ ЯЗЫК: НАСТРОЙКИ → ИГРА → ЯЗЫК / LANGUAGE", "info")
		_play("done", -6.0)
		_pulse_glitch(1.0)
		state = "ru2"
		btn_install.visible = false
		btn_launch.visible = true
		btn_remove.disabled = false
	else:
		_log("+ ОРИГИНАЛ ВОССТАНОВЛЕН. ДО ВСТРЕЧИ, ЦИКАДА", "ok")
		_play("back", -8.0)
		_set_game(game_dir)


func _quit() -> void:
	if busy:
		_log("! ДОЖДИСЬ ОКОНЧАНИЯ ОПЕРАЦИИ", "warn")
		return
	_play("back", -8.0)
	var tw := create_tween()
	tw.tween_callback(func(): _pulse_glitch(1.0))
	tw.tween_property(self, "modulate:a", 0.0, 0.3)
	tw.tween_callback(get_tree().quit)
