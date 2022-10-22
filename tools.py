import pandas as pd
import random
from PIL import Image,ImageDraw,ImageOps,ImageFont

def loadPeople()->pd.DataFrame:
    return pd.read_csv("data/people.csv")

def getPossibleBadAssingees(df:pd.DataFrame)->list:
    opt = list(df[df["badSeats"]<=0][["firstName","lastName"]].itertuples(index=False,name=None))
    return opt
    
def pickXRandom(l:list,x:int)->list:
    random.shuffle(l)
    return l[0:x]

def makeSeatBox(width:int,height:int,tuple,borderSize:int=2,textHeight:int=60)->Image.Image:
    fname,lname = tuple[0],tuple[1]
    canvas = ImageOps.expand(Image.new('RGB', (width-borderSize,height-borderSize), "lightgrey"),border=borderSize,fill='black')
    try:
        img = Image.open(f'data/photos/{lname} {fname}.jpg', 'r')
        w,h = img.size
        img = img.crop((0,0.15*h,w,0.75*h))
    except Exception as e:
        print(e)
        img = Image.open(f'data/photos/default.jpg', 'r')
    img.thumbnail((width-borderSize,height-borderSize-textHeight))
    draw = ImageDraw.Draw(canvas)  
    margin = int((width -img.size[1]-2*borderSize)/2)
    canvas.paste(img, (borderSize+margin,borderSize))
    font = ImageFont.truetype("arial.ttf", 27)
    message = fname
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((width-w)/2,img.size[1]+borderSize ), message, font=font, fill=(0,0,0))
    message = lname
    _, _, w, _ = draw.textbbox((0, 0), message, font=font)
    draw.text(((width-w)/2,img.size[1]+borderSize+h ), message, font=font, fill=(0,0,0))
    return canvas