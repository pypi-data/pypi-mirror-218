from setuptools import setup

setup(
    name='waterfly',
    version='10.7.2023',
    install_requires=[
        'googletrans>=3.1.0a0',
        'opencv-python',
        'rembg',
        'requests',
        'pyautogui'
    ],
    description='Waterfly is a powerful new AI tool to create Firefly URLs, process images, and draw on images.',
    long_description='''

Hi here!

Create URLs for images and text styles, for example:
create.image('Chocolate tree', ['hyper_realistic', 'cool_colors', 'studio_light'], 'portrait')
Create a great photo of a chocolate tree for your Instagram stories with very realistic graphics,
beautiful colors, and studio lighting.
Not interested in stories? Create something else! Example:
create.image('Sakura tree', ['cartoon', 'beautiful', 'pastel_colors', dramatic_light'], 'widescreen')
Creates a beautifully drawn picture of a sakura tree, in cartoon style, beautiful,
in pastel colors and with dramatic lighting,
with an aspect ratio that is ideal for desktop backgrounds

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Already have the image you need? Edit it!

The code that will remove the background:
edit.backdrop('image.img', 'backdrop.img')
You can add a vignette like this:
edit.vignette('image.img', level)
Turn the image into a cartoon:
edit.cartoon('image.img')

–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Want to point out something in an image?
Build any shape with lines and ellipses!

And much more...

''',
    author = 'Igor_Shapovalov_Andrejovich',
    packages = ['waterfly'],
    author_email = 'igor.shapovalov.andrejovich@gmail.com'
)