#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XCONDA 발표 덱 — 에셋 일괄 다운로더 (영상 + 이미지)
====================================================
index.html은 `videos/`, `images/` 폴더의 파일을 **로컬 우선**으로 재생/표시하고,
파일이 없으면 Google Drive 스트리밍으로 자동 대체합니다.
Git 저장소에 함께 올릴 영상·이미지를 이 스크립트로 한 번에 받으세요.

사용법:
    python3 download_assets.py

- 이미 받아 놓은 파일은 건너뜁니다.
- Drive의 '바이러스 스캔 경고' 페이지를 자동 우회(confirm + uuid)합니다.
- 영상 총 용량이 약 3.5GB(트레일러 2편이 각 ~923MB)라 시간이 걸립니다.
"""
import os
import re
import urllib.request
import urllib.parse
import http.cookiejar

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# ---------------- 매니페스트 ----------------
VIDEOS = {
    "625_medical_center.mp4":      "17LssmurqbA25k3sFmYEhDdECljpV3nBY",
    "blockingboard_result.mp4":    "1_ACAVjHo4pxI_l7nC-cvPjLVR_S7F1Pv",
    "coldsite_trailer.mp4":        "1-oDok4XHLLe4DUewiKtnpYG86bCm8-Ox",
    "eiel_hybrid_01.mp4":          "1HSCxkRMGL8Bq-A7XIqTwURtrT2FtoKHS",
    "eiel_hybrid_composite.mp4":   "1fHSLCxaV5fDerV-PIwV6elbzJzwq2w19",
    "eiel_webdrama_trailer.mp4":   "13jH_tndgmbI7MOOOW02I2ADEMFXY6Ii8",
    "faceswap_mask_01.mp4":        "1VxPfGJ6ukJLvPn8czobmZ4YnDQPpl5Dk",
    "flexboard_result_final.mp4":  "1MUbSzzpHdrIt_bI2fe28hj08OIZtyHRH",
    "foreign_hybrid.mp4":          "1ie62hJRsdSlfuJhyrliLYrweRX96iel-",
    "gumiho.mp4":                  "11iuLIW6oUnxzFovBjFj0EJzpcRBEsNgb",
    "seedwar.mp4":                 "1jP4J4RbNFDlK3bZI5dWz_atj4pYMPFeo",
    "thousand_years.mp4":          "1OWlKxIH2LRfohRSSR2Fk46Ou2RdYmOya",
    "thousand_years_actor.mp4":    "1G0h9M3Tsfbke_P3HimiEp4JWn3J7lFZl",
    "thousandyears_yootaewoong.mp4": "1GUb9TZpxsdFu3dGjMlXN9vjJUqP5I3vJ",
    "toyfarm.mp4":                 "1o5pVmIcxeoCE4CEq090ememV_lj-IQF4",
}

IMAGES = {
    "1000yActor.jpg":              "1diEuh-GuLyUBRy2OpiSiCgO18otA5P-o",
    "1000yActor2.png":             "1sE-4DiwUc8sNe8MScyzeVNZPa_CAujlo",
    "coldsite_still.jpg":          "1rjv4GuDqkVqTL6WhfkQxOdzXbPn8Lb9w",
    "division_zero_still.jpg":     "1GeKap8aGxGKSEA4yHuR5xxQB1G5l9RYZ",
    "eiel_poster.jpg":             "1ZARO5oIS8Ls2-p2Dd7hOqTRkuRVAaVC9",
    "mokguryung_still.png":        "1QxlojJIikMFx9fUP5TAT4mrYX4W_TmBg",
    "thousandyears_character.png": "1pLoZ_EqqA8yeCgMnGclaGZbzPfqqxxqQ",
    "xconda_logo.png":             "1YBC-wtyhwJghb-StE9yoKqYQtuKxykAT",
    "xconda_qr_openchat.png":      "1WRrvYBzgWTbr-xvjvZn_iooLuqSSImZS",
}


def fetch(url, cj=None, timeout=1800):
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj or http.cookiejar.CookieJar()))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        return opener.open(req, timeout=timeout).read()
    except Exception as e:  # noqa: BLE001
        print("  [오류]", e)
        return b""


def looks_like_mp4(data):
    return b"ftyp" in data[:64] and len(data) > 100_000


def looks_like_img(data):
    if not data or len(data) < 500:
        return False
    return (data[:3] == b"\xff\xd8\xff" or            # jpg
            data[:8] == b"\x89PNG\r\n\x1a\n" or        # png
            data[:6] in (b"GIF87a", b"GIF89a") or     # gif
            data[:4] == b"RIFF")                      # webp


def download_video(name, fid):
    path = os.path.join("videos", name)
    if os.path.exists(path) and os.path.getsize(path) > 100_000:
        print(f"[건너뜀] videos/{name} (이미 있음)")
        return
    cj = http.cookiejar.CookieJar()
    print(f"[영상] {name} ...")
    page = fetch(f"https://drive.google.com/uc?export=download&id={fid}",
                 cj, timeout=120).decode("utf-8", "replace")
    conf = re.search(r'name="confirm"\s+value="([^"]+)"', page)
    uu = re.search(r'name="uuid"\s+value="([^"]+)"', page)
    confirm = conf.group(1) if conf else "t"
    uuid = uu.group(1) if uu else ""
    url = ("https://drive.usercontent.google.com/download?export=download&confirm="
           + urllib.parse.quote(confirm) + "&id=" + fid)
    if uuid:
        url += "&uuid=" + urllib.parse.quote(uuid)
    data = fetch(url, cj)
    if not looks_like_mp4(data):
        data = fetch("https://drive.usercontent.google.com/download"
                     "?export=download&confirm=t&id=" + fid, cj)
    if not looks_like_mp4(data):
        print(f"  [실패] {name} — 받은 데이터가 MP4가 아닙니다. Drive 권한 확인 필요.")
        return
    os.makedirs("videos", exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    print(f"  [완료] videos/{name} ({len(data)/1048576:.1f}MB)")


def download_image(name, fid):
    path = os.path.join("images", name)
    if os.path.exists(path) and os.path.getsize(path) > 500:
        print(f"[건너뜀] images/{name} (이미 있음)")
        return
    print(f"[이미지] {name} ...")
    data = b""
    for url in [f"https://lh3.googleusercontent.com/d/{fid}",
                f"https://drive.google.com/uc?export=view&id={fid}",
                f"https://drive.usercontent.google.com/download?id={fid}&export=view"]:
        data = fetch(url, timeout=120)
        if looks_like_img(data):
            break
    if not looks_like_img(data):
        print(f"  [실패] {name} — Drive 권한 확인 필요.")
        return
    os.makedirs("images", exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    print(f"  [완료] images/{name} ({len(data)/1024:.0f}KB)")


if __name__ == "__main__":
    print("=== 영상 ===")
    for name, fid in VIDEOS.items():
        download_video(name, fid)
    print("\n=== 이미지 ===")
    for name, fid in IMAGES.items():
        download_image(name, fid)
    print("\n끝.")
    print("이미 준비된 파일: videos/blockingboard_intro.mp4, videos/flexboard_intro.mp4")
    print("(이병욱 셀카 leebyoungwook_selca.jpg는 index.html에 내장되어 있어 별도 파일 불필요)")
    print("\nGit에 올릴 때는 Git LFS 권장:  git lfs track \"videos/*.mp4\"")
