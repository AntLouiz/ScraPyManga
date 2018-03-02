import os
import glob
import img2pdf


def manga_to_pdf(title, chapter, manga_path):
  """
    Converts a chapter of a manga in pdf.
  """

  chapter_path = os.path.join(manga_path, str(chapter))

  if not os.path.exists(chapter_path):
    raise OSError()

  chapter_pdf_name = "{} {}.pdf".format(title, chapter)
  chapter_pdf_path = os.path.join(chapter_path, chapter_pdf_name)

  chapter_pages = glob.glob(
    os.path.join(chapter_path, '*jpg')
  )
  
  chapter_pdf_bytes = img2pdf.convert(chapter_pages)

  with open(chapter_pdf_path, "wb") as pdf_file:
    pdf_file.write(chapter_pdf_bytes)

  return chapter_pdf_path