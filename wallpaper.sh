# Dimensions
magick identify a.jpg

# Resize
magick a.jpg -resize 1920x1080^ a2.jpg
magick a.png -resize 1920x1080^ -gravity east -extent 1920x1080 a2.png
magick b.png -resize 50% b2.png

# Crop
magick a.jpg -gravity southeast -extent 1920x1080+200 a2.png

# Shift hue
magick a2.jpg -modulate 100,100,50 a3.png # 50% = 200%; 0% = 300%
magick symbol.png -set option:modulate:colorspace hsv  -modulate 65,75,122 s.png

# Flip
magick a.jpg -flop b.jpg # Horizontally
magick a.jpg -flip b.jpg # Vertically

# Compose
magick a2.jpg b2.jpg +append -quality 100 result.jpg
magick wallpaper-prior.png sb.png -geometry +1920+0 -composite wallpaper2.png
magick original.png replacement.png -gravity center -composite output.png

# Blur & Overlay
magick result.jpg -blur 0x10 -evaluate Multiply 0.3 blurred.png
magick result.png blurred.png -compose Overlay -composite result2.png

# View
img result2.png

# Set
nitrogen ~/images/wallpapers/20xx/wallpaper.png --set-auto --save
