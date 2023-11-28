import os, argparse, convert_to_ascii, cv2
from PIL import Image

def read_args():
    parser = argparse.ArgumentParser(description="mp4 to youtube subtitle json")
    parser.add_argument('--file',     dest='file',     required=True)
    parser.add_argument('--columns',  dest='columns',  required=True)
    parser.add_argument('--msoffset', dest='msoffset', required=False)

    return parser.parse_args()

def throw(problem):
    print(problem)
    exit(1)

def validate_args(args):
    # if int(args.fps) % 30 != 0:       throw("fps input must be a multiple of 30. Terminating.")
    if not os.path.exists(args.file): throw("file " + args.file + " was not found. Terminating.")


def print_progress_bar(iteration, total):
    percent = "{:.1f}".format(100 * (iteration / float(total)))
    progress = f"Progress: {iteration}/{total} - {percent}%"
    print(progress, end='\r', flush=True)

if '__main__' == __name__:
    args = read_args()
    validate_args(args)

    file = args.file
    msoffset = int(args.msoffset or 0)
    num_columns = int(args.columns)
    '''
    num_columns =
	40 ---- 3:30 vids (Bad apple) if you upload your srt file and the subtitle
            doesn't appear its because the file is too big (5.5 i think is the max)
	56 ---- 2:00 vids so use less columms if your file is too big
    64 ---- max res
    '''

    print("Extracting pngs from video " + file + " . . .")

    cam = cv2.VideoCapture(file)
    fps = cam.get(cv2.CAP_PROP_FPS)
    mspf = 1000 / fps

    cam.set(cv2.CAP_PROP_POS_MSEC, msoffset)

    frames = []

    while True:
        ret, frame = cam.read()
        if not ret: break
        frames.append(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))

    cam.release()

    num_frames = len(frames)

    print('Generating ASCII art')
    for i in range(num_frames):
        print_progress_bar(i, num_frames)
        frame = frames[i]

        # https://www.desmos.com/calculator/zi1oxgc0xx
        tile_width = frame.width / num_columns
        num_rows = round(0.43 * frame.height / tile_width)
        tile_height = frame.height / num_rows

        convert_to_ascii.convert(i, frame, mspf, num_columns, num_rows, tile_width, tile_height)

    # finalize .ytt and write to output
    convert_to_ascii.export()
