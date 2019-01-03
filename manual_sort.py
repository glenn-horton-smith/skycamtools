"""An interactive tool for humans to sort events from Spalding AllSky camera
images collected by WSentinel.exe.  (www.goskysentinal.com)

Requires:
  matplotlib for displaying images,
  vlc for displaying videos efficiently,
  evdisp (uses imageio) for displaying events frame-by-frame.

Invoke at command line as
   python3 (unsorted events directory) (sorted events directory)

All files from WSentinel should be present in unsorted events directory.
The sorted events directory should contain subdirectories for each category,
and a single file named "categories.txt" with one category name per line.
The subdirectory names must match the names in categories.txt exactly, and
the first letter of category must be unique.

Interaction is through the keyboard.  Time-lapse exposure images for
each event are presented one at a time. Press "?" to see the video for
the event.  Press the first letter of a category to move the files for
the event to the file.  Press ctrl-D or ctrl-C to exit.

If you accidentally move an image to the wrong category, you can
exit the program and move the files to the right directory manually.

If you decide later to split a category into two categories, then you
can run this program specifying the subdirectory of the category that
you want to split as the input directory.

:author: Glenn Horton-Smith, 2018-12-31

"""

import sys
import os
import subprocess
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import evdisp

#JPG_VIEW_COMMAND=['display','-immutable','-geometry','+0+0']
MP4_VIEW_COMMAND=['vlc']

def manual_sort(dirin, dirout):
    """This is the main function for doing all the work.
    See module description for usage.
    """
    categories = list( line.strip() for line in
                       open(dirout+'/categories.txt') )
    categories.sort()
    keycodes = dict( (c[0], c) for c in categories )
    if len(keycodes) != len(categories):
        raise Exception("Non-unique category first letters")
    prompt = '  '.join(categories) + '  ?(to animate event)  /(event display) :  '
    csvlist = list( fn for fn in os.listdir(dirin)
                    if fn[0] == 'c' and fn.endswith('.csv') )
    viewer_log = open('manual_sort_viewer_log.txt','w')
    csvlist.sort()
    fig,ax = plt.subplots()
    figprompt = fig.text(0, 1, prompt, verticalalignment='top', wrap=True)
    fig.canvas.set_window_title(sys.argv[0])
    fig.show()
    for csv in csvlist:
        t = csv[1:-4]
        print(t)
        # pid = os.spawnlp(os.P_NOWAIT, VIEWER_COMMAND, VIEWER_COMMAND,
        #                  '%s/j%s.jpg'%(dirin, t))
        # proc = subprocess.Popen(JPG_VIEW_COMMAND + ['%s/j%s.jpg'%(dirin, t)],
        #                         stdin=subprocess.DEVNULL,
        #                         stdout=viewer_log, stderr=subprocess.STDOUT)
        img = mpimg.imread('%s/j%s.jpg'%(dirin, t))
        plt.figure(fig.number)
        imgplot = ax.imshow(img)
        ax.set_title(t)
        fig.canvas.set_window_title(sys.argv[0] + " " + t)
        fig.canvas.draw_idle()
        evd = None
        proc2 = None
        while True:
            fig.canvas.draw_idle()
            answer = input(prompt)
            if answer == '?':
                # pid2 = os.spawnlp(os.P_NOWAIT, VIEWER_COMMAND, VIEWER_COMMAND,
                #          '%s/m%s.mp4'%(dirin, t))
                if proc2 == None:
                    proc2 = subprocess.Popen(
                        MP4_VIEW_COMMAND + ['%s/m%s.mp4'%(dirin, t)],
                        stdin=subprocess.DEVNULL,
                        stdout=viewer_log, stderr=subprocess.STDOUT)
                else:
                    print("Video already playing")
                continue
            elif answer == '/':
                if evd == None:
                    evd = evdisp.evdisp(None)
                evd.open('%s/m%s.mp4'%(dirin, t))
                continue
            elif answer in keycodes:
                category = keycodes[answer]
                moveall(t, dirin, dirout, category)
                # f = open('%s/%s.txt' % (dirout, category), 'a')
                # f.write(t+"\n")
                # f.close()
                break
            else:
                print("Invalid response %s" % answer)
        # os.kill(pid, signal.SIGTERM)
        # if pid2 != None:
        #     os.kill(pid2, signal.SIGTERM)
        #proc.terminate()
        ax.clear()
        evd.stopvideo()
        evd.f.canvas.window().hide()
    print("All files processed.")


    
def moveall(t, dirin, dirout, category):
    """Utility function for moving all files for a given event to the
    appropriate category subdirectory.
    """
    for k in [('m','mp4'), ('c','csv'), ('j','jpg'), ('e','txt')]:
        fn = '%s%s.%s'%(k[0], t, k[1])
        os.rename('%s/%s'%(dirin,fn), '%s/%s/%s'%(dirout,category,fn))


def main(argv):
    """main() for command-line invocation"""
    if len(argv) <= 2:
        print("Usage: manual_sort.py (indir) (outdir)")
        sys.exit(1)
    manual_sort(argv[1], argv[2])


if __name__ == "__main__":
    main(sys.argv)
