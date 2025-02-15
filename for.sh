for x in {115..125..3}; do
	for y in {65..80..5}; do
		for z in {75..90..5}; do
			magick symbol.png -set option:modulate:colorspace hsv -modulate $z,$y,$x s${x}-${y}-${z}.png
		done
	done
done
