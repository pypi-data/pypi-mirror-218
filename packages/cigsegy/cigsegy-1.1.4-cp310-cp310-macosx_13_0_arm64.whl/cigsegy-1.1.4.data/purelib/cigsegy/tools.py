import numpy
from typing import List, Tuple
from .cigsegy import (Pysegy, collect, fromfile, tofile,
                      create_by_sharing_header)
import warnings


def create(segy_out: str,
           binary_in: str or numpy.ndarray,
           sizeZ: int,
           sizeY: int,
           sizeX: int,
           format: int = 5,
           dt: int = 2000,
           start_time: int = 0,
           X_interval: float = 25,
           Y_interval: float = 25,
           min_iline: int = 1,
           min_xline: int = 1,
           custom_info: List[str] = []) -> None:
    """
    Create a segy format file from a binary file or numpy.ndarray
    
    Parameters:
        - segy_out: str, out segy format file path
        - binary_in: str or numpy.array, the input binary file or array
        - sizeZ: int, number of inline
        - sizeY: int, number of crossline
        - sizeX: int, number of samples per trace
        - format: int, the data format code, 1 for 4 bytes IBM float, 5 for 4 bytes IEEE float
        - dt: int, data sample interval, 2000 means 2ms
        - start_time: int, start time for each trace
        - X_interval: int
        - Y_interval: int
        - min_iline: int, the start inline number
        - min_xline: int, the start crossline number
        - custom_info: textual header info by user custom, max: 12 rows
            each row is less than 76 chars
    """
    if isinstance(binary_in, str):
        segy_create = Pysegy(binary_in, sizeX, sizeY, sizeZ)
    elif isinstance(binary_in, numpy.ndarray):
        if binary_in.shape == (sizeZ, sizeY, sizeX):
            segy_create = Pysegy(sizeX, sizeY, sizeZ)
        else:
            raise RuntimeError(
                f'the binary_in shape: {binary_in.shape} does not match the input dim: ({sizeZ}, {sizeY}, {sizeX})'
            )
    else:
        raise ValueError(
            f'the input argument: binary_in must be a string or numpy array')
    segy_create.setDataFormatCode(format)
    segy_create.setSampleInterval(dt)
    segy_create.setStartTime(start_time)
    segy_create.setXInterval(X_interval)
    segy_create.setYInterval(Y_interval)
    segy_create.setMinInline(min_iline)
    segy_create.setMinCrossline(min_xline)
    if isinstance(binary_in, str):
        segy_create.create(segy_out, custom_info)
    else:
        segy_create.create(segy_out, binary_in, custom_info)


def eval_xline(segy: Pysegy) -> List:
    """
    To guess the crossline location of the segy
    """
    tracecout = segy.trace_count()
    options = [193, 17, 21]
    select = [193, 17, 21]
    for op in options:
        segy.setCrosslineLocation(op)
        l = []
        l.append(segy.get_traceInfo(0)[1])
        l.append(segy.get_traceInfo(1)[1])
        l.append(segy.get_traceInfo(2)[1])
        l.append(segy.get_traceInfo(tracecout // 2)[1])
        l.append(segy.get_traceInfo(tracecout - 1)[1])
        if sum([x > 0 for x in l]) != 5:
            select.remove(op)
            continue
        if l[0] == l[1] or l[0] == l[2] or l[1] == l[2]:
            select.remove(op)
            continue
        step = l[1] - l[0]
        if max(l) - min(l) > min((tracecout * step / 10), 10000 * step):
            select.remove(op)
            continue

    if select == []:
        raise RuntimeError("Cannot evaluate crossline location")

    return select


def eval_iline(segy: Pysegy) -> List:
    """
    To guess the inline location of the segy
    """
    tracecout = segy.trace_count()
    options = [189, 5, 9, 221]
    select = [189, 5, 9, 221]
    for op in options:
        segy.setInlineLocation(op)
        l0 = segy.get_traceInfo(0)[0]
        ll = segy.get_traceInfo(tracecout - 1)[0]
        l2 = segy.get_traceInfo(tracecout // 2)[0]
        if sum([x > 0 for x in [l0, ll, l2]]) != 3:
            select.remove(op)
            continue
        if l0 == ll or l0 == l2 or ll == l2:
            select.remove(op)
            continue
        if max([l0, ll, l2]) - min([l0, ll, l2]) > tracecout - 1:
            select.remove(op)
            continue
        l1 = segy.get_traceInfo(1)[0]
        ll2 = segy.get_traceInfo(tracecout - 2)[0]
        if l0 != l1 or ll != ll2:
            select.remove(op)
            continue

    if select == []:
        raise RuntimeError("Cannot evaluate inline location")

    return select


def eval_xstep(segy: Pysegy, xline: int) -> int:
    """
    To guess the crossline step
    """
    segy.setCrosslineLocation(xline)
    l0 = segy.get_traceInfo(0)[1]
    l1 = segy.get_traceInfo(1)[1]
    l2 = segy.get_traceInfo(2)[1]

    if l2 - l1 != l1 - l0:
        return 0
    else:
        return l2 - l1


def eval_istep(segy: Pysegy, iline: int) -> int:
    """
    To guess the inline step
    """
    segy.setInlineLocation(iline)
    i0 = segy.get_traceInfo(0)[0]
    x1 = 1
    while segy.get_traceInfo(x1)[0] == i0:
        x1 += 1
    i1 = segy.get_traceInfo(x1)[0]

    x2 = x1 + 1
    while segy.get_traceInfo(x2)[0] == i1:
        x2 += 1
    i2 = segy.get_traceInfo(x2)[0]

    if i2 - i1 != i1 - i0:
        return 0
    else:
        return i2 - i1


def guess(segy_name: str or Pysegy) -> List:
    """
    guess the locations and steps of inline and crossline

    Parameters:
        - segy_name: str, the input segy file

    return:
    locs: [loc1, loc2, ...], all possible loctaions,
          each location is like: [iline, xline, istep, xstep]
    """
    if isinstance(segy_name, str):
        segy = Pysegy(segy_name)
    elif isinstance(segy_name, Pysegy):
        segy = segy_name
    else:
        raise TypeError("Invalid type of `segy_name`")
    xlines = eval_xline(segy)
    ilines = eval_iline(segy)
    xselect = []
    iselect = []
    xsteps = []
    isteps = []

    for xline in xlines:
        xstep = eval_xstep(segy, xline)
        if xstep:
            xselect.append(xline)
            xsteps.append(xstep)

    for iline in ilines:
        istep = eval_istep(segy, iline)
        if istep:
            iselect.append(iline)
            isteps.append(istep)
    segy.close_file()

    out = []
    for i in range(len(iselect)):
        for x in range(len(xselect)):
            try:
                s = Pysegy(segy_name)
                s.setInlineLocation(iselect[i])
                s.setCrosslineLocation(xselect[x])
                s.setSteps(isteps[i], xsteps[x])
                t = s.metaInfo()
            except:
                continue

            out.append([iselect[i], xselect[x], isteps[i], xsteps[x]])

    if out == []:
        raise RuntimeError("cannot guess the location and steps")

    return out


def textual_header(segy_name: str) -> None:
    """
    Print segy file's 3200 bytes textual header.
    """
    segy = Pysegy(segy_name)
    print(segy.textual_header())
    segy.close_file()


def metaInfo(segy_name: str,
             iline: int = 189,
             xline: int = 193,
             istep: int = 1,
             xstep: int = 1,
             xloc: int = 73,
             yloc: int = 77,
             use_guess: bool = False) -> None:
    if use_guess:
        [iline, xline, istep, xstep] = guess(segy_name)[0]
    segy = Pysegy(segy_name)
    segy.setInlineLocation(iline)
    segy.setCrosslineLocation(xline)
    segy.setSteps(istep, xstep)
    segy.setXLocation(xloc)
    segy.setYLocation(yloc)
    print(segy.metaInfo())
    segy.close_file()


def fromfile_by_guess(segy_name: str) -> numpy.ndarray:
    """
    reading from a segy file.

    Parameters:
    - segy_name: the input segy file name
    """

    loc = guess(segy_name)

    for l in loc:
        try:
            metaInfo(segy_name, l[0], l[1], l[2], l[3])
            d = fromfile(segy_name, l[0], l[1], l[2], l[3])
            return d
        except:
            continue

    raise RuntimeError(
        "Cannot read by guess location, please specify the location")


def tofile_by_guess(segy_name: str, out_name: str) -> None:
    """
    convert a segy file to a binary file

    Parameters:
    - segy_name: the input segy file name
    - out_name: the output binary file name
    """
    loc = guess(segy_name)
    finish = False

    for l in loc:
        try:
            metaInfo(segy_name, l[0], l[1], l[2], l[3])
            tofile(out_name, l[0], l[1], l[2], l[3])
            finish = True
            break
        except:
            continue

    if not finish:
        raise RuntimeError(
            "Cannot read by guess location, please specify the location")


def create_by_sharing_header_guess(segy_name: str,
                                   header_segy: str,
                                   src: numpy.ndarray or str,
                                   shape: list or tuple = None,
                                   offset: list or tuple or dict = None,
                                   custom_info: List[str] = []) -> None:
    """
    create a segy and its header is from an existed segy.

    Parameters:
    - segy_name: str, the out segy name
    - header_segy: str, the header segy file
    - src: numpy.ndarray, source data
    - shape: if src is str, shape must be specify
    - offset: the offset of a sub data from a original data, 
            e.g., dsub = d[256:400, 500: 100:], offset = [256, 500, 100]
    - custom_info: textual header info by user custom, max: 12 rows
            each row is less than 76 chars, use it when offset is not None
    """
    if isinstance(src, str) and shape is None:
        raise ValueError("Shape is None!")

    loc = guess(header_segy)
    finish = False

    for l in loc:
        try:
            if isinstance(src, str):
                create_by_sharing_header(segy_name,
                                         header_segy,
                                         src,
                                         shape,
                                         l[0],
                                         l[1],
                                         l[2],
                                         l[3],
                                         offset=offset,
                                         custom_info=custom_info)
            else:
                create_by_sharing_header(segy_name,
                                         header_segy,
                                         src,
                                         l[0],
                                         l[1],
                                         l[2],
                                         l[3],
                                         offset=offset,
                                         custom_info=custom_info)
            finish = True
            break
        except:
            continue

    if not finish:
        raise RuntimeError(
            "Cannot read by guess location, please specify the location")


def plot_region(segy, loc: list = None, save: str = None) -> None:
    if isinstance(segy, Pysegy):
        try:
            segy.scan()
        except:
            loc = guess(segy)[0]
            segy.setInlineLocation(loc[0])
            segy.setCrosslineLocation(loc[1])
            segy.setSteps(loc[2], loc[3])
            segy.scan()
        lineinfo = segy.get_lineInfo()
        is_xline_fast = segy.is_crossline_fast_order()
    elif isinstance(segy, str):
        if loc is None:
            loc = guess(segy)[0]
        segyc = Pysegy(segy)
        segyc.setInlineLocation(loc[0])
        segyc.setCrosslineLocation(loc[1])
        segyc.setSteps(loc[2], loc[3])
        segyc.scan()
        lineinfo = segyc.get_lineInfo()
        is_xline_fast = segyc.is_crossline_fast_order()
    else:
        raise RuntimeError("Invalid type of `segy`")

    x = numpy.concatenate((lineinfo[:, 0], lineinfo[::-1, 0]))
    y = numpy.concatenate((lineinfo[:, 1], lineinfo[::-1, 2]))
    x = numpy.append(x, x[0])
    y = numpy.append(y, y[0])

    istep = x[1] - x[0]
    xstep = (lineinfo[0, 2] - lineinfo[0, 1]) // (lineinfo[0, 5] - 1)
    if not is_xline_fast:
        istep, xstep = xstep, istep

    import matplotlib.pyplot as plt

    plt.fill(x, y, color=(0.9, 0.9, 0.9))
    plt.plot(x, y)
    plt.gca().invert_yaxis()
    # plt.gca().xaxis.set_ticks_position('top')

    plt.grid(True, linestyle='--')
    xlabel = f"Inline Number/interval={istep}"
    ylabel = f"Crossline Number/interval={xstep}"
    if not is_xline_fast:
        xlabel, ylabel = ylabel, xlabel
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title('Region')
    if save:
        plt.savefig(save, dpi=200, bbox_inches='tight', pad_inches=0.0)
    plt.show()
