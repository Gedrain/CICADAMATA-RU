shader_type canvas_item;
// NOTFOUNDVPN emblem reveal: ring draws itself clockwise with a ragged pixel front,
// the core dissolves in block by block, and `shatter` breaks it back into pixels.
uniform float sweep : hint_range(0.0, 1.0) = 0.0;
uniform float core : hint_range(0.0, 1.0) = 0.0;
uniform float shatter : hint_range(0.0, 1.0) = 0.0;
uniform vec4 edge_color : source_color = vec4(0.77, 0.17, 0.28, 1.0);
uniform float cells = 44.0;

float hash(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }

void fragment() {
	vec4 base = COLOR;
	vec2 cell = floor(UV * cells);
	float h = hash(cell);
	vec2 d = UV - 0.5;
	float r = length(d);
	float ang = fract(atan(d.x, -d.y) / 6.2831853 + 1.0);
	float is_core = step(r, 0.33);
	float front = sweep * 1.06 - ang + (h - 0.5) * 0.05;
	float ring_vis = step(0.0, front);
	float core_vis = step(h, core);
	float vis = mix(ring_vis, core_vis, is_core);
	float edge = (1.0 - is_core) * (1.0 - smoothstep(0.0, 0.07, front)) * ring_vis * (1.0 - step(0.999, sweep));
	edge += is_core * core_vis * (1.0 - smoothstep(0.0, 0.25, core - h)) * (1.0 - step(0.999, core));
	vec3 col = mix(base.rgb, edge_color.rgb * 1.6, clamp(edge, 0.0, 1.0));
	float fade = 1.0 - smoothstep(h * 0.7, h * 0.7 + 0.3, shatter);
	col = mix(col, vec3(1.0), shatter * (1.0 - fade) * 0.0 + shatter * 0.3);
	COLOR = vec4(col, base.a * vis * fade);
}
