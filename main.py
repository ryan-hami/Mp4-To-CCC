import os, argparse, convert_to_ascii, convert_to_png

def read_args():
    parser = argparse.ArgumentParser(description="mp4 to youtube subtitle json")
    parser.add_argument('--fps',      dest='fps',      required=True)
    parser.add_argument('--file',     dest='file',     required=True)
    parser.add_argument('--columns',  dest='columns',  required=True)
    parser.add_argument('--msoffset', dest='msoffset', required=False)

    return parser.parse_args()

def throw(problem):
    print(problem)
    exit(1)

def validate_args(args):
    if int(args.fps) % 30 != 0:       throw("fps input must be a multiple of 30. Terminating.")
    if not os.path.exists(args.file): throw("file " + args.file + " was not found. Terminating.")

def traverse_temp(num_columns, ms, frames):
    triplet_iter = 0
    for frame in frames:
        duration_ms = 34 if triplet_iter == 2 else 33

        convert_to_ascii.convert(frame, ms, duration_ms, num_columns)

        # 33.333333 milliseconds would be a frame so every third frame we make it 34 ms (33+33+34=100)
        triplet_iter = (triplet_iter + 1) % 3

        ms += 34 if triplet_iter == 2 else 33


if '__main__' == __name__:
    args = read_args()
    validate_args(args)

    file = args.file
    fps = int(args.fps)
    mspf = 1000 / fps
    fpsdiv = fps / 30
    ms = int(args.msoffset or 0)
    num_columns = int(args.columns)
    '''
    num_columns =
	40 ---- 3:30 vids (Bad apple) if you upload your srt file and the subtitle
            doesn't appear its because the file is too big (5.5 i think is the max)
	56 ---- 2:00 vids so use less columms if your file is too big
    64 ---- max res
    '''

    print("Extracting pngs from video " + file + " . . .")
    frames = convert_to_png.convert(file)

    print('Generating Ascii art')
    traverse_temp(num_columns, ms, frames)

    # finalize .ytt and write to output
    convert_to_ascii.export()
