import pandas as pd
import random
from PIL import Image, ImageDraw, ImageOps, ImageFont
from os.path import isfile

def loadPeople() -> pd.DataFrame:
    return pd.read_csv("data/people.csv")


def getPossibleBadAssingees(df: pd.DataFrame) -> list:
    return list(df[df["badSeats"] <= 0][["firstName", "lastName"]].itertuples(index=False, name=None))

def pickXRandom(l: list, x: int) -> list:
    random.shuffle(l)
    return l[0:x]

def makeSeatBox(width: int, height: int, tuple=[str,str], borderSize: int = 2, textHeight: int = 60,overwrite=False) -> Image.Image:
    fname, lname = tuple[0], tuple[1]
    if isfile(f"data/photos/{tuple[0]}-{tuple[1]}-{width}-{height}-{borderSize}-{textHeight}.png"):
        return Image.open(f"data/photos/{tuple[0]}-{tuple[1]}-{width}-{height}-{borderSize}-{textHeight}.png", "r")
    canvas = ImageOps.expand(
        Image.new("RGB", (width - borderSize, height - borderSize), "lightgrey"),
        border=borderSize,
        fill="black")
    try:
        img = Image.open(f"data/photos/{lname} {fname}.jpg", "r")
        w, h = img.size
        img = img.crop((0, 0.15 * h, w, 0.75 * h))
    except Exception as e:
        print(e)
        img = Image.open(f"data/photos/default.jpg", "r")

    img.thumbnail((width - borderSize, height - borderSize - textHeight))
    draw = ImageDraw.Draw(canvas)
    margin = int((width - img.size[0] - 2 * borderSize) / 2)
    canvas.paste(img, (borderSize + margin, borderSize))
    font = ImageFont.truetype("arial.ttf", 27)

    _, _, w, h = draw.textbbox((0, 0), fname, font=font)
    draw.text(((width - w) / 2, img.size[1] + borderSize), fname, font=font, fill=(0, 0, 0))

    _, _, w, _ = draw.textbbox((0, 0), lname, font=font)
    draw.text(((width - w) / 2, img.size[1] + borderSize + h),lname,font=font,fill=(0, 0, 0))
    canvas.save(f"data/photos/{tuple[0]}-{tuple[1]}-{width}-{height}-{borderSize}-{textHeight}.png")
    return canvas
