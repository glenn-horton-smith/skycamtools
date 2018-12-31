import sys
import os
import subprocess
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#JPG_VIEW_COMMAND=['display','-immutable','-geometry','+0+0']
MP4_VIEW_COMMAND=['vlc']

def manual_sort(dirin, dirout):
    categories = list( line.strip() for line in
                       open(dirout+'/categories.txt') )
    categories.sort()
    keycodes = dict( (c[0], c) for c in categories )
    if len(keycodes) != len(categories):
        raise Exception("Non-unique category first letters")
    prompt = '  '.join(categories) + '  ?(to show mp4) :  '
    csvlist = list( fn for fn in os.listdir(dirin)
                    if fn[0] == 'c' and fn.endswith('.csv') )
    viewer_log = open('manual_sort_viewer_log.txt','w')
    csvlist.sort()
    fig = plt.figure(1)
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
        imgplot = plt.imshow(img)
        ax = fig.axes[0]
        ax.set_title(t)
        fig.canvas.set_window_title(sys.argv[0] + " " + t)
        fig.canvas.draw_idle()
        proc2 = None
        while True:
            fig.canvas.draw_idle()
            answer = input(prompt)
            if answer == '?' and proc2 == None:
                # pid2 = os.spawnlp(os.P_NOWAIT, VIEWER_COMMAND, VIEWER_COMMAND,
                #          '%s/m%s.mp4'%(dirin, t))
                proc2 = subprocess.Popen(
                    MP4_VIEW_COMMAND + ['%s/m%s.mp4'%(dirin, t)],
                    stdin=subprocess.DEVNULL,
                    stdout=viewer_log, stderr=subprocess.STDOUT)
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
        if proc2:
            proc2.terminate()
    print("All files processed.")


    
def moveall(t, dirin, dirout, category):
    for k in [('m','mp4'), ('c','csv'), ('j','jpg'), ('e','txt')]:
        fn = '%s%s.%s'%(k[0], t, k[1])
        os.rename('%s/%s'%(dirin,fn), '%s/%s/%s'%(dirout,category,fn))


def main(argv):
    if len(argv) <= 2:
        print("Usage: manual_sort.py (indir) (outdir)")
        sys.exit(1)
    manual_sort(argv[1], argv[2])


if __name__ == "__main__":
    main(sys.argv)
