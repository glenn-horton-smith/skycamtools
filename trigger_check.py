import imageio
import numpy as np

class TriggerCheck:
    """Class used for checking effect of trigger level on a video
    using SkySentinel algorithm
    [1] http://www.goskysentinel.com/docs/skysentinel_guide.pdf
    """
    def __init__(self):
        """Sets up class with default values for
        threshold, triggerGap, triggerCountBegin, triggerSumBegin
        """
        self.threshold = 35
        self.triggerGap = 10
        self.triggerCountBegin = 2
        self.triggerSumBegin = 12
    
    def check_video_max_threshold(self, filename,
                                  thresholdVideoOutFilename=None):
        """Reads a video filename and get max threshold
        that would trigger the SkySentinel algorithm.
        Also write a video showing frame diffs
        if thresholdVideoOutFilename is set, write out a video showing
        differences over gap.
        """
        rdr = imageio.get_reader(filename)
        if thresholdVideoOutFilename:
            vout = imageio.get_writer(thresholdVideoOutFilename,
                                      fps= rdr.get_meta_data()['fps'])
        else:
            vout = None
        imbuf = list( rdr.get_next_data().max(axis=2).astype('h')
                      for i in range(self.triggerGap) )
        thbuf = [0] * self.triggerCountBegin
        # convert triggerSumBegin to percentage of pixels
        pct = 100.0 * ( 1.0 - self.triggerSumBegin / imbuf[0].size )
        iframe = 0
        ith = 0
        maxthn = 0
        for imrgb in rdr:
            im = imrgb.max(axis=2).astype('h')
            diff = im - imbuf[iframe]
            imbuf[iframe] = im
            iframe = (iframe+1) % self.triggerGap
            da = np.abs(diff)
            th = np.percentile(da.flatten(), pct)
            thbuf[ith] = th
            ith = (ith+1) % self.triggerCountBegin
            thn = min(thbuf)
            if thn > maxthn:
                maxthn = thn
            if vout:
                dp = np.clip(diff, 0, 255).astype(np.uint8)
                dn = np.clip(-diff, 0, 255).astype(np.uint8)
                imrgb[:,:,0] = dp
                imrgb[:,:,1] = da.astype(np.uint8)
                imrgb[:,:,2] = dn
                vout.append_data(imrgb)
        if vout:
            vout.close()
        return maxthn
    
            
def main(argv):
    tc = TriggerCheck()
    for arg in argv[1:]:
        maxthn = tc.check_video_max_threshold(arg, arg + '-diff.mp4')
        print( "%g %s" % (maxthn, arg) )

if __name__ == "__main__":
    import sys
    main(sys.argv)

        
