from PIL import Image

# loads an image
def load_image(loc):
    # loads the image from the file 'loc'
    img = Image.open(loc)

    # creates an array representing the rgb-values of the pixels of the image
    pixels = img.getdata()

    # size of the image
    width, height = img.size

    return pixels, width, height

# converts the pixels of the image to blocks
def convert_to_blocks(pixels):
    pixel, greyscale_pixels, blocks = [], [], []

    # loops through all the pixels
    for x in range(len(pixels)):
        pixel = pixels[x]

        # adds the greyscale-value of the pixel at x to greyscale_pixels
        greyscale_pixels.append((pixel[0] + pixel[1] + pixel[2]) / 3)

    # converts greyscale-pixels to blocks
    for y in range(int(height / block_height)):
        # adds a new line to the block-array
        blocks.append([])
        for x in range(int(width / block_width)):
            # creates a new block
            block = 0

            # loops through all the pixels that should be in the current block
            for y_offset in range(block_height):
                for x_offset in range(block_width):
                    # adds the value of the current pixel to the block-value
                    # y_offset -> y-offset from the first pixel of the block
                    # x_offset -> x-offset from the first pixel of the block
                    block += greyscale_pixels[(x * block_width + x_offset) + (y * block_height + y_offset) * width]

            # changes the block-value to the average value of its pixels
            block /= block_height * block_width

            # adds the current block to the block-array
            blocks[y].append(block)

    return blocks

# replaces each block with an ascii-character
def convert_to_ascii(blocks):
    # array that stores the characters
    chars = []

    # loops through all blocks
    for y in range(int(height / block_height)):
        # adds a new line to the character-array
        chars.append([])

        for x in range(int(width / block_width)):
            # adds a specified character for different block-values to the character-array
            # black
            if blocks[y][x] == 0:
                chars[y].append("@")
            # charcoal
            elif blocks[y][x] <= 32:
                chars[y].append("#")
            # darkgray
            elif blocks[y][x] > 32 and blocks[y][x] <= 64:
                chars[y].append("8")
            # mediumgray
            elif blocks[y][x] > 64 and blocks[y][x] <= 96:
                chars[y].append("&")
            # medium
            elif blocks[y][x] > 96 and blocks[y][x] <= 128:
                chars[y].append("o")
            # gray
            elif blocks[y][x] > 128 and blocks[y][x] <= 160:
                chars[y].append(":")
            # slategray
            elif blocks[y][x] > 192 and blocks[y][x] <= 224:
                chars[y].append("*")
            # lightgray
            elif blocks[y][x] > 224 and blocks[y][x] < 256:
                chars[y].append(".")
            # white
            else:
                chars[y].append(" ")

    return chars

# prints the character-array to the console
def print_chars(chars):
    for y in range(int(height / block_height)):
        for x in range(int(width / block_width)):
            print(chars[y][x], end="")

        print()

# saves the character-array to a file
def save_chars(location):
    # opens the file 'location', creates a new file if necessary
    file = open(location, "w")

    for y in range(int(height / block_height)):
        for x in range(int(width / block_width)):
            # writes the current character in the file
            file.write(chars[y][x])

        # creates a new line
        file.write("\n")

    # closes the file
    file.close()

# used for the main-loop, programm ends if is_runnig == 0
is_running = 1
chars = []
# size of a block
block_height, block_width = 6, 2

print("--------------------")
print("|image to ASCII art|")
print("--------------------")

# main-loop
while is_running == 1:
    # waits for an input that will determine what the programm will do next
    action = input("> ")

    # converts a new image to ascii
    if action == "new":
        # location of the image
        location = input("> sourcefile: ")

        pixels, width, height = load_image(location)
        print("Successfully loaded the image!")

        blocks = convert_to_blocks(pixels)

        chars = convert_to_ascii(blocks)

        print("Successfully convertet image to ASCII!")

    # prints the character-array to the console
    if action == "print":
        print_chars(chars)

    # saves the character-array to a file
    if action == "save":
        # location where it will be saved
        location = input("> save to: ")

        save_chars(location)

        print("> saved image to ", location)

    # ends the programm
    if action == "end":
        is_running = 0