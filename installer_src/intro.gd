extends Control
## NOTFOUNDVPN studio splash, styled after the game's own CICADALINK VII boot:
##   A) retro login sequence  B) NOTFOUNDLINK wordmark  C) emblem seal with rotating ring text.

signal finished

const RED := Color("c42b47")
const GREY := Color(0.58, 0.58, 0.62)
const W := 1120
const H := 640
const CENTER := Vector2(W / 2.0, 272)
const RING_TEXT := "СДИРАЙ ПЛОТЬ С КОСТЕЙ + NOTFOUNDVPN + РУССКАЯ ЛОКАЛИЗАЦИЯ + "
const SCRAMBLE := "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789#%&+/<>ЖЯЦШ"

var host: Node
var F_BIG: Font
var F_PIX: Font
var F_CIPHER: Font
var F_SERIF: Font = preload("res://assets/fonts/NotoSerifDisplay-Black.ttf")

var stage := "A"
var t := 0.0
var ending := false
var last_tick := -1

# A: login
var boot_left: Label
var boot_right: Label
var spinner := false
# B: wordmark
var logo_box: Control
var logo_clip := 0.0
# C: seal
var emblem: TextureRect
var emat: ShaderMaterial
var glow: TextureRect
var ring_alpha := 0.0
var ring_rot := 0.0
var ring_reveal := 0.0
var bracket := 0.0
var pulses: Array = []
var pres: Label
var tag: Label
var flash: ColorRect
var spores: CPUParticles2D


func setup(h: Node, big: Font, pix: Font, ciph: Font) -> void:
	host = h
	F_BIG = big
	F_PIX = pix
	F_CIPHER = ciph


func _lbl(text: String, font: Font, size: int, color: Color, parent: Node = null) -> Label:
	var l := Label.new()
	l.text = text
	l.add_theme_font_override("font", font)
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", color)
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	(parent if parent else self).add_child(l)
	return l


func _ready() -> void:
	size = Vector2(W, H)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var black := ColorRect.new()
	black.color = Color.BLACK
	black.size = size
	black.show_behind_parent = true
	add_child(black)

	# ---- A: login sequence (like the game's boot screen)
	boot_left = _lbl("", F_PIX, 12, Color.WHITE)
	boot_left.position = Vector2(150, 430)
	boot_left.add_theme_constant_override("line_spacing", 6)
	boot_right = _lbl("", F_PIX, 12, Color.WHITE)
	boot_right.position = Vector2(720, 430)
	boot_right.add_theme_constant_override("line_spacing", 6)

	# ---- B: NOTFOUNDLINK wordmark (after CICADALINK VII)
	logo_box = Control.new()
	logo_box.size = size
	logo_box.visible = false
	logo_box.clip_contents = true
	add_child(logo_box)
	var nw := F_SERIF.get_string_size("NOTFOUND", HORIZONTAL_ALIGNMENT_LEFT, -1, 92).x
	var vw := F_BIG.get_string_size("VPN", HORIZONTAL_ALIGNMENT_LEFT, -1, 112).x
	var lx := W / 2.0 - (nw + 16 + vw) / 2.0
	var word := _lbl("NOTFOUND", F_SERIF, 92, Color.WHITE, logo_box)
	word.position = Vector2(lx, 196)
	var vpn := _lbl("VPN", F_BIG, 112, Color.WHITE, logo_box)
	vpn.position = Vector2(lx + nw + 16, 186)
	var bar := ColorRect.new()
	bar.color = Color.WHITE
	bar.position = Vector2(lx + 4, 322)
	bar.size = Vector2(nw - 8, 22)
	logo_box.add_child(bar)
	var code := _lbl("NOTFOUNDVPN NOTFOUNDVPN NOTFOUNDVPN NOTFOUNDVPN", F_CIPHER, 15, Color.BLACK, bar)
	code.position = Vector2(4, 0)
	bar.clip_contents = true
	var motto := _lbl("Г д е   и н ф о р м а ц и я   о б р е т а е т   я з ы к   в   с о в е р ш е н н о й   г а р м о н и и", F_PIX, 9, Color.WHITE, logo_box)
	motto.position = Vector2(lx + 4, 350)
	var red := ColorRect.new()
	red.color = RED
	red.position = Vector2(lx + nw + 18, 322)
	red.size = Vector2(vw - 6, 22)
	logo_box.add_child(red)
	var ru := _lbl("RU", F_PIX, 14, Color.WHITE, red)
	ru.position = Vector2(8, 2)

	# ---- C: seal
	spores = CPUParticles2D.new()
	spores.texture = load("res://assets/px.png")
	spores.amount = 80
	spores.lifetime = 7.0
	spores.preprocess = 7.0
	spores.position = Vector2(W / 2.0, H + 10)
	spores.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	spores.emission_rect_extents = Vector2(W / 2.0, 4)
	spores.direction = Vector2(0, -1)
	spores.spread = 14.0
	spores.gravity = Vector2.ZERO
	spores.initial_velocity_min = 20.0
	spores.initial_velocity_max = 75.0
	spores.scale_amount_min = 0.25
	spores.scale_amount_max = 0.8
	var ramp := Gradient.new()
	ramp.set_color(0, Color(1, 1, 1, 0))
	ramp.add_point(0.25, Color(1, 1, 1, 0.3))
	ramp.add_point(0.7, Color(1, 0.3, 0.42, 0.25))
	ramp.set_color(ramp.get_point_count() - 1, Color(1, 1, 1, 0))
	spores.color_ramp = ramp
	spores.visible = false
	add_child(spores)

	glow = TextureRect.new()
	glow.texture = load("res://assets/logo_glow.png")
	glow.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	glow.size = Vector2(380, 380)
	glow.position = CENTER - glow.size / 2.0
	glow.modulate.a = 0.0
	glow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(glow)
	emblem = TextureRect.new()
	emblem.texture = load("res://assets/logo_white.png")
	emblem.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	emblem.size = Vector2(236, 236)
	emblem.pivot_offset = emblem.size / 2.0
	emblem.position = CENTER - emblem.size / 2.0
	emblem.mouse_filter = Control.MOUSE_FILTER_IGNORE
	emat = ShaderMaterial.new()
	emat.shader = load("res://emblem.gdshader")
	emblem.material = emat
	emblem.visible = false
	add_child(emblem)
	pres = _lbl("", F_PIX, 14, GREY)
	pres.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	pres.size = Vector2(W, 20)
	pres.position = Vector2(0, 512)
	tag = _lbl("", F_PIX, 10, Color(1, 1, 1, 0.45))
	tag.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	tag.size = Vector2(W, 16)
	tag.position = Vector2(0, 538)

	var skip := _lbl("+ НАЖМИ ЛЮБУЮ КНОПКУ +", F_PIX, 9, Color(1, 1, 1, 0.22))
	skip.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	skip.size = Vector2(W, 14)
	skip.position = Vector2(0, H - 28)
	flash = ColorRect.new()
	flash.color = Color(1, 1, 1, 0)
	flash.size = size
	flash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(flash)
	_sequence()


# ------------------------------------------------------------------ timeline
func _type(l: Label, text: String, dur: float) -> Callable:
	return func(v: float):
		var n := int(v * text.length())
		if n != l.get_meta("n", -1):
			l.set_meta("n", n)
			l.text = text.left(n)
			if n % 2 == 0:
				host._play("tick", -24.0)


func _sequence() -> void:
	var left := "Инициализация последовательности входа\nЗагрузка сцен и актёров"
	var right := "ОНЭЙ-сервер\nNFVPN-сервер\nconnect: поиск хоста\n        : notfound.vpn"
	var tw := create_tween()
	tw.tween_callback(func(): host._play("term", -12.0))
	tw.tween_interval(0.25)
	tw.tween_method(_type(boot_left, left, 0.7), 0.0, 1.0, 0.7)
	tw.tween_callback(func(): spinner = true)
	tw.tween_method(_type(boot_right, right, 0.8), 0.0, 1.0, 0.8)
	tw.tween_interval(0.45)
	# B
	tw.tween_callback(_to_logo)
	tw.tween_property(self, "logo_clip", 1.0, 0.5).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	tw.tween_interval(1.25)
	# C
	tw.tween_callback(_to_seal)
	tw.tween_property(self, "bracket", 1.0, 0.5).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	tw.parallel().tween_method(_set_sweep, 0.0, 1.0, 1.1).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tw.parallel().tween_property(self, "ring_reveal", 1.0, 1.3).set_delay(0.1)
	tw.tween_callback(_slam)
	tw.tween_method(func(v: float): emat.set_shader_parameter("core", v), 0.0, 1.0, 0.16)
	tw.parallel().tween_property(emblem, "scale", Vector2.ONE, 0.35).from(Vector2(1.14, 1.14)).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.parallel().tween_property(glow, "modulate:a", 0.8, 0.5)
	tw.tween_method(_type(pres, "+ ПРЕДСТАВЛЯЕТ +", 0.4), 0.0, 1.0, 0.4)
	tw.tween_method(_type(tag, "РУССКАЯ ЛОКАЛИЗАЦИЯ // CICADAMATA\" // v2.0", 0.5), 0.0, 1.0, 0.5)
	tw.tween_interval(1.4)
	tw.tween_callback(close)


func _to_logo() -> void:
	stage = "B"
	boot_left.visible = false
	boot_right.visible = false
	spinner = false
	logo_box.visible = true
	host._play("reveal", -5.0)
	host._pulse_glitch(0.9)
	flash.color.a = 0.25


func _to_seal() -> void:
	stage = "C"
	host._pulse_glitch(1.0)
	host._play("glitch", -8.0)
	logo_box.visible = false
	emblem.visible = true
	spores.visible = true
	flash.color.a = 0.12


func _set_sweep(v: float) -> void:
	emat.set_shader_parameter("sweep", v)
	var k := int(v * 28.0)
	if k != last_tick:
		last_tick = k
		host._play("tick", -20.0)


func _slam() -> void:
	host._play("glitch2", -6.0)
	host._pulse_glitch(1.0)
	pulses.append([112.0, 0.9, 3.0])
	pulses.append([90.0, 0.6, 1.0])
	flash.color.a = 0.2


func close() -> void:
	if ending:
		return
	ending = true
	host._play("glitch", -6.0)
	host._pulse_glitch(1.0)
	var tw := create_tween()
	if emblem.visible:
		tw.tween_method(func(v: float): emat.set_shader_parameter("shatter", v), 0.0, 1.0, 0.45)
		tw.parallel().tween_property(emblem, "scale", Vector2(1.25, 1.25), 0.45).set_ease(Tween.EASE_IN)
	tw.parallel().tween_property(self, "ring_alpha", 0.0, 0.35)
	tw.parallel().tween_property(glow, "modulate:a", 0.0, 0.4)
	tw.parallel().tween_property(flash, "color:a", 0.55, 0.25).set_delay(0.15)
	tw.tween_callback(func(): finished.emit())
	tw.tween_property(self, "modulate:a", 0.0, 0.3)
	tw.tween_callback(queue_free)


func _gui_input(e: InputEvent) -> void:
	if t > 0.6 and e is InputEventMouseButton and e.pressed:
		print("INTRO skip: mouse ", e.button_index)
		close()


func _unhandled_input(e: InputEvent) -> void:
	if t > 0.6 and e is InputEventKey and e.pressed and not e.echo:
		print("INTRO skip: key ", e.keycode)
		close()


# ------------------------------------------------------------------ frame
func _process(delta: float) -> void:
	t += delta
	if not ending:
		flash.color.a = move_toward(flash.color.a, 0.0, delta * 1.2)
		if stage == "C":
			ring_alpha = move_toward(ring_alpha, 1.0, delta * 2.0)
			glow.modulate.a = clampf(glow.modulate.a + sin(t * 2.4) * 0.004, 0.0, 0.9)
	ring_rot += delta * 0.22
	if stage == "B":
		logo_box.size = Vector2(W, lerpf(150.0, 400.0, logo_clip))
	for p in pulses:
		p[0] += delta * 240.0
		p[1] = maxf(0.0, p[1] - delta * 0.9)
	pulses = pulses.filter(func(p): return p[1] > 0.0)
	queue_redraw()


func _draw() -> void:
	if stage == "A":
		if spinner:
			var c := Vector2(150 + F_PIX.get_string_size("Загрузка сцен и актёров", HORIZONTAL_ALIGNMENT_LEFT, -1, 12).x + 18, 430 + 30)
			for i in 10:
				var a := t * 7.0 + i * TAU / 12.0
				draw_rect(Rect2(c + Vector2.from_angle(a) * 8.0 - Vector2(1.5, 1.5), Vector2(3, 3)), Color(1, 1, 1, float(i + 2) / 12.0))
		return
	if stage == "B":
		# scanline wipe revealing the wordmark
		if logo_clip < 1.0:
			draw_rect(Rect2(0, lerpf(150.0, 400.0, logo_clip), W, 2), Color(1, 1, 1, 0.6))
		return
	# stage C: dot grid, rings, seal text, HUD
	for gx in range(16, W, 32):
		for gy in range(16, H, 32):
			draw_rect(Rect2(gx, gy, 2, 2), Color(1, 1, 1, 0.045))
	for p in pulses:
		draw_arc(CENTER, p[0], 0.0, TAU, 96, Color(RED.r, RED.g, RED.b, p[1]), p[2], true)
	var ra := ring_alpha
	draw_arc(CENTER, 150.0, 0.0, TAU, 128, Color(1, 1, 1, 0.55 * ra), 2.0, true)
	draw_arc(CENTER, 212.0, 0.0, TAU, 128, Color(1, 1, 1, 0.55 * ra), 2.0, true)
	draw_arc(CENTER, 218.0, 0.0, TAU, 128, Color(1, 1, 1, 0.2 * ra), 1.0, true)
	_draw_ring_text(CENTER, 181.0, 26, ra)
	for i in 72:
		var ang := -ring_rot * 0.6 + TAU * i / 72.0
		var r2 := 232.0 if i % 6 == 0 else 226.0
		draw_line(CENTER + Vector2.from_angle(ang) * 222.0, CENTER + Vector2.from_angle(ang) * r2, Color(1, 1, 1, 0.3 * ra), 1.0)
	var m := 34.0
	var L := 60.0 * bracket
	var col := Color(1, 1, 1, 0.75 * bracket)
	for corner in [Vector2(m, m), Vector2(W - m, m), Vector2(m, H - m), Vector2(W - m, H - m)]:
		var sx := 1.0 if corner.x < W / 2.0 else -1.0
		var sy := 1.0 if corner.y < H / 2.0 else -1.0
		draw_line(corner, corner + Vector2(L * sx, 0), col, 2.0)
		draw_line(corner, corner + Vector2(0, L * sy), col, 2.0)
	if bracket > 0.9:
		var dim := Color(1, 1, 1, 0.4)
		draw_string(F_PIX, Vector2(m + 8, m + 24), "NOTFOUNDLINK VII", HORIZONTAL_ALIGNMENT_LEFT, -1, 10, dim)
		draw_string(F_PIX, Vector2(W - m - 150, m + 24), "SIG %06.2f" % fmod(t * 37.13, 999.99), HORIZONTAL_ALIGNMENT_LEFT, -1, 10, dim)
		draw_string(F_PIX, Vector2(m + 8, H - m - 12), "+ 7ПС / ОНЭЙР", HORIZONTAL_ALIGNMENT_LEFT, -1, 10, Color(RED.r, RED.g, RED.b, 0.75))
		draw_string(F_PIX, Vector2(W - m - 150, H - m - 12), "REC +", HORIZONTAL_ALIGNMENT_LEFT, -1, 10, Color(1, 1, 1, 0.4 + 0.4 * float(int(t * 2) % 2)))


## Seal text around the emblem, like the game's "COME HEAVEN OR HIGH WATER" stamp.
func _draw_ring_text(c: Vector2, r: float, fs: int, alpha: float) -> void:
	if alpha <= 0.0:
		return
	var widths: Array[float] = []
	var total := 0.0
	for ch in RING_TEXT:
		var w := F_SERIF.get_string_size(ch, HORIZONTAL_ALIGNMENT_LEFT, -1, fs).x
		widths.append(w)
		total += w
	# shrink the font if the phrase is longer than the circle, spread it evenly otherwise
	var circ := TAU * r * 0.97
	if total > circ:
		var k := circ / total
		fs = int(fs * k)
		for i in widths.size():
			widths[i] *= k
		total *= k
	var a := -PI / 2.0 + ring_rot
	var asc := F_SERIF.get_ascent(fs) * 0.72
	for i in RING_TEXT.length():
		var step := widths[i] / total * TAU
		var mid := a + step / 2.0
		var shown := float(i) / RING_TEXT.length() <= ring_reveal
		if shown and RING_TEXT[i] != " ":
			draw_set_transform(c + Vector2.from_angle(mid) * r, mid + PI / 2.0, Vector2.ONE)
			draw_char(F_SERIF, Vector2(-widths[i] / 2.0, asc / 2.0), RING_TEXT[i], fs, Color(1, 1, 1, 0.92 * alpha))
		a += step
	draw_set_transform_matrix(Transform2D())
