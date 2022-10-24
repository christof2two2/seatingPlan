from helperFunctions import loadPeople, getPossibleBadAssingees, pickXRandom, makeSeatBox
import random
from PIL import Image


def assignSeats() -> list:
    # [ShitSeats]*14 + [column1 remainder]*4 + [column2 remainder]*3 +[column3 remainder]*3 + [column 4 remainder]*4 + [row1]*11 + [row3]*14 + [row2]*13
    #       0-14        14-18               18-21                       21-24                   24-28                 +28-39      +39-53      53-66
    seats = [None]*66
    df = loadPeople()

    l = getPossibleBadAssingees(df)  # get people who have not yet been on a bad set and are thus elligble
    badSeatsPeople = pickXRandom(l, 14)  # pick 14 people from this list randomly
    seats[0:14] = badSeatsPeople  # assign them bad seats

    fnames, lnames = [i[0] for i in badSeatsPeople], [i[1] for i in badSeatsPeople]
    remaining = df[~((df["firstName"].isin(fnames)) & (df["lastName"].isin(lnames)))]  # get all not yet assigned people

    # assign everybody not yet assigned a random seat
    remaining = list(remaining[["firstName", "lastName"]].itertuples(index=False, name=None))
    random.shuffle(remaining)
    seats[12:] = remaining

    # check if maxine is on row 2
    index = [x for x, y in enumerate(seats[53:]) if y[0] == "Maxine"]
    if len(index) > 0:  # if maxine is on row 2
        index = index[0] + 53
        randomSeat = random.randint(14, 53 - 1)  # pick a random seat that is not on row 2 and is not a bad seat to swap with
        print(f"Maxine is on row 2 -> swapping Maxine with {seats[randomSeat]}")
        seats[randomSeat], seats[index] = seats[index], seats[randomSeat]  # swap them

    # split list up into smaller lists representing the rows of tables
    # to make rendering easier.
    col1 = seats[0:3] + seats[14:18] +[seats[12]]
    col2 = seats[3:6] + seats[18:21]
    col3 = seats[6:9] + seats[21:24]
    col4 = seats[9:12] + seats[24:28] +[seats[13]]
    row1 = seats[28:39]
    row2 = seats[53:]
    row3 = seats[39:53]
    return [col1, col2, col3, col4, row1, row2, row3]


def render(seats: list) -> None:
    boxWidth = 215
    boxHeight = 215
    canvasWidth = 3508
    canvasHeight = 2480
    marginWidth = 25
    marginHeight = 25
    canvas = Image.new("RGB", (canvasWidth, canvasHeight), "white")

    # col1
    for i, item in enumerate(seats[0]):
        img = makeSeatBox(boxWidth, boxHeight, item)
        canvas.paste(img, (marginWidth, canvasHeight - marginHeight - (i + 1) * boxHeight))

    # col2
    for i, item in enumerate(seats[1]):
        img = makeSeatBox(boxWidth, boxHeight, item)
        canvas.paste(img,(2 * marginWidth + boxWidth,canvasHeight - marginHeight - (i + 1) * boxHeight,))

    # col3
    for i, item in enumerate(seats[2]):
        img = makeSeatBox(boxWidth, boxHeight, item)
        canvas.paste(img,(canvasWidth - 2 * marginWidth - 2 * boxWidth,canvasHeight - marginHeight - (i + 1) * boxHeight,))
    # col4
    for i, item in enumerate(seats[3]):
        img = makeSeatBox(boxWidth, boxHeight, item)
        canvas.paste(img,(canvasWidth - marginWidth - boxWidth,canvasHeight - marginHeight - (i + 1) * boxHeight,))
    # row1
    for i, item in enumerate(seats[4]):
        img = makeSeatBox(boxWidth, boxHeight, item)
        canvas.paste(img,(3 * marginWidth + 2 * boxWidth + i * boxWidth,canvasHeight - 9 * boxHeight - marginHeight,))

    # row2
    for i, item in enumerate(seats[5]):
        img = makeSeatBox(boxWidth, boxHeight, item)
        canvas.paste(img,(3 * marginWidth + 2 * boxWidth + i * boxWidth,canvasHeight - 10 * boxHeight - 2 * marginHeight,))

    # row3
    for i, item in enumerate(seats[6]):
        img = makeSeatBox(boxWidth, boxHeight, item)
        canvas.paste(img,(3 * marginWidth + boxWidth + i * boxWidth,canvasHeight - 11 * boxHeight - 3 * marginHeight,))

    canvas.save("seatingPlan.png")
    canvas.save("seatingPlan.pdf")
    canvas.show()


if __name__ == "__main__":
    seats = assignSeats()
    render(seats)
