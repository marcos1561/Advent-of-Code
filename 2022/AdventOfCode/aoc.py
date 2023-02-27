def get_input(input_path: str, to_strip=True) -> list[str]: 
    '''
    Read the input and return a list which i-th item is the
    i-th row in the input.

    Parameters:
    -----------
        input_path: str
            Path to the input file
        
        to_strip: bool
            If is to strip the input lines.

    Return:
    -------
        data: list
            The input lines.
    '''

    data = []
    with open(input_path, "r") as f:
        for line in f.readlines():
            if to_strip:
                data.append(line.strip())
            else:
                data.append(line)
    return data