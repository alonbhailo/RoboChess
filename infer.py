#!/usr/bin/env python3
import cv2
import numpy as np
from hailo_platform import (HEF, VDevice, HailoStreamInterface, InferVStreams, ConfigureParams, InputVStreamParams, OutputVStreamParams, FormatType)


HEF_XCEPTION_PATH = "hefs/Xception_last.hef"


class RoboChess:
    def __init__(self, target):
        self._target = target
        self._xception_infer_vstreams = self._create_xception_infer_vstream(target)

    def _create_xception_infer_vstream(self, target):
        hef = HEF(HEF_XCEPTION_PATH)
        configure_params = ConfigureParams.create_from_hef(hef, interface=HailoStreamInterface.PCIe)
        network_group = target.configure(hef, configure_params)[0]
        input_vstreams_params = InputVStreamParams.make_from_network_group(network_group, quantized=False, format_type=FormatType.UINT8)
        output_vstreams_params = OutputVStreamParams.make_from_network_group(network_group, quantized=False, format_type=FormatType.FLOAT32)
        return InferVStreams(network_group, input_vstreams_params, output_vstreams_params)

    def infer(self):
        with self._xception_infer_vstreams as infer_pipeline:
            network_group = self._xception_infer_vstreams._configured_net_group
            input_vstream_info = network_group.get_input_stream_infos()[0]
            network_group_params = network_group.create_params()
            input_data = {input_vstream_info.name: np.random.randint(0, 256, size=(1, 299, 299, 3), dtype=np.uint8)}
            with network_group.activate(network_group_params):
                infer_results = infer_pipeline.infer(input_data)
                print(infer_results)

def main():
    with VDevice() as target:
        robochess = RoboChess(target)
        robochess.infer()
    # Open the video capture from /dev/video8
    cap = cv2.VideoCapture('/dev/video8')

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
    else:
         # Set the resolution (width and height)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2304)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1296)

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        
        # Check if the frame was successfully captured
        if ret:
            # Display the captured frame (image)
            cv2.imshow("Captured Image", frame)
            
            # Wait for 1ms for keypress and refresh display quickly
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Error: Could not read frame.")
            break
    cap.release()
    cv2.destroyAllWindows()

    #while True:
    #    # Read a frame from the camera
    #    ret, frame = cap.read()

    #    # Check if the frame was successfully captured
    #    if ret:
    #        # Display the captured frame (image)
    #        cv2.imshow("Captured Image", frame)

    #        # Wait for 1 millisecond for a key press
    #        # This allows the window to update every 1ms
    #        if cv2.waitKey(0.001) & 0xFF == ord('q'):  # Press 'q' to quit
    #            break
    #    else:
    #        print("Error: Could not read frame.")
    #        break
    #    # Release the capture device and close all windows
    #cap.release()
    #cv2.destroyAllWindows()
        

if __name__ == "__main__":
    main()
