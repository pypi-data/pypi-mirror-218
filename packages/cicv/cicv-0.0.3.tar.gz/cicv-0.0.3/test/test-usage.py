import cicv
import cv2
import time

# --------------------------------------------------
# Simple Usage

def _image_source():
    src = cicv.Source('../data/cat.jpg')
    fps = -1

    while(True):
        
        t_start = time.time()

        # Read Frame
        frame = src.read()

        # Display
        cicv.put_highlighted_text(frame=frame, message=f"FPS:{fps}")
        cv2.imshow('Test', frame)
        
        # Waitkey
        if cv2.waitKey(1) in [ ord('q'), 27, ord('Q') ]:
            break

        # Update time
        fps = 1//( time.time() - t_start )

    cv2.destroyAllWindows()
    src.release()

def _image_folder_source():
    src = cicv.Source('./data')
    timeout, wait_fps = 1/src.get_fps(), time.time()
    while(True):

        if (time.time()-wait_fps) < timeout:
            continue

        frame = src.read()
        
        cv2.imshow('Test', frame)
        if cv2.waitKey(1) in [ ord('q'), 27, ord('Q') ]:
            break
    cv2.destroyAllWindows()
    src.release()

def _video_source():
    
    src = cicv.Source('../data/test.mp4')
    fps = -1
    
    while(True):

        t_start = time.time()

        frame = src.read()
        
        cicv.put_highlighted_text(frame, f"FPS: {fps}")
        cv2.imshow('Test', frame)
        if cv2.waitKey(1) in [ ord('q'), 27, ord('Q') ]:
            break

        fps = 1//(time.time() - t_start)

    cv2.destroyAllWindows()
    src.release()

def _cam_source():
    # Method 1
    src = cicv.Source('/dev/video0')
    src.set_cam(width=1280,height=720, fps=30)
    
    timeout, wait_fps = 1/src.get_fps(), time.time()
    while(True):

        if (time.time()-wait_fps) < timeout:
            continue

        frame = src.read()
        cv2.imshow('Test', frame)
        if cv2.waitKey(1) in [ ord('q'), 27, ord('Q') ]:
            break

    cv2.destroyAllWindows()
    src.release()

def _rtsp_source():
    src = cicv.Source('rtsp://admin:admin@172.16.21.1:554/snl/live/1/1/n')
    src.set_cam(height=1080, width=1920, fps=30)
    timeout, wait_fps = 1/src.get_fps(), time.time()
    while(True):

        if (time.time()-wait_fps) < timeout:
            continue

        frame = src.read()
        cv2.imshow('Test', frame)
        if cv2.waitKey(1) in [ ord('q'), 27, ord('Q') ]:
            break

    cv2.destroyAllWindows()
    src.release()

def _image_resize():
    src = cicv.Source('./data/cat.jpg', (640, 480))

    timeout, wait_fps = 1/src.get_fps(), time.time()
    while(True):

        if (time.time()-wait_fps) < timeout:
            continue

        frame = src.read()
        
        cv2.imshow('Test', frame)
        if cv2.waitKey(1) in [ ord('q'), 27, ord('Q') ]:
            break
    cv2.destroyAllWindows()
    src.release()

if __name__ == "__main__":
    _image_source()
    # _image_folder_source()
    _video_source()
    # _cam_source()
    # _rtsp_source()
    # _image_resize()