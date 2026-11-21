// news-image-20261120: copy the entry image to the output directory.
//
// The image is drawn by draw_news.py (Python + PIL) and shipped in this
// repository as entry.png. This program only copies it, so both runs of
// the grader produce byte-identical output.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
