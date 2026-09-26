"""VMAP 1.0 manifest (inline VAST 3.0) for the selected breaks, plus generated slate creatives."""
from __future__ import annotations

import hashlib
from pathlib import Path
from xml.sax.saxutils import escape

from .media import run

# ffmpeg on Windows usually has no fontconfig, so drawtext needs an explicit font file.
FONTS = ("C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/System/Library/Fonts/Helvetica.ttc")


def _offset(seconds: float) -> str:
    millis = round(seconds * 1000)
    hours, rest = divmod(millis, 3_600_000)
    minutes, rest = divmod(rest, 60_000)
    secs, ms = divmod(rest, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"


def build_vmap(candidates: list[dict], catalogue: list[dict], creative_url: str) -> str:
    """One linear AdBreak per selected candidate, using the creative chosen for that break.
    `creative_url` is a template containing {brand_id} and {creative_id}."""
    brands = {b["brand_id"]: b for b in catalogue}
    breaks = []
    for c in sorted((c for c in candidates if c.get("selected") and c.get("brand") and c.get("creative")), key=lambda c: c["time"]):
        brand = brands.get(c["brand"]["brand_id"])
        if brand is None:
            continue
        creative = c["creative"]
        duration = _offset(creative["duration"]).split(".")[0]
        media = escape(creative_url.format(brand_id=brand["brand_id"], creative_id=creative["id"]))
        breaks.append(f"""  <vmap:AdBreak timeOffset="{_offset(c['time'])}" breakType="linear" breakId="{escape(c['cand_id'])}">
    <vmap:AdSource id="{escape(c['cand_id'])}-src" allowMultipleAds="false" followRedirects="true">
      <vmap:VASTAdData>
        <VAST version="3.0">
          <Ad id="{escape(creative['id'])}">
            <InLine>
              <AdSystem>Drishti</AdSystem>
              <AdTitle>{escape(brand['name'])}</AdTitle>
              <Creatives>
                <Creative>
                  <Linear>
                    <Duration>{duration}</Duration>
                    <MediaFiles>
                      <MediaFile delivery="progressive" type="video/mp4" width="1280" height="720"><![CDATA[{media}]]></MediaFile>
                    </MediaFiles>
                  </Linear>
                </Creative>
              </Creatives>
            </InLine>
          </Ad>
        </VAST>
      </vmap:VASTAdData>
    </vmap:AdSource>
  </vmap:AdBreak>""")
    body = "\n".join(breaks)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<vmap:VMAP xmlns:vmap="http://www.iab.net/videosuite/vmap" version="1.0">\n{body}\n</vmap:VMAP>\n'


def ensure_creative(brand: dict, creative: dict, creatives_root: Path, cache_dir: Path, ffmpeg: str) -> Path:
    """The catalogue's creative file if it exists (relative to creatives_root), otherwise a generated slate of the same length."""
    if creative.get("url"):
        path = (creatives_root / creative["url"]).resolve()
        if path.is_file():
            return path
    target = cache_dir / f"{creative['id']}.mp4"
    if target.is_file():
        return target
    cache_dir.mkdir(parents=True, exist_ok=True)
    duration = f"{creative['duration']:.2f}"
    color = "0x" + hashlib.md5(brand["brand_id"].encode()).hexdigest()[:6]
    text = brand["name"].replace("\\", "").replace(":", "").replace("'", "")
    base = [ffmpeg, "-y", "-f", "lavfi", "-i", f"color=c={color}:s=1280x720:r=25:d={duration}",
            "-f", "lavfi", "-i", f"sine=frequency=520:sample_rate=44100:duration={duration}"]
    tail = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(target)]
    font = next((f for f in FONTS if Path(f).is_file()), None)
    font_arg = f"fontfile='{font.replace(':', chr(92) + ':')}':" if font else ""
    try:
        run(base + ["-vf", f"drawtext={font_arg}text='{text}':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=(h-text_h)/2,"
                           f"drawtext={font_arg}text='Advertisement':fontcolor=white@0.7:fontsize=28:x=(w-text_w)/2:y=h-90"] + tail, timeout=120)
    except Exception:
        run(base + tail, timeout=120)  # ffmpeg built without drawtext/fonts: plain colour slate
    return target
