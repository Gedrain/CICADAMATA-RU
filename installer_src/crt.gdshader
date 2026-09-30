shader_type canvas_item;
// Full-screen post effect: scanlines, vignette, grain and glitch (chromatic split + row tearing).

uniform sampler2D screen_tex : hint_screen_texture, filter_nearest;
uniform float glitch : hint_range(0.0, 1.0) = 0.0;
uniform float scan_strength : hint_range(0.0, 1.0) = 0.16;
uniform float vignette : hint_range(0.0, 2.0) = 0.9;

float hash(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }

void fragment() {
	vec2 uv = SCREEN_UV;
	float t = TIME;
	// row tearing while glitching
	float row = floor(uv.y * 90.0);
	float tear = step(1.0 - glitch * 0.35, hash(vec2(row, floor(t * 24.0))));
	uv.x += tear * (hash(vec2(row, t)) - 0.5) * 0.06 * glitch;
	float split = 0.0015 + glitch * 0.008;
	vec3 col;
	col.r = texture(screen_tex, uv + vec2(split, 0.0)).r;
	col.g = texture(screen_tex, uv).g;
	col.b = texture(screen_tex, uv - vec2(split, 0.0)).b;
	// scanlines
	float sl = sin(FRAGCOORD.y * 3.14159) * 0.5 + 0.5;
	col *= 1.0 - scan_strength * sl;
	// grain
	col += (hash(FRAGCOORD.xy + t * 60.0) - 0.5) * 0.035;
	// vignette
	vec2 d = SCREEN_UV - 0.5;
	col *= 1.0 - dot(d, d) * vignette;
	COLOR = vec4(col, 1.0);
}
