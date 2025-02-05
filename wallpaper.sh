# Dimensions
magick identify a.jpg

# Resize
magick a.jpg -resize 1920x1080\> a2.jpg
magick a.jpg -gravity southeast -extent 1920x1080+200 a2.png
magick b.png -resize 50% b2.png

# Shift hue
magick a2.jpg -modulate 100,100,50 a3.png # 50% = 200%; 0% = 300%

# Compose
magick a2.jpg b2.jpg +append -quality 100 result.jpg

# Blur & Overlay
magick result.jpg -blur 0x10 -evaluate Multiply 0.85 blurred.png
magick result.png blurred.png -compose Overlay -composite result2.png

# View
img result2.png
