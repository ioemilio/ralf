# encoding: utf-8

import math
import os, os.path, shutil
import random
import sys

sys.path.insert(0, "./lib")
from PIL import Image
from colors import colorsys, webcolors
from workflow import Workflow


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


MAX_RESULTS = 500  # just a limit for alfred results


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def ball(wf):
    BA = ["It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."]
    ba = random.choice(BA)
    wf.add_item(
        title=ba,
        icon="./resources/icon/ball.png",
        arg=ba,
        valid=True)

    wf.send_feedback()  # Send the results to Alfred as XML


def colr(wf):
    def colorDistance(r1, g1, b1, r2, g2, b2):
        rmean = (r1 + r2) / 2
        r, g, b = (r1 - r2), (g1 - g2), (b1 - b2),
        return math.sqrt((((512+rmean)*r*r)>>8) + 4*g*g + (((767-rmean)*b*b)>>8))

    def closestColor(r, g, b):
        minColors = {}
        for key, name in webcolors.css3_hex_to_names.items():
            cr, cg, cb = webcolors.hex_to_rgb(key)
            # https://www.compuphase.com/cmetric.htm
            dist = colorDistance(r, g, b, cr, cg, cb)
            minColors[dist] = name
        return minColors[min(minColors.keys())]

    def getColorName(r, g, b):
        try:
            colorName = webcolors.rgb_to_name((r, g, b))
        except ValueError:
            colorName = closestColor(r, g, b)
        return colorName.capitalize()

    def generateIcon(r, g, b):
        iconPath = "./resources/colr/r{}-g{}-b{}.png".format(r, g, b)
        if os.path.exists("./resources/colr"):
            shutil.rmtree("./resources/colr")
        os.mkdir("./resources/colr")
        im = Image.new("RGB", (64, 64))
        im.putdata([(r, g, b)] * (64*64))
        im.save(iconPath)

        return iconPath

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    iconPath = generateIcon(r, g, b)

    colorName = getColorName(r, g, b)
    hexc = ("#%02x%02x%02x" % (r, g, b)).upper()
    rgbc = "rgb({}, {}, {})".format(r, g, b)
    c,m,y,k = colorsys.rgb_to_cmyk(r, g, b)
    cmykc = "cmyk({}, {}, {}, {})".format(int(c), int(m), int(y), int(k))
    r /= 255.0
    g /= 255.0
    b /= 255.0
    h,s,l = colorsys.rgb_to_hls(r, g, b)
    hslc = "hsl({}, {}, {})".format(int(h*360), int(s*100), int(l*100))
    h,s,v = colorsys.rgb_to_hsv(r, g, b)
    hsvc = "hsv({}, {}, {})".format(int(h*360), int(s*100), int(v*100))

    wf.add_item(
        title=colorName,
        subtitle="Color name",
        arg=colorName,
        icon=iconPath,
        valid=True)
    wf.add_item(
        title=hexc,
        subtitle="HEX",
        arg=hexc,
        icon=iconPath,
        valid=True)
    wf.add_item(
        title=rgbc,
        subtitle="RGB",
        arg=rgbc,
        icon=iconPath,
        valid=True)
    wf.add_item(
        title=hslc,
        subtitle="HSL",
        arg=hslc,
        icon=iconPath,
        valid=True)
    wf.add_item(
        title=hsvc,
        subtitle="HSV",
        arg=hsvc,
        icon=iconPath,
        valid=True)
    wf.add_item(
        title=cmykc,
        subtitle="CMYK",
        arg=cmykc,
        icon=iconPath,
        valid=True)

    wf.send_feedback()  # Send the results to Alfred as XML


def draw(wf):
    deck = []
    S = ["Hearts", "Diamonds", "Clubs", "Spades"]
    for s in S:
        for v in range(1, 13+1):
            if v == 1:
                deck.append("{} of {}".format("A", s))
            elif v <= 10:
                deck.append("{} of {}".format(v, s))
            elif v == 11:
                deck.append("{} of {}".format("J", s))
            elif v == 12:
                deck.append("{} of {}".format("Q", s))
            else:  # v == 13
                deck.append("{} of {}".format("K", s))

    try:
        arg = " ".join(sys.argv[1].split(" ")[1:])
        n = max(1, min(int(arg), 52))
        CD = random.sample(deck, n)
        for i, cd in enumerate(CD):
            shortName = cd.split(" of ")[0]+cd.split(" of ")[1][0]
            wf.add_item(
                title=cd,
                subtitle="Card {}".format(i+1),
                arg=cd,
                icon="./resources/draw/{}.png".format(shortName),
                valid=True)
        cd = ", ".join([f.split(" of ")[0]+f.split(" of ")[1][0] for f in CD])
        wf.add_item(
            title=cd,
            subtitle="All Cards",
            arg=cd,
            icon="./resources/icon/draw.png",
            valid=True)
    except:
        cd = random.choice(deck)
        shortName = cd.split(" of ")[0]+cd.split(" of ")[1][0]
        wf.add_item(
            title=cd,
            subtitle="Card",
            arg=cd,
            icon="./resources/draw/{}.png".format(shortName),
            valid=True)

    wf.send_feedback()  # Send the results to Alfred as XML


def flip(wf):
    try:
        arg = " ".join(sys.argv[1].split(" ")[1:])
        n = max(1, min(int(arg), MAX_RESULTS))
        CF = []
        for i in range(1, n+1):
            cf = "Heads" if random.random() < 0.5 else "Tails"
            CF.append(cf)
            wf.add_item(
                title=cf,
                subtitle="Flip {}".format(i),
                icon="./resources/flip/{}.png".format(cf[0]),
                arg=cf,
                valid=True)
        cf = ", ".join([f[0] for f in CF])
        wf.add_item(
            title=cf,
            subtitle="All flips",
            icon="./resources/icon/flip.png",
            arg=cf,
            valid=True)
    except:
        cf = "Heads" if random.random() < 0.5 else "Tails"
        wf.add_item(
            title=cf,
            subtitle="Flip",
            icon="./resources/flip/{}.png".format(cf[0]),
            arg=cf,
            valid=True)

    wf.send_feedback()  # Send the results to Alfred as XML


def pick(wf):
    arg = " ".join(sys.argv[1].split(" ")[1:])
    n = arg.split(",")
    rp = random.choice(n)
    wf.add_item(
        title=rp,
        subtitle="Pick",
        icon="./resources/icon/pick.png",
        arg=rp,
        valid=True)

    wf.send_feedback()  # Send the results to Alfred as XML


def rand(wf):
    try:
        arg = " ".join(sys.argv[1].split(" ")[1:])
        if arg.isdigit():
            n = abs(int(arg))
            rn = str(random.randint(1, n))
            wf.add_item(
                title=rn,
                subtitle="Random integer in [{}, {}]".format(1, n),
                icon="./resources/icon/rand.png",
                arg=rn,
                valid=True)
        else:
            a, b = arg.split("..")
            a = int(a.strip())
            b = int(b.strip())
            # if a > b:
            #     raise Exception()
            rn = str(random.randint(a, b))
            wf.add_item(
                title=rn,
                subtitle="Random integer in [{}, {}]".format(a, b),
                icon="./resources/icon/rand.png",
                arg=rn,
                valid=True)
    except:
        rn = str(random.random())
        wf.add_item(
            title=rn,
            subtitle="Random in [{},{}[".format(0, 1),
            icon="./resources/icon/rand.png",
            arg=rn,
            valid=True)

    wf.send_feedback()  # Send the results to Alfred as XML


def roll(wf):
    try:
        DR = []
        arg = " ".join(sys.argv[1].split(" ")[1:])
        if arg.isdigit():
            n = max(1, min(int(arg), MAX_RESULTS))
            d = 6
        else:
            n, d = arg.lower().split("d")
            if n.strip() == "":
                n = 1
            else:
                n = max(1, min(int(n.strip()), MAX_RESULTS))
            d = max(1, int(d.strip()))

        for i in range(1, n+1):
            dr = random.randint(1, d)
            if d <= 6:
                icon = "./resources/roll/{}.png".format(dr)
            else:
                icon = "./resources/icon/roll.png"
            dr = str(dr)
            DR.append(dr)
            wf.add_item(
                title=dr,
                subtitle="D{} Roll {}".format(d, i),
                icon=icon,
                arg=dr,
                valid=True)
        dr = ", ".join(DR)
        wf.add_item(
            title=dr,
            subtitle="All D{} Rolls".format(d),
            icon="./resources/icon/roll.png",
            arg=dr,
            valid=True)
    except:
        dr = str(random.randint(1, 6))
        wf.add_item(
            title=dr,
            subtitle="D6 Roll",
            icon="./resources/roll/{}.png".format(dr),
            arg=dr,
            valid=True)

    wf.send_feedback()  # Send the results to Alfred as XML


def tell(wf):
    t = "YES" if random.random() < 0.5 else "NO"
    wf.add_item(
        title=t,
        icon="./resources/icon/tell.png",
        arg=t,
        valid=True)

    wf.send_feedback()  # Send the results to Alfred as XML


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    wf = Workflow()

    func = ["ball", "colr", "draw", "flip", "pick", "rand", "roll", "tell"]
    sub = {
        "ball": "Ask the Magic 8-Ball! `ball`",
        "colr": "See a Random Color! `colr`",
        "draw": "Draw a Card! `draw n`",
        "flip": "Flip a coin! Heads or Tails? `flip n`",
        "pick": "Just Pick One! `pick a,b,c`",
        "rand": "Generate a Random Number! `rand a..b`",
        "roll": "Roll a Dice! `roll nDk`",
        "tell": "Tell me! Yes or No? `tell`"
    }

    for f in func:
        if arg in f:
            wf.add_item(
                title=f,
                subtitle=sub[f],
                autocomplete="{} ".format(f),
                icon="resources/icon/{}.png".format(f),
                valid=False)
        elif f in arg:
            sys.exit(wf.run(locals()[f]))

    wf.send_feedback()  # Send the results to Alfred as XML
