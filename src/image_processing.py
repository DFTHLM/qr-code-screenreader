import finder_detection as fd

def getFinders(img):
    """
    this function takes a binary image input and attempts to find the finder patterns in it
    """

    # find the finder patterns in the original image
    candidates = fd.find_finder_patterns(img)
    return candidates # returning a set to remove duplicates

