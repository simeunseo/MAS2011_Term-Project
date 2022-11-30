import cv2
import sys
import numpy as np

def get_arguments():
    global width
    global height
    width = 960
    height = 540
    # get and set arguments
    input_video_arg = sys.argv[1]
    background_arg = sys.argv[2]
    output_video_arg = sys.argv[3]
    
    # get input video
    input_video = cv2.VideoCapture(input_video_arg)
    if not input_video.isOpened():
        print('video open failed!')
        sys.exit()
        
    # get background image and resize
    background = cv2.imread(background_arg)
    background = cv2.resize(background, (width, height), interpolation=cv2.INTER_CUBIC)
    
    # set delay time
    fps = round(input_video.get(cv2.CAP_PROP_FPS))
    delay = int(1000 / fps)
    
    # set video writer
    codec = "mp4v"
    fourcc = cv2.VideoWriter_fourcc(*codec)
    recorder = cv2.VideoWriter(output_video_arg, fourcc, fps, (width, height))
    return input_video, background, recorder, delay

def nothing(x):
        pass

def mouse_colorpick(event, x, y, flags, param):
        global color
        
        if event == cv2.EVENT_LBUTTONDOWN:
            
            print("HSV color @ position (%d,%d) = %s" %
                (x, y, ', '.join(str(i) for i in hsv[y, x])))
            
            color = np.array([hsv[y, x][0], hsv[y, x][1], hsv[y, x][2]])
    
def main():
    input_video, background, recorder, delay = get_arguments()
    global hsv
    global color
    
    # initialize values
    lower_bg = np.uint16(np.array([0, 0, 0]))
    upper_bg = np.uint16(np.array([255, 255, 255]))
    color = np.array([0,0,0])


    # create track bar for threshold
    panel_threshold = np.zeros([100, 100], np.uint8)
    cv2.namedWindow("panel_threshold")
    cv2.createTrackbar('threshold', 'panel_threshold', 0,100,nothing)

    '''
        you can use trackbar to select chroma key color if you need
    # create track bar for color bound
    panel_color = np.zeros([200, 700], np.uint8)
    cv2.namedWindow("panel_color")
    cv2.createTrackbar('L - h', 'panel_color', 0, 179, nothing)
    cv2.createTrackbar('U - h', 'panel_color', 179, 179, nothing)
    cv2.createTrackbar('L - s', 'panel_color', 0, 255, nothing)
    cv2.createTrackbar('U - s', 'panel_color', 255, 255, nothing)
    cv2.createTrackbar('L - v', 'panel_color', 0, 255, nothing)
    cv2.createTrackbar('U - v', 'panel_color', 255, 255, nothing)
    
    '''

    while True: 
        ret, frame = input_video.read() 
        if not ret: # quit when the input video ends
            break
        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        '''
            you can use trackbar to select chroma key color if you need
        
        l_h = cv2.getTrackbarPos('L - h', 'panel')
        u_h = cv2.getTrackbarPos('U - h', 'panel')
        l_s = cv2.getTrackbarPos('L - s', 'panel')
        u_s = cv2.getTrackbarPos('U - s', 'panel')
        l_v = cv2.getTrackbarPos('L - v', 'panel')
        u_v = cv2.getTrackbarPos('U - v', 'panel')
            
        lower_bg = np.array([l_h,l_s,l_v])
        upper_bg = np.array([u_h,u_s,u_v])
        
        lower_bg = np.array([0,0,128])
        upper_bg = np.array([179,76,247])
        
        '''
        
        cv2.imshow('input_video', frame)
        
        # set color to delete and adjust threshold
        cv2.setMouseCallback('input_video', mouse_colorpick)
        threshold = cv2.getTrackbarPos('threshold', 'panel_threshold')
        
        for i in range(3):
            if lower_bg[i] < threshold :
                lower_bg[i] = 0
            else :
                lower_bg[i] = color[i]-threshold
            upper_bg[i] = color[i]+threshold  

        
        #print("threshold :"+str(threshold))
        #print(lower_bg, upper_bg)    
        
        mask_og = cv2.inRange(hsv, lower_bg, upper_bg)
        # cv2.imshow('mask_og', mask_og)
        mask_blur = cv2.medianBlur(mask_og,9)
        #cv2.imshow('mask_blur', mask_blur)
        object = frame - cv2.bitwise_and(frame, frame, mask=mask_blur)
        #cv2.imshow('object', object)
        result = np.where(object==0, background, object)
        cv2.imshow('result', result)
        recorder.write(result)
        key = cv2.waitKey(delay)

        if key == 27: 
            break
            
    recorder.release()
    input_video.release() 
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()

