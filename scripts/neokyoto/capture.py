"""Film the Neo-Kyoto title page: step window.renderAt(t) frame by frame and encode WebP.

The page exposes window.ready and window.renderAt(t). Frames are captured one
at a time, so timing never depends on how fast the software GPU is, and every
frame is a keyframe (partial frames leave rectangle ghosts on dark ground).
The page renders at --scale times the output size and each frame is reduced
with a Lanczos filter; --sub averages that many sub-frames across a half-frame
shutter for motion blur. Each sub-frame also passes the frame's own time, so a
page with camera cuts can keep every sub-frame on the same side of a cut.

    python capture.py neokyoto.html neokyoto-hero.webp --seconds 17.5 --fps 24 --sub 3 \n        --scale 2 --width 1800 --keep frames

The profile's hero is those frames encoded at 1440 px, quality 80; the phone hero is
a 600 px crop of them centred on the pagoda.

--still takes one or more comma-separated times with a {t} slot in the path:
    python capture.py neokyoto.html - --still 3.0,9.5 shots/s{t}.png
"""
import argparse
import functools
import http.server
import io
import threading
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).parent
W, H = 1200, 560
RADIUS = 18


def serve(page: str) -> str:
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0), functools.partial(Quiet, directory=str(HERE)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{server.server_address[1]}/{page}"


def rounded(img: Image.Image) -> Image.Image:
    w, h = img.size
    alpha = Image.new("L", (w, h), 0)
    ImageDraw.Draw(alpha).rounded_rectangle((0, 0, w - 1, h - 1), RADIUS, fill=255)
    img.putalpha(alpha)
    return img


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("page")
    parser.add_argument("out", type=Path)
    parser.add_argument("--seconds", type=float, default=12.75)
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--quality", type=int, default=85)
    parser.add_argument("--scale", type=int, default=2)
    parser.add_argument("--sub", type=int, default=1)
    parser.add_argument("--still", nargs=2, metavar=("T", "PNG"))
    parser.add_argument("--width", type=int, default=W,
                        help="output width; rendering stays at the page size times --scale, so a smaller "
                             "width means more supersampling, not a blurrier render")
    parser.add_argument("--kmax", type=int, default=1,
                        help="max frames between keyframes; 1 makes every frame a keyframe")
    parser.add_argument("--keep", type=Path, help="also save every frame as PNG in this folder")
    parser.add_argument("--encode", type=Path, help="skip rendering; encode the PNG frames in this folder")
    args = parser.parse_args()
    if args.encode:
        encode([Image.open(f) for f in sorted(args.encode.glob("f*.png"))], args)
        return

    from playwright.sync_api import sync_playwright
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(args=[
            "--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
            "--ignore-gpu-blocklist"])
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=args.scale)
        errors: list[str] = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.goto(serve(args.page))
        try:
            page.wait_for_function("window.ready === true", timeout=180000)
        except Exception:
            raise SystemExit("page never became ready: " + " | ".join(errors[:5]))

        def grab(t: float, center: float) -> np.ndarray:
            page.evaluate(f"window.renderAt({t}, {center})")
            png = page.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
            big = Image.open(io.BytesIO(png)).convert("RGB")
            out_h = round(args.width * H / W)
            return np.asarray(big.resize((args.width, out_h), Image.LANCZOS), dtype=np.float32)

        def shot(t: float, sub: int) -> Image.Image:
            shutter = 0.5 / args.fps
            acc = sum(grab(t + shutter * (k / sub - 0.5), t) for k in range(sub)) if sub > 1 else grab(t, t)
            if sub > 1:
                acc = acc / sub
            return rounded(Image.fromarray(np.clip(acc + 0.5, 0, 255).astype(np.uint8)))

        if args.still:
            times, pattern = args.still
            for t in times.split(","):
                path = pattern.replace("{t}", t)
                Path(path).parent.mkdir(parents=True, exist_ok=True)
                started = time.perf_counter()
                shot(float(t), args.sub).save(path)
                print(path, f"{time.perf_counter() - started:.2f}s")
            print("timeline:", page.evaluate("JSON.stringify(window.timeline || null)"))
            print("errors:", errors[:3])
            browser.close()
            return
        count = round(args.seconds * args.fps)
        started = time.perf_counter()
        frames = []
        if args.keep:
            args.keep.mkdir(parents=True, exist_ok=True)
        for i in range(count):
            frames.append(shot(i / args.fps, args.sub))
            if args.keep:
                frames[-1].save(args.keep / f"f{i:04d}.png")
            if i % 24 == 0:
                print(f"frame {i}/{count} {time.perf_counter() - started:.0f}s", flush=True)
        print(f"{count} frames in {time.perf_counter() - started:.0f}s", "errors:", errors[:3])
        browser.close()
    encode(frames, args)


def encode(frames: list, args: argparse.Namespace) -> None:
    args.out.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(args.out, save_all=True, append_images=frames[1:],
                   duration=round(1000 / args.fps), loop=0, quality=args.quality,
                   method=4, kmin=0 if args.kmax == 1 else args.kmax - 1, kmax=args.kmax,
                   allow_mixed=False)
    print(args.out, len(frames), "frames", args.out.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
