# pip install googletrans==3.1.0a0 #
from googletrans import Translator

# pip install opencv-python #
from cv2 import (
    imwrite,
    imread,
    filter2D,
    bitwise_not,
    bitwise_or,
    transform,
    bilateralFilter,
    cvtColor,
    stylization,
    convertScaleAbs,
    detailEnhance,
    pencilSketch,
    GaussianBlur,
    medianBlur,
    warpAffine,
    getRotationMatrix2D,
    getGaussianKernel,
    threshold,
    adaptiveThreshold,
    bilateralFilter,
    bitwise_and,
    line,
    ellipse,
    putText,
    findContours,
    drawContours,
    FONT_HERSHEY_SIMPLEX,
    inRange,
)

# pip install rembg --user #
from rembg import remove

# pip install requests #
from requests import get
from numpy import uint8, zeros, copy, array, float64, matrix, where
from math import cos, sin
import pyautogui
from os.path import getsize
from random import choice, randint, random


class create:
    def screenshot(image="screenshot.png"):
        imwrite(image, cvtColor(array(pyautogui.screenshot()), 4))

    def image(prompt, styles=["hyper_realistic"], ratio="square"):
        url = f"https://firefly.adobe.com/generate/images?prompt={Translator().translate(prompt).text.replace(' ', '+')}&"
        for style in styles:
            url += f"style={style}&"
        return f"{url}aspectRatio={ratio}&locale=en-en"

    def text(
        prompt,
        text="Firefly",
        font="acumin-pro-wide",
        background="transparent",
        fit="tight",
    ):
        return f"https://firefly.adobe.com/generate/font-styles?prompt={Translator().translate(prompt).text.replace(' ', '+')}&fitType={fit}&text={text}&font={font}&bgColor={background}&textColor=%23000000"


class edit:
    def cut(image, startwidth, endwidth, startheight, endheight):
        imwrite(image, imread(image)[startheight:endheight, startwidth:endwidth])

    def rotate(image, gradus=180):
        file = imread(image)
        imwrite(
            image,
            warpAffine(
                file,
                getRotationMatrix2D(
                    (file.shape[1] // 2, file.shape[0] // 2), gradus, 1
                ),
                (file.shape[1], file.shape[0]),
            ),
        )

    def blur(image, stage=0):
        imwrite(image, GaussianBlur(imread(image), (stage + 51, stage + 51), 0))

    def bright(image, stage=20):
        imwrite(image, convertScaleAbs(imread(image), beta=stage))

    def invert(image):
        imwrite(image, bitwise_not(imread(image)))

    def blackwhite(image):
        imwrite(image, cvtColor(imread(image), 6))

    def median(image, stage=5):
        imwrite(image, medianBlur(imread(image), stage))

    def bilateral(image):
        imwrite(image, bilateralFilter(imread(image), 9, 75, 75))

    def scratch(image, scale=127):
        imwrite(image, cvtColor(imread(image), 6))
        imwrite(image, threshold(imread(image), scale, 255, 0)[1])

    def cartoon(image):
        file = imread(image)
        imwrite(
            image,
            bitwise_and(
                bilateralFilter(file, 9, 250, 250),
                file,
                mask=adaptiveThreshold(cvtColor(file, 6), 255, 0, 0, 9, 9),
            ),
        )

    def paint(image):
        imwrite(
            image,
            filter2D(
                imread(image),
                ddepth=-1,
                kernel=array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]),
            ),
        )

    def paint2(image):
        imwrite(
            image,
            stylization(
                GaussianBlur(imread(image), (5, 5), 0, 0), sigma_s=40, sigma_r=0.1
            ),
        )

    def hd(image):
        imwrite(image, detailEnhance(imread(image), sigma_s=12, sigma_r=0.15))

    def pencil(image):
        imwrite(
            image,
            pencilSketch(imread(image), sigma_s=60, sigma_r=0.07, shade_factor=0.1)[1],
        )

    def vignette(image, level=3):
        file = imread(image)
        kernel = (
            getGaussianKernel(file.shape[0], file.shape[0] / level)
            * getGaussianKernel(file.shape[1], file.shape[1] / level).T
        )
        mask = kernel / kernel.max()
        image_vignette = copy(file)
        for i in range(3):
            image_vignette[:, :, i] = image_vignette[:, :, i] * mask
        imwrite(image, image_vignette)

    def embossed(image):
        imwrite(
            image,
            filter2D(
                imread(image), -1, kernel=array([[0, -3, -3], [3, 0, -3], [3, 3, 0]])
            ),
        )

    def sepia(image):
        sepia = transform(
            array(imread(image), dtype=float64),
            matrix(
                [[0.272, 0.543, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]
            ),
        )
        sepia[where(sepia > 255)] = 255
        imwrite(image, array(sepia, dtype=uint8))

    def outline(image, level=200):
        file = imread(image)
        img_grey = cvtColor(file, 6)
        ret, thresh_img = threshold(img_grey, level, 255, 0)
        contours, hierarchy = findContours(thresh_img, 3, 2)
        img_contours = uint8(zeros((file.shape[0], file.shape[1])))
        drawContours(img_contours, contours, -1, (255, 255, 255), 1)
        imwrite(image, drawContours(img_contours, contours, -1, (255, 255, 255), 1))

    def splash(image, lower=20, upper=32):
        img = imread(image)
        res = zeros(img.shape, uint8)
        mask = inRange(
            cvtColor(img, 40),
            array([lower, 128, 128]),
            array([upper, 255, 255]),
        )
        for i in range(3):
            res[:, :, i] = bitwise_and(
                cvtColor(img, 6), cvtColor(img, 6), mask=bitwise_not(mask)
            )
        imwrite(image, bitwise_or(bitwise_and(img, img, mask=mask), res))

    def backdrop(image, output):
        with open(image, "rb") as i:
            with open(output, "wb") as o:
                o.write(remove(i.read()))


class draw:
    def text(image, text, position, size=4, color=(150, 120, 255), thickness=6):
        imwrite(
            image,
            putText(
                imread(image),
                text,
                position,
                FONT_HERSHEY_SIMPLEX,
                size,
                color,
                thickness,
            ),
        )

    def point(image, position, color=(150, 120, 255), thickness=6):
        imwrite(image, line(imread(image), position, position, color, thickness))

    def line(image, start, end, color=(150, 120, 255), thickness=6):
        imwrite(image, line(imread(image), start, end, color, thickness))

    def angle(
        image,
        center,
        firstradius,
        secondradius,
        degree=0,
        inclination=90,
        color=(150, 120, 255),
        thickness=3,
    ):
        file = imread(image)
        angle_radians = degree * 0.017453292519943295
        inclination_radians = inclination * 0.017453292519943295
        point1 = int(center[0] + firstradius * cos(angle_radians)), int(
            center[1] - firstradius * sin(angle_radians)
        )
        point2 = int(
            center[0] + secondradius * cos(angle_radians + inclination_radians)
        ), int(center[1] - secondradius * sin(angle_radians + inclination_radians))
        line(file, center, point1, color, thickness)
        line(file, center, point2, color, thickness)
        imwrite(image, file)

    def triangle(
        image,
        firstpoint,
        secondpoint,
        thirdpoint,
        degree=0,
        color=(150, 120, 255),
        thickness=3,
    ):
        file = imread(image)
        angle_radians = degree * 0.017453292519943295
        rotated_firstpoint = (
            int(
                firstpoint[0] * cos(angle_radians) - firstpoint[1] * sin(angle_radians)
            ),
            int(
                firstpoint[0] * sin(angle_radians) + firstpoint[1] * cos(angle_radians)
            ),
        )
        rotated_secondpoint = (
            int(
                secondpoint[0] * cos(angle_radians)
                - secondpoint[1] * sin(angle_radians)
            ),
            int(
                secondpoint[0] * sin(angle_radians)
                + secondpoint[1] * cos(angle_radians)
            ),
        )
        rotated_thirdpoint = (
            int(
                thirdpoint[0] * cos(angle_radians) - thirdpoint[1] * sin(angle_radians)
            ),
            int(
                thirdpoint[0] * sin(angle_radians) + thirdpoint[1] * cos(angle_radians)
            ),
        )
        line(file, rotated_firstpoint, rotated_secondpoint, color, thickness)
        line(file, rotated_secondpoint, rotated_thirdpoint, color, thickness)
        line(file, rotated_thirdpoint, rotated_firstpoint, color, thickness)
        imwrite(image, file)

    """
    def quadrangle(): pass
    def pentagon(): pass
    def hexagon(): pass
    def heptagon(): pass
    def octagon(): pass
    """

    def ellipse(
        image,
        center,
        axes=(100, 60),
        degree=0,
        startAngle=0,
        endAngle=360,
        color=(150, 120, 255),
        thickness=3,
    ):
        imwrite(
            image,
            ellipse(
                imread(image),
                center,
                axes,
                degree,
                startAngle,
                endAngle,
                color,
                thickness,
            ),
        )

    def circle(
        image,
        center,
        radius=20,
        startAngle=0,
        endAngle=360,
        color=(150, 120, 255),
        thickness=3,
    ):
        imwrite(
            image,
            ellipse(
                imread(image),
                center,
                (radius, radius),
                0,
                startAngle,
                endAngle,
                color,
                thickness,
            ),
        )


class random:
    def image(search=""):
        with open("image.jpg", "wb") as file:
            file.write(get(f"https://source.unsplash.com/random?{search}").content)

    class color:
        def name(dest="en"):
            if dest.startswith("en"):
                return choice(info.colors)
            return Translator().translate(choice(info.colors), src="en", dest=dest).text

        def rgb():
            return randint(0, 255), randint(0, 255), randint(0, 255)

        def rgba():
            return randint(0, 255), randint(0, 255), randint(0, 255), random()

        def cmyk():
            return randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100)

        def hex():
            return "#" + hex(randint(0, 16777215))[2:].upper()


class info:
    measures_compare_with_byte = {
        "microbit": 0.000001,
        "milibit": 0.001,
        "base": 0.0625,
        "bit": 0.125,
        "nibble": 0.5,
        "byte": 1,
        "octet": 1,
        "kilobyte": 1024,
        "megabyte": 1048576,
        "gigabyte": 1073741824,
        "terabyte": 1099511627776,
        "petabyte": 1125899906842624,
        "exabyte": 1152921504606846976,
    }
    colors = [
        "absolute zero",
        "acid green",
        "aero",
        "african violet",
        "air superiority blue",
        "alice blue",
        "alizarin",
        "alloy orange",
        "almond",
        "amaranth deep purple",
        "amaranth pink",
        "amaranth purple",
        "amazon",
        "amber",
        "amethyst",
        "android green",
        "antique brass",
        "antique bronze",
        "antique fuchsia",
        "antique ruby",
        "antique white",
        "apricot",
        "apple",
        "apricot",
        "aqua",
        "aquamarine",
        "arctic lime",
        "artichoke green",
        "arylide yellow",
        "ash grey",
        "atomic tangerine",
        "aureolin",
        "army green",
        "azure",
        "baby blue",
        "baby blue eyes",
        "baby pink",
        "baby powder",
        "baker-miler pink",
        "banana mania",
        "barn red",
        "battleship grey",
        "beau blue",
        "beaver",
        "beige",
        "b'dazzled blue",
        "big dip o'ruby",
        "bisque",
        "bistre",
        "bistre brown",
        "bitter lemon",
        "black",
        "black bean",
        "black coral",
        "black olive",
        "black shadows" "blanched almond",
        "blast-off bronze",
        "bleu de France",
        "blizzard blue",
        "blood red",
        "blue",
        "blue (crayola)",
        "blue (munsell)",
        "blue (NCS)",
        "blue (pantone)",
        "blue (pigment)",
        "blue bell",
        "blue-gray (crayola)",
        "blue jeans",
        "blue sapphire",
        "blue-violet",
        "blue yonder",
        "bluetiful",
        "blush",
        "bole",
        "bone",
        "brick red",
        "bright lilac",
        "bright yellow (crayola)",
        "bronze",
        "brown",
        "brown suggar",
        "bud green",
        "buff",
        "burgundy",
        "burlywood",
        "burnished brown",
        "burnt orange",
        "burnt sienna",
        "burnt umber",
        "byzantine",
        "buzantium" "cadet blue",
        "cadet grey",
        "cadmium green",
        "cadmium orange",
        "café au lait",
        "café noir",
        "cambridge blue",
        "camel",
        "cameo pink",
        "canary",
        "canary yellow",
        "candy pink",
        "cardinal",
        "caribbean green",
        "carmine",
        "carnation pink",
        "carnelian",
        "carolina blue",
        "carrot orange",
        "catawba",
        "cedar chest",
        "celadon",
        "celeste",
        "cerise",
        "cerulean",
        "cerulean blue",
        "cerulean frost",
        "cerulean (crayola)",
        "champagne",
        "champagne pink",
        "charcoal",
        "charm pink",
        "chartreuse",
        "chartreuse (web)",
        "cherry blossom pink",
        "chestnut",
        "chili red",
        "china pink",
        "chinese red",
        "chinese violet",
        "chinese yellow",
        "chocolate (traditional)",
        "chocolate (web)",
        "cinereous",
        "cinnabar",
        "cinnamon satin",
        "citrine",
        "citron",
        "claret",
        "coffee",
        "columbia blue",
        "congo pink",
        "cool gray",
        "copper",
        "copper (crayola)",
        "copper penny",
        "copper red",
        "copper rose",
        "coquelicot",
        "coral",
        "coral pink",
        "cordovian",
        "corn",
        "cornflower blue",
        "cornsilk",
        "cosmic cobalt",
        "cosmic latte",
        "coyote brown",
        "cotton candy",
        "cream",
        "crimson",
        "crimson (UA)",
        "cultured pearl",
        "cyan",
        "cyan (process)",
        "cyber grape",
        "cyber yellow",
        "cyclamen",
        "dark brown",
        "dark byzantium",
        "dark blue",
        "dark cyan",
        "dark electric blue",
        "dark goldenrod",
        "darkgreen (x11)",
        "darkgreen",
        "darkgrey",
        "dark jungle green",
        "dark khaki",
        "dark lava",
        "dark liver (horses)",
        "dark magenta",
        "dark olive green",
        "dark orange",
        "dark orchid",
        "dark purple",
        "dark red",
        "dark salmon",
        "dark sea green",
        "dark sienna",
        "dark sky blue",
        "dark slate blue",
        "dark slate gray",
        "dark spring green",
        "dark turquoise",
        "dark violet",
        "davy's grey",
        "deep cerise",
        "deep champagne",
        "deep chestnut",
        "deep jungle green",
        "deep pink",
        "deep saffron",
        "deep sky blue",
        "deep space sparkle",
        "deep taupe",
        "denim",
        "denim blue",
        "desert",
        "desert sand",
        "dim gray",
        "dodger blue",
        "drab dark brown",
        "duke blue",
        "dutch white",
        "ebony",
        "ecru",
        "eerie black",
        "eggplant",
        "eggshell",
        "electric lime",
        "electric purple",
        "electric violet",
        "emerald",
        "eminence",
        "english lavender",
        "english red",
        "english vermilion",
        "english violet",
        "erin",
        "eton blue",
        "fallow",
        "falu red",
        "fandango",
        "fandango pink",
        "fawn",
        "fern green",
        "field drab",
        "fiery rose",
        "finn",
        "firebrick",
        "fire engine red",
        "flame",
        "flax",
        "flirt",
        "floral white",
        "forest green",
        "french beige",
        "french bistre",
        "french blue",
        "french fuchsia",
        "french lilac",
        "french lime",
        "french mauve",
        "french pink",
        "french raspberry",
        "french sky blue",
        "french violet",
        "frostbite",
        "fuchsia",
        "fuchsia (crayola)",
        "fulvous",
        "fuzzy wuzzy",
        "gainsboro",
        "gamboge",
        "generic viridan",
        "ghost white",
        "glaucous",
        "glossy grape",
        "go green",
        "gold (metallic)",
        "gold (crayola)",
        "gold fusion",
        "golden",
        "golden brown",
        "golden poppy",
        "golden yellow",
        "goldenrod",
        "gotham green",
        "granite gray",
        "granny smith apple",
        "grey (web)",
        "grey (X11)",
        "green",
        "green (crayola)",
        "green (web)",
        "green (munsell)",
        "green (NCS)",
        "green (pantone)",
        "green (pigment)",
        "green-blue",
        "green-yellow",
        "green lizard",
        "green sheen",
        "gunmetal",
        "hansa yellow",
        "harlequin",
        "harvest gold",
        "heat wave",
        "heliotrope",
        "heliotrope gray",
        "hollywood cerise",
        "honolulu blue",
        "hooker's green",
        "hot magenta",
        "hot pink",
        "hunter green",
        "honeydew",
        "iceberg",
        "illuminating emerald",
        "imperial red",
        "inchworm",
        "independence",
        "india green",
        "indian red",
        "indian yellow",
        "indigo",
        "indigo dye",
        "international klein blue",
        "international orange (engineering)",
        "international orange (golden gate bridge)",
        "irresistible",
        "isabelline",
        "italian sky blue",
        "indianred",
        "indigo",
        "ivory",
        "japanese carmine",
        "japanese violet",
        "jasmine",
        "jazzberry jam",
        "jet",
        "jonquil",
        "june bud",
        "jungle green",
        "kelly green",
        "keppel",
        "key lime",
        "khaki",
        "kobe",
        "kobi",
        "kobicha",
        "KSU purple" "languid lavender",
        "lapis lazuli",
        "laser lemon",
        "laurel green",
        "lava",
        "lavender (floral)",
        "lavender (web)",
        "lavender blue",
        "lavender blush",
        "lavender gray",
        "lawn green",
        "lemon",
        "lemon chiffon",
        "lemon curry",
        "lemon glacier",
        "lemon meringue",
        "lemon yellow",
        "lemon yellow (crayola)",
        "liberty",
        "light blue",
        "light coral",
        "light cornflower blue",
        "light cyan",
        "light french beige",
        "light goldenrod yellow",
        "light gray",
        "light green",
        "light orange",
        "light periwinkle",
        "light khaki",
        "light pink",
        "light salmon",
        "light sea green",
        "light sky blue",
        "light slate gray",
        "light steel blue",
        "light yellow",
        "lilac",
        "lilac luster",
        "lime (color whell)",
        "lime x11 (web)",
        "lime green",
        "lincoln green",
        "linen",
        "lion",
        "liseran purple",
        "little boy blue",
        "liver",
        "liver (dogs)",
        "liver (organ)",
        "liver chestnut",
        "livid",
        "macaroni and cheese",
        "madder lake",
        "magenta",
        "magenta (crayola)",
        "magenta (dye)",
        "magenta (pantone)",
        "magenta (process)",
        "magenta haze",
        "magic mit",
        "magnolia",
        "mahogany",
        "maize",
        "maize (crayola)",
        "majorelle blue",
        "malachite",
        "manatee",
        "mandarin",
        "mango",
        "mango tango",
        "mantis",
        "mardi gras",
        "marigold",
        "maroon (crayola)",
        "maroon (web)",
        "maroon x11",
        "mauve",
        "mauve taupe",
        "mauvelous",
        "maximum blue",
        "maximum blue green",
        "maximum blue purple",
        "maximum green",
        "maximum green yellow",
        "maximum purple",
        "maximum red",
        "maximum red purple",
        "maximum yellow",
        "maximum yelow red",
        "may green",
        "maya blue",
        "medium aquamarine",
        "medium blue",
        "medium candy apple red",
        "medium carmine",
        "medium champagne",
        "medium orchid",
        "medium purple",
        "medium sea green",
        "medium slate blue",
        "medium spring green",
        "medium turquoise",
        "medium violet-red",
        "mellow apricot",
        "mellow yellow",
        "melon",
        "metallic gold",
        "metallic seaweed",
        "metallic sunburst",
        "mexican pink",
        "middle blue",
        "middle blue green",
        "middle blue purple",
        "middle grey",
        "middle green",
        "middle green yellow",
        "middle purple",
        "middle red",
        "middle red purple",
        "middle yellow",
        "middle yellow red",
        "midnight" "midnight blue",
        "midnight green (eagle green)",
        "mikado yellow",
        "mimi pink",
        "mindaro",
        "ming",
        "minion yellow",
        "mint",
        "mint cream",
        "mint green",
        "mistry moss",
        "misty rose",
        "moccasin",
        "mode beige",
        "mona lisa",
        "morning blue",
        "moss green",
        "mountain meadow",
        "mountbatten pink",
        "MSU green",
        "mulberry",
        "mulberry (crayola)",
        "mustrad",
        "myrtle green",
        "mystic",
        "mystic maroon",
        "nadeshiko pink",
        "naples yellow",
        "navajo white",
        "navy blue",
        "navy blue (Crayola)",
        "neon blue",
        "neon green",
        "neon fuchisia",
        "new york pink",
        "nikel",
        "non-photo blue",
        "nyanza",
        "ochre",
        "old burgundy",
        "old gold",
        "old lace",
        "old lavender",
        "old mauve",
        "old rose",
        "old silver",
        "olive",
        "olive drab #3",
        "olive drab #7",
        "olive green",
        "olivine",
        "onyx",
        "opal",
        "opera mauve",
        "orange",
        "orange (crayola)",
        "orange (Pantone)",
        "orange (web)",
        "orange peel",
        "orange-red",
        "orange-red (Crayola)",
        "orange soda",
        "orange-yellow",
        "orange-yellow (crayola)",
        "orchid",
        "orchid pink",
        "orchid (crayola)",
        "outer space (crayola)",
        "outrageous orange",
        "oxblood",
        "oxford blue",
        "ou crimson red",
        "pacific blue",
        "pakistan green",
        "palatinate purple",
        "pale aqua",
        "pale cerulean",
        "pale dogwood",
        "pale pink",
        "pale purple (pantone)",
        "pale spring bud",
        "pansy purple",
        "paolo veronese green",
        "papaya whip",
        "paradise pink",
        "parchment",
        "paris green",
        "pastel pink",
        "patriarch",
        "paua",
        "payne's grey",
        "peach",
        "peach (crayola)",
        "peach puff",
        "pear",
        "pearly purple",
        "periwinkle",
        "periwinkle (crayola)",
        "permanent geranium lake",
        "persian blue",
        "persian green",
        "persian indigo",
        "persian orange",
        "persian pink",
        "persian plum",
        "persian red",
        "persian rose",
        "persimmon",
        "pewter blue",
        "phlox",
        "phthalo blue",
        "phthalo green",
        "picotee blue",
        "pictorial carmine",
        "piggy pink",
        "pine green",
        "pine tree",
        "pink",
        "pink (pantone)",
        "pink lace",
        "pink lavender",
        "pink sherbet",
        "pistachio",
        "platinum",
        "plum",
        "plum (web)",
        "plump purple",
        "polished pine",
        "pomp and power",
        "popstar",
        "portland orange",
        "powder blue",
        "princeton orange",
        "process yellow",
        "prune",
        "prussian blue",
        "psychedelic purple",
        "puce",
        "pullman brown",
        "pumpkin",
        "purple",
        "purple (web)",
        "purple (munsell)",
        "purple x11",
        "purple mountain majesty",
        "purple navy",
        "purple pizzazz",
        "purple plum",
        "purpureus",
        "queen blue",
        "queen pink",
        "quick silver",
        "quinacridone magenta" "radical red",
        "raisin black",
        "rajan",
        "raspberry",
        "raspberry glacé",
        "raspberry rose",
        "raw sienna",
        "raw umber",
        "razzle dazzle rose",
        "razzmatazz",
        "razzmic berry",
        "rebecca purple",
        "red",
        "red (crayola)",
        "red (munsell)",
        "red (ncs)",
        "red pantone",
        "red (pigment)",
        "red (ryb)",
        "red-orange",
        "red-orange (crayola)",
        "red-orange (color wheel)",
        "red-purple",
        "red salsa",
        "red-violet",
        "red-violet (crayola)",
        "red-violet (color wheel)",
        "redwood",
        "redolution blue",
        "rhythm",
        "rich black",
        "rhich black (fogra 29)",
        "rich black (fogra 39)",
        "rifle green",
        "robin egg blue",
        "rocket metallic",
        "rojo spanish red",
        "roman silver",
        "rose",
        "rose bondon",
        "rose dust",
        "rose ebony",
        "rose madder",
        "rose pink",
        "rose pompadour",
        "rose red",
        "rose taupe",
        "rose vale",
        "rosewood",
        "rosso corsa",
        "rosy brown",
        "royal blue (dark)",
        "royal blue (light)",
        "royal purple",
        "royal yellow",
        "ruber",
        "rubine red",
        "ruby",
        "ruby red",
        "rufous",
        "russet",
        "russian green",
        "russian violet",
        "rust",
        "rustly red",
        "saddlebrown",
        "salmon",
        "sandybrown",
        "seagreen",
        "seashell",
        "sienna",
        "silver",
        "skyblue",
        "slateblue",
        "slategray",
        "slategrey",
        "snow",
        "springgreen",
        "steelblue",
        "tan",
        "teal",
        "thistle",
        "tomato",
        "turquoise",
        "violet",
        "wheat",
        "white",
        "whitesmoke",
        "xanadu",
        "xantihic",
        "xanthous" "yellow",
        "yellowgreen",
        "zaffre",
        "zebra",
        "zomp",
    ]

    class image:
        def name(image):
            return image.replace("\\", "/").split("/")[-1]

        def format(image):
            return image.split(".")[-1].upper()

        def size(image):
            file = imread(image)
            return {
                "height": file.shape[1],
                "width": file.shape[0],
                "channels": file.shape[2],
                "pixels": file.size,
            }

        def weight(image, measure="kilobyte"):
            return getsize(image) / info.measures_compare_with_byte[measure]

    class screen:
        def weight():
            return pyautogui.size()

        def on_screen(x, y):
            return pyautogui.onScreen(x, y)
