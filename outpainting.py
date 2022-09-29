# from https://pypi.org/project/dalle2/#description

from dalle2 import Dalle2
from PIL import Image, ImageDraw
import urllib.request
import os,sys 

sess_id = sys.argv[1]
dalle = Dalle2(sess_id)
scale_factor = 0.9
prompt = "forest leaves, photoreal"
frames = 200

for i in range(0, frames):
    current_frame = str(i).zfill(4)
    previous_frame = str(i-1).zfill(4)

    src_file = os.path.join(os.getcwd() , "outpainting" , "A", previous_frame + ".png")
    if not os.path.exists(src_file):
        src_file = os.path.join(os.getcwd() , "outpainting" , "start.png")

    image = Image.open(src_file)
    m, n = image.size

    image_alpha = Image.new("RGBA", image.size, 0)

    # scale down image 90%
    image = image.resize((int(m*scale_factor), int(n*scale_factor)), Image.ANTIALIAS)

    # copy the scaled down image in the empty one
    margin = (1 - scale_factor) * 0.5
    image_alpha.paste(image, (int(m*margin), int(n*margin)))
    image_alpha.save(os.path.join(os.getcwd() , "outpainting", "next.png"))

    generations = dalle.generate_from_masked_image(
        prompt,
        os.path.join(os.getcwd() , "outpainting", "next.png"),
    )

    g=0
    abc=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    for generation in generations:
        # download image
        gen_image = generation["generation"]["image_path"]
        dest_folder = os.path.join(os.getcwd() , "outpainting" , abc[g])
        #create folder if needed
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        dest_file = os.path.join(dest_folder , current_frame + ".png")
        urllib.request.urlretrieve(gen_image, dest_file)
        g+=1

