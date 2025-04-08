from os import rmdir
from PIL import Image
from pathlib import Path
from zipfile import ZipFile
from datetime import datetime

TRAY_SIZE = 96  # and need to be called tray.png
STICKER_SIZE = 512
TRAY_IMAGE_FORMAT = 'png'
STICKER_IMAGE_FORMAT = 'webp'
INPUT_DIR = Path('input_dir')
OUTPUT_DIR = Path('output')


def is_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()  # Verifies if the image can be opened
        return True
    except (IOError, SyntaxError):
        return False


def handle_txt_file(txt_file_path: Path, default_name) -> str:
    if not txt_file_path.exists():
        txt_file_path.touch()
        prompt = f'Please enter {"a title" if txt_file_path.name == "title.txt" else "an author"} to the pack: '
        txt_file_path.write_text(prompt if prompt else default_name)
    txt_value = txt_file_path.read_text(encoding='utf8')
    print(f'{txt_file_path} is being used with value of "{txt_value}"')
    return txt_value


def verify_title_and_author() -> str:
    title = handle_txt_file(INPUT_DIR / 'title.txt', f'nezorf{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')
    handle_txt_file(INPUT_DIR / 'author.txt', 'nezorf')
    return title


def check_for_tray_image():
    tray_image_path = INPUT_DIR / 'tray.png'  # TODO more file types support
    if not tray_image_path.exists():
        print(f'{tray_image_path.name} not found, using an image from the pack')
        # TODO: continue


def resize_image(image_input_path, image_output_path, new_width, new_height, file_format):
    with Image.open(image_input_path) as img:
        img = img.resize((new_width, new_height), Image.LANCZOS)
        img.save(image_output_path, file_format)


def reformat_stickers():
    Path.mkdir(OUTPUT_DIR, exist_ok=True)
    for i, item in enumerate(INPUT_DIR.iterdir()):
        if not is_image(item):
            continue
        # TODO if name == tray.png add as tray and also as the sticker if flag
        new_name = OUTPUT_DIR / f'sticker_{i}.{STICKER_IMAGE_FORMAT}'
        resize_image(item, new_name, STICKER_SIZE, STICKER_SIZE, STICKER_IMAGE_FORMAT)
        print(new_name)
        if i == 30:
            print('maximum number of images reached!')
            break


def zip_and_format_pack(pack_name: str = None):
    zip_file_path = Path(f'{pack_name}.zip')
    with ZipFile(zip_file_path, 'w') as zip_file:
        for file in OUTPUT_DIR.iterdir():
            file_path = Path(file)
            zip_file.write(file_path, file_path.name)

    wastickers_file_type = zip_file_path.with_suffix('.wastickers')
    zip_file_path.rename(wastickers_file_type)
    print('Done! your sticker pack is at', zip_file_path)
    # delete output dir, we only need the pack
    # rmdir(OUTPUT_DIR)


def make_sticker_pack():
    Path.mkdir(INPUT_DIR, exist_ok=True)
    pack_title = verify_title_and_author()
    check_for_tray_image()
    reformat_stickers()
    zip_and_format_pack(pack_title)


if __name__ == '__main__':
    make_sticker_pack()
    # make_above_minimum_all_directory('input_dir')
