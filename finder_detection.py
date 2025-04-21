# finder pattern detection algorithm from https://pmc.ncbi.nlm.nih.gov/articles/PMC8321072/#sec3-jimaging-06-00067

def confirm_pattern(run_lengths, tolerance=1.5, middle_tolerance=2.0): # works only when assuming the pattern is B | W | B | W | B (which it should be)
    """
    check if the run lengths match the expected pattern of a finder pattern
    uses the tolrance from the original paper
    """

    # avoiding sum to help the time complexity at least a bit
    w = run_lengths[0] + run_lengths[1] + run_lengths[2] + run_lengths[3] + run_lengths[4]

    if w < 7:
        return False

    w /= 7
    
    # kind of ignoring DRY, but this seems much more readable than the alternative
    if w - tolerance <= run_lengths[0] <= w + tolerance and \
       w - tolerance <= run_lengths[1] <= w + tolerance and \
       w * 3 - middle_tolerance <= run_lengths[2] <= w * 3 + middle_tolerance and \
       w - tolerance <= run_lengths[3] <= w + tolerance and \
       w - tolerance <= run_lengths[4] <= w + tolerance:
        if run_lengths[2] > max(run_lengths[0] + run_lengths[1], run_lengths[3] + run_lengths[4]):
            return True

    return False

def group_candidates(candidates):
    """
    groups the finder pattern candidates vertically and horizontally
    vertically by 3/7 of the width of the pattern
    and horizontally by 3
    """
    
    # group the candidates by their x coordinate
    candidates.sort(key=lambda x: x[0]) # sort by x coordinate
    grouped_vertically = []
    current_group = []

    for i in range(len(candidates)):
        if i == 0:
            current_group.append(candidates[i])
        else:
            if abs(candidates[i][0] - candidates[i-1][0]) < 3: # if the distance between the two candidates is less than 3, add them to the same group
                current_group.append(candidates[i])
            else:
                grouped_vertically.append(current_group)
                current_group = [candidates[i]]

    grouped_vertically.append(current_group) # add the last group
    grouped_horizontally = []

    for group in grouped_vertically:
        group.sort(key=lambda x: x[1])
        current_group = []

        for i in range(len(group)):
            if i == 0:
                current_group.append(group[i])
            else:
                if abs(group[i][1] - group[i-1][1]) < (group[i][2] * 3) / 7: # if the distance between the two candidates is less than 3, add them to the same group
                    current_group.append(group[i])
                else:
                    grouped_horizontally.append(current_group)
                    current_group = [group[i]]

        grouped_horizontally.append(current_group) # add the last group

    # remove duplicates
    grouped_horizontally = [list(set(group)) for group in grouped_horizontally]
    return grouped_horizontally

def find_finder_patterns(binary_img):
    """
    slides a window across the image to find patterns
    that match the basic finder pattern structure.

    colors is a list of colors in the pattern
    run_lengths is a list of the lengths of the runs - a run is a continuous path of the same color
    count is the number of pixels of the same color in a straight line

    run 2x - once on normal image, then rotate 90 degrees and run again to find vertical and horiznontal patterns

    """
    h, w = binary_img.shape
    candidates = []

    for y in range(h): # iterate over each column
        run_lengths = []
        colors = []
        current_color = binary_img[y, 0]
        count = 0

        for x in range(w): # move the window across the image
            pixel = binary_img[y, x]
            if pixel == current_color:
                count += 1
            else:   # color change -> save the count and the color of the run, count = 1 as we move to the following pixel
                run_lengths.append(count)
                colors.append(current_color)
                current_color = pixel
                count = 1

        # save the last run
        run_lengths.append(count)
        colors.append(current_color)

        for i in range(len(run_lengths) - 4): # len(run_lengths) - 4 to avoid index out of range, each finder pattern has 5 color variations - B -> W -> B -> W -> B
            runs = run_lengths[i:i+5]
            run_colors = colors[i:i+5]

            if run_colors == [0, 255, 0, 255, 0]: # check that the pattern matches the expected colors (cant start with white)
                if confirm_pattern(runs): # if the pattern matches the expected structure, append the center of the pattern to the candidates list
                    x_center = sum(runs[:2]) + runs[2] / 2 + sum(runs[3:4])
                    x_pixel = int(sum(run_lengths[:i]) + x_center)
                    candidates.append((x_pixel, y, sum(runs)))

        # now group the patterns vertically and horizontally
    candidates = group_candidates(candidates)

    for x in candidates:
       x.sort(key=lambda x: x[1])
       print(x)

