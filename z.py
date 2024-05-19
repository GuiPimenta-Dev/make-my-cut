from PIL import Image

# Define the ASCII characters to use
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]


def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width / 1.65
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image


def grayify(image):
    grayscale_image = image.convert("L")
    return grayscale_image


def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel // 25]
    return ascii_str


def main(image_path, new_width=100):
    image = Image.open(image_path)
    image = resize_image(image, new_width)
    image = grayify(image)
    ascii_str = pixels_to_ascii(image)
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ""
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i : i + img_width] + "\n"
    return ascii_img


if __name__ == "__main__":
    image_path = "diagram.png"  # Replace with your image path
    ascii_image = main(image_path)
    print(ascii_image)
