from pathlib import Path
from lxml import etree
import click
from PIL import Image
import io
import tqdm
import base64

@click.command()
@click.argument('src', type=click.Path(exists=True, dir_okay=False))
@click.option('-o', '--output-dir', type=click.Path(), required=True)
def export_notes(src, output_dir):
    parser = etree.HTMLParser(huge_tree=True)
    tree = etree.parse(src, parser)

    bookmark_containers = tree.xpath('//body/div[./div[@class="bm-image"]]')
    print(f'Found {len(bookmark_containers)} bookmarks')

    if not Path(output_dir).exists():
        Path(output_dir).mkdir()

    for idx, container in enumerate(tqdm.tqdm(bookmark_containers)):
        page_number = container.xpath('./p[@class="bm-page"]/text()')[0]

        img_element = container.xpath('./div[@class="bm-image"]/img')[0]
        img_blob_base64 = img_element.attrib['src'].split(',')[1]
        img_data = base64.b64decode(img_blob_base64)

        img = Image.open(io.BytesIO(img_data))

        out_path = Path(output_dir) / f'{idx}_{page_number}.png'
        img.save(out_path)

if __name__ == '__main__':
    export_notes()
