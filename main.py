from pytube import YouTube
import datetime


url = 'https://www.youtube.com/watch?v=VwVg9jCtqaU'

def format_filesize(size):
    if size > 1000_000_000:
        return '{:.2f}GB'.format((size / 1000_000_000))
    elif size > 1000_000:
        return '{:.2f}MB'.format((size / 1000_000))
    elif size > 1000:
        return '{:.2f}KB'.format((size / 1000))
    return '{:.2f}B'.format(size)


def on_progress(stream, chunk, bytes_remains):
    filesize = stream.filesize
    _val = int(((1 - (bytes_remains / filesize)) * 100))
    #: credit 'https://stackoverflow.com/users/5283360/ivan-procopovich'

    '''
    index is expected to be 0 based index. 
    0 <= index < total
    '''
    bar_len = 60
    percent_done = (filesize-bytes_remains+1)/filesize*100
    percent_done = round(percent_done, 1)

    done = round(percent_done/(100/bar_len))
    togo = bar_len-done

    done_str = '█'*int(done)
    togo_str = '░'*int(togo)

    print(f'⏳{format_filesize(filesize - bytes_remains)} : [{done_str}{togo_str}] {percent_done}%\t', end='\r')

    if bytes_remains == 0:
        print('✅\t')


def load_url(url):
    ytb_obj = YouTube(url)
    ytb_obj.register_on_progress_callback(on_progress)
    streams = ytb_obj.streams

    videos = streams.order_by('resolution')
    audios = streams.filter(type='audio').order_by('filesize')

    return streams, videos, audios


streams, videos, audios = load_url(url)


def format_streams(videos, audios):

    formated_streams = []
    out_idx = 0

    for idx, s in enumerate(videos):
        formated_streams.append([str(idx), format_filesize(s.filesize), s.type, s.mime_type, s.resolution, f'{s.fps}FPS', s.is_progressive, s.title])
        out_idx = idx

    for a in audios:
        formated_streams.append([str(idx+1), format_filesize(a.filesize), a.type, a.mime_type, "none", f'{a.fps}FPS', s.is_progressive])
        idx += 1

    return formated_streams

def print_format(f_streams):
    print(f'{f_streams[0][-1]} is ready :- \n')
    print('Select one index from blew to download :- ')
    print(f'{"":<4} {"size":>10} {"type":>10} {"mime type":>14} {"resolution":>10} {"FPS":>10} {"progressive":>10}')

    for s in f_streams:
        print(f'{s[0]:<4} {s[1]:>10} {s[2]:>10} {s[3]:>15} {s[4]:>10} {s[5]:>10} {s[6]:>10}')
    
    valid = False
    idx = None

    while not valid:
        idx = input("Enter number :- ")

        if idx.isnumeric():
            valid = True

    _stream = f_streams[int(idx)]
    if _stream[4] != 'none':
        _ytb_file = streams.filter(resolution=_stream[4], mime_type=_stream[3], type=_stream[2], fps=int(_stream[5].replace('FPS', ''))).first()
    else:
        _ytb_file = streams.filter(mime_type=_stream[3], type=_stream[2], fps=int(_stream[5].replace('FPS', ''))).first()
    _filesize = _ytb_file.filesize

    _ytb_file.download(filename=f'[{datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M")}]-{_ytb_file.title}')
    print(f'{_ytb_file.title} is download successfully')


if __name__ == '__main__':
    f_streams = format_streams(videos, audios)
    print_format(f_streams)
