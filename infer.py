#!/usr/bin/env python3
import cv2
import numpy as np
from hailo_platform import (HEF, VDevice, HailoStreamInterface, InferVStreams, ConfigureParams, InputVStreamParams, OutputVStreamParams, FormatType)
from preprocess import preprocess


HEF_XCEPTION_PATH = "hefs/Xception_last.hef"


class RoboChess:
    def __init__(self, target):
        self._target = target
        self._xception_infer_vstreams = self._create_xception_infer_vstream(target)

    def _create_xception_infer_vstream(self, target):
        hef = HEF(HEF_XCEPTION_PATH)
        configure_params = ConfigureParams.create_from_hef(hef, interface=HailoStreamInterface.PCIe)
        configure_params['Xception_last'].batch_size = 64
        network_group = target.configure(hef, configure_params)[0]
        input_vstreams_params = InputVStreamParams.make_from_network_group(network_group, quantized=False, format_type=FormatType.UINT8)
        output_vstreams_params = OutputVStreamParams.make_from_network_group(network_group, quantized=False, format_type=FormatType.FLOAT32)
        return InferVStreams(network_group, input_vstreams_params, output_vstreams_params)

    def infer(self, input_data):
        with self._xception_infer_vstreams as infer_pipeline:
            network_group = self._xception_infer_vstreams._configured_net_group
            network_group_params = network_group.create_params()
            with network_group.activate(network_group_params):
                infer_results = infer_pipeline.infer(input_data)
                return infer_results


def main():
    with VDevice() as target:
        robochess = RoboChess(target)

        # Open the video capture from /dev/video0
        cap = cv2.VideoCapture('/dev/video0')

        # Check if the camera opened successfully
        if not cap.isOpened():
            print("Error: Could not open camera.")
        else:
            # Set the resolution (width and height)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            # Set the capture format to MJPEG (if supported by the camera)
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        while True:
            # Read a frame from the camera
            ret, frame = cap.read()

            # Check if the frame was successfully captured
            if ret:
                # Display the captured frame (image) continuously
                cv2.imshow("Captured Image", cv2.resize(frame, (1024,768)))

                # Wait for keypress
                key = cv2.waitKey(1) & 0xFF

                if key == ord('q'):  # If 'q' is pressed, exit
                    break
                elif key == ord(' '):  # If spacebar is pressed, process the frame
                    print("Processing Board")
                    # Perform the preprocessing and inference only when spacebar is pressed
                    detected, cropped_board, pieces64 = preprocess(frame)
                    if not detected:
                        continue
                    #pieces64 /= 255
                    #pieces64 -= 1
                    board_result = robochess.infer(pieces64)  # 64 on 13
                    # Display the cropped board
                    cv2.imshow("Cropped Board", cv2.resize(cropped_board, (1024,768)))

            else:
                print("Error: Could not read frame.")
                break

        cap.release()
        cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
