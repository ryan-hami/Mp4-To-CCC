import os, argparse, convert_to_ascii, cv2
from PIL import Image

def read_args():
    parser = argparse.ArgumentParser(description=".mp4 to .ytt")
    parser.add_argument('--file',    dest='file',    required=True)
    parser.add_argument('--columns', dest='columns', required=True)
    parser.add_argument('--startms', dest='startms', required=False)

    return parser.parse_args()

def throw(problem):
    print(problem)
    exit(1)

def print_progress_bar(iteration, total):
    percent = "{:.1f}".format(100 * (iteration / float(total)))
    progress = f"Progress: {iteration}/{total} - {percent}%"
    print(progress, end='\r', flush=True)

def capture_frames(frames):
    video = cv2.VideoCapture(file)
    fps = video.get(cv2.CAP_PROP_FPS)

    video.set(cv2.CAP_PROP_POS_MSEC, startms)

    while True:
        ret, frame = video.read()
        if not ret: break
        frames.append(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))

    video.release()

    return fps

if '__main__' == __name__:
    args = read_args()
    if not os.path.exists(args.file): throw("file " + args.file + " was not found. Terminating.")

    file = args.file
    startms = int(args.startms or 0)
    num_columns = int(args.columns)

    print("Extracting pngs from video " + file + " . . .")

    frames = []
    fps = capture_frames(frames)
    mspf = 1000 / fps
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
    convert_to_ascii.export(file[:file.rfind(".")])
