# merge videos
# mencoder -really-quiet -ovc lavc -lavcopts vcodec=mjpeg -mf fps=${FPS} -vf scale=${videoX}:${videoY} -o $output_video_file_name video_*.avi

echo '' > humans_list.txt
let i=0
for fi in events-manual-sorted/humansnear/m*.mp4; do
    let i=i+1
    echo "file '$fi'" >> humans_list.txt
done
ffmpeg -f concat -i humans_list.txt -c copy humansnear.mp4

python3 humans_subtitle.py > humans_subtitle.srt

# https://stackoverflow.com/questions/8672809/use-ffmpeg-to-add-text-subtitles
#  - dotokikja's answer will add subtitles to the subtitle stream
#  - HdN8's answer will "burn" them into the video

# dotokikja's technique, omitting audio
ffmpeg -i humansnear.mp4 -f srt -i humans_subtitle.srt \
       -map 0:0  -map 1:0 -c:v copy  \
       -c:s mov_text humansnear_cc.mp4
# HdN8's technique
ffmpeg -i humans_subtitle.srt  humans_subtitle_0.ass
awk '// { if ($0 ~ /Style: Default/) { print "Style: Default,Arial,15,&Hffffff,&Hffffff,&H0,&H0,0,0,0,0,100,100,0,0,1,1,0,7,10,10,10,0"; } else { print $0}}' humans_subtitle_0.ass > humans_subtitle.ass

ffmpeg -i humansnear.mp4 -vf ass=humans_subtitle.ass humansnear_timestamped.mp4

