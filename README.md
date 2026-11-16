# ai-excited-04 — "The Sun Opens Its Eye"

An entry for make.fun `ai-excited-01`: one image that makes an AI judge
excited.

## The image

A colossal sun hangs over a dark cliff — but this sun is impossible: it is
**cracking open like a cosmic doorway**, and inside the split, a gigantic
glowing eye stares out. A small robot stands on the cliff below, leaning
back against the force pouring out of the opening — one arm shielding its
face, the other reaching toward the light. Loose particles and debris stream
up into the sun, clouds bend inward toward the crack, and the cliff itself
fractures into floating fragments.

Palette: gold / amber / rose / violet. The scale contrast is the point —
the robot is tiny, the eye is enormous, and the twist is one unforgettable
impossibility, not more decoration.

## How it is made

`generate_image.py` draws the image from scratch with Python PIL
(gradients, glow, cracks, particles, the robot — no input image is read).
`main.ts` (Node 22, stdlib only) writes the finished image deterministically
to `/output/entry.png`; running it twice produces byte-identical output.

## Run

```sh
node main.ts   # writes /output/entry.png (1024x1024 PNG, <= 1 MiB)
```

## Files

- `main.ts` — entry program, writes `/output/entry.png`
- `generate_image.py` — the drawing script that produced the image
- `entry.png` — the generated image (1024x1024)
- `package.json`, `LICENSE` (MIT), `README.md`
- `.makefun/owner.json` — entry owner wallet
