import finder_detection as fd

def getFinders(bimg):
    """
    this function takes a binary image input and attempts to find the finder patterns in it
    """

    # find the finder patterns in the original image
    candidates = fd.find_finder_patterns(bimg)
    return candidates # returning a set to remove duplicates

