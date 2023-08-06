from PyPDF2 import PdfReader, PageObject, Transformation, PdfWriter
from PyPDF2.generic import RectangleObject
from contextlib import ExitStack


LETTER_WIDTH = 612.0
LETTER_HEIGHT = 792.0
MARGIN_TOP = 50.0
MARGIN_BOTTOM = 50.0
MARGIN_LEFT = 50.0
MARGIN_RIGHT = 50.0

def transform(from_bbox, to_bbox,keep_aspect=False):
    x0, y0, x1, y1 = from_bbox
    a0, b0, a1, b1 = to_bbox

    scale_x = (a1-a0) / (x1-x0)
    scale_y = (b1-b0) / (y1-y0)

    if keep_aspect:
        if scale_x > scale_y:
            scale_x = scale_y
            extra = (a1 - a0) - (x1 - x0) * scale_x 
            a0 += extra / 2
        else:
            scale_y = scale_x
            extra = (b1 - b0) - (y1 - y0) * scale_y
            b0 += extra / 2

    return Transformation().translate(-x0, -y0).scale( scale_x, scale_y).translate(a0, b0)


def make_targets(margin, spacing, page_width, page_height):
    spacing /= 2.  # will add to each side to emd up with "spacing" distance
    return [
        (margin, page_height / 2 + spacing, page_width / 2 - spacing, page_height - margin),
        (page_width / 2 + spacing, page_height / 2 + spacing, page_width - margin, page_height - margin),
        (margin, margin, page_width / 2 - spacing, page_height / 2 - spacing),
        (page_width / 2 + spacing, margin, page_width - margin, page_height / 2 - spacing),
    ]

def merge(files, *, output, margin=20.0, spacing=0.0, keep_aspect=False):
    targets = make_targets(
        margin=margin,
        spacing=spacing,
        page_width=LETTER_WIDTH,
        page_height=LETTER_HEIGHT,
    )
    index = len(targets)
    with ExitStack() as stack:
        new_pages = []
        for fname in files:
            f = stack.enter_context(open(fname, 'rb'))
            pdf = PdfReader(f)
            for pageindex in range(len(pdf.pages)):
                if index >= len(targets):
                    page = PageObject.create_blank_page(None, LETTER_WIDTH, LETTER_HEIGHT)
                    new_pages.append(page)
                    index = 0
                p = pdf.pages[pageindex]
                x0, y0, x1, y1 = p.trimbox
                tr = transform(p.trimbox, targets[index], keep_aspect=keep_aspect)
                x0, y0 = tr.apply_on([x0, y0])
                x1, y1 = tr.apply_on([x1, y1])
                p.trimbox = RectangleObject([x0, y0, x1, y1])
                p.add_transformation(tr)
                page.merge_page(p)
                index += 1

        writer = PdfWriter()
        for page in new_pages:
            writer.add_page(page)

        with open(output, 'wb') as f:
            writer.write(f)

def main():
    import argparse

    parser = argparse.ArgumentParser('Merge multiple PDF pages onto a single page')
    parser.add_argument('-o', '--output', required=True, help='Output PDF file')
    parser.add_argument('-m', '--margin', type=float, default=20.0, help='Margin around sheet, in pts. Default is 10pt.')
    parser.add_argument('-s', '--spacing', type=float, default=0.0, help='Spacing petween min-pages, in pts. Default is 0pt')
    parser.add_argument('-k', '--keep-aspect', action='store_true', help='Set to preserve original aspect ratio')
    parser.add_argument('files', nargs='+')

    args = parser.parse_args()

    merge(args.files, output=args.output, keep_aspect=args.keep_aspect, margin=args.margin, spacing=args.spacing)


if __name__ == '__main__':
    main()