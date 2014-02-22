from PIL import Image
import gifmaker


def smart_resize(filepath, width = 612, height = 612):

  img = Image.open(filepath)
  outfile = 'resize-%s' % filepath

  if img.format == "GIF":
    frames = []  
    try:
      while 1:
        frames.append(resize_img(img, width, height))
        img.seek(img.tell() + 1)
    except EOFError:
      pass # end of sequence

    fp = open(outfile, "wb")
    gifmaker.makedelta(fp, frames)
    fp.close()

  else:
    new_img = resize_img(img, width, height)
    new_img.save(outfile)

def resize_img(img, width, height):

  orig_height, orig_width = img.size

  if orig_height >= orig_width:
    f = float(width) / float(orig_width)
  else:
    f = float(height) / float(orig_height)


  new_img = img.resize((int(orig_height*f), int(orig_width*f)), Image.ANTIALIAS)

  new_height, new_width = new_img.size

  width_delta = (new_width - width)/2
  height_delta = (new_height - height)/2

  dim = (
     0 + height_delta, 
     0 + width_delta, 
     new_height - height_delta,
     new_width - width_delta
  )

  final_img = new_img.crop(dim)

  return final_img

if __name__ == '__main__':
  imgs = ['samp.png', 'ajax-loader.gif']
  for i in imgs:
    smart_resize(i)
