
# Development Guide
The `gstreamer_app.py` file contains shared classes that support the various pipeline scripts:

- **GStreamerApp Class**: Manages the GStreamer pipeline, handling events and callbacks.
- **App Callback Class**: Facilitates communication between the main application and callback functions, allowing for easy customization and extension.

The `gstreamer_helper_pipelines.py` file contains shared classes that support the various pipeline scripts:
- **pipeline helper functions** These functions are designed to encapsulate GStreamer pipelines, enabling developers to build robust and efficient pipelines without delving into the complexities of GStreamer syntax.


## Pipeline Helper Functions
Instead of manually crafting GStreamer pipelines, it is highly recommended to utilize the **pipeline helper functions** provided in `hailo_apps_infra/gstreamer_helper_pipelines.py`. This approach not only streamlines the development process but also ensures that best practices are consistently applied across all pipeline scripts. Queues also enfoces

### `QUEUE`

**Description:**
Creates a GStreamer `queue` element with configurable parameters. Queues are essential for managing the flow of data between different pipeline elements, ensuring smooth and efficient processing.It is also used to enable multithreading. A queue will create a new thread on its output, allowing different parts of the pipeline to run in parallel. See [Gstreamer Multithreading documentation](https://gstreamer.freedesktop.org/documentation/tutorials/basic/handy-elements.html#multithreading) for more details.

**Usage:**
Use the `QUEUE` function to insert buffering points in your pipeline, controlling the number of buffers, bytes, and time the queue can handle, as well as its leak behavior.

**For more details, refer to the [`QUEUE` function in `gstreamer_helper_pipelines.py`](hailo_apps_infra/gstreamer_helper_pipelines.py).**

### `SOURCE_PIPELINE`

**Description:**
Generates a GStreamer pipeline string tailored to the specified video source type (e.g., Raspberry Pi camera, USB camera, or file). It automatically configures essential properties such as format, width, and height based on the source.

**Usage:**
Utilize the `SOURCE_PIPELINE` function to create the source segment of your pipeline without manually specifying each element and property.

**For more details, refer to the [`SOURCE_PIPELINE` function in `gstreamer_helper_pipelines.py`](hailo_apps_infra/gstreamer_helper_pipelines.py).**

---

### `INFERENCE_PIPELINE`

**Description:**
Constructs a GStreamer pipeline string for performing inference and post-processing using user-provided HEF files and shared object (`.so`) post processing files. Integrates Hailo's inference engine (`hailonet`) and post-processing (`hailofilter`) elements seamlessly.

**Usage:**
Use the `INFERENCE_PIPELINE` function to set up the inference stage of your pipeline, specifying parameters like batch size, configuration files, and additional processing options.

**For more details, refer to the [`INFERENCE_PIPELINE` function in `gstreamer_helper_pipelines.py`](hailo_apps_infra/gstreamer_helper_pipelines.py).**

---

### `INFERENCE_PIPELINE_WRAPPER`

**Description:**
Wraps an existing inference pipeline with `hailocropper` and `hailoaggregator` elements. This wrapper maintains the original video resolution and color space, ensuring seamless integration with complex pipelines.

**Usage:**
Use the `INFERENCE_PIPELINE_WRAPPER` function to encapsulate your inference pipeline, facilitating advanced processing like cropping and aggregation without altering the original pipeline's properties.
**Note:** The post process will have to warp the network output to the 'original' resolution. This is not yet implemented in all post processes and metadata types.

**For more details, refer to the [`INFERENCE_PIPELINE_WRAPPER` function in `gstreamer_helper_pipelines.py`](hailo_apps_infra/gstreamer_helper_pipelines.py).**

---

### `TRACKER_PIPELINE`
**Description:**
Wraps an inner pipeline with hailocropper and hailoaggregator.
The cropper will crop detections made by earlier stages in the pipeline.
Each detection is cropped and sent to the inner pipeline for further processing.
The aggregator will combine the cropped detections with the original frame.
Example use case: After face detection pipeline stage, crop the faces and send them to a face recognition pipeline.

**Usage:**
Use the `TRACKER_PIPELINE` function to add a tracker stage to your pipeline for tracking detections.

**For more details, refer to the [`TRACKER_PIPELINE` function in `gstreamer_helper_pipelines.py`](hailo_apps_infra/gstreamer_helper_pipelines.py).**

---

### `DISPLAY_PIPELINE`

**Description:**
Generates a GStreamer pipeline string for displaying video output. Incorporates the `hailooverlay` plugin to render bounding boxes and labels, enhancing the visual output of processed frames.

**Usage:**
Utilize the `DISPLAY_PIPELINE` function to add a display segment to your pipeline, with options to enable FPS overlay and configure the video sink.

**For more details, refer to the [`DISPLAY_PIPELINE` function in `gstreamer_helper_pipelines.py`](hailo_apps_infra/gstreamer_helper_pipelines.py).**

---

### `USER_CALLBACK_PIPELINE`

**Description:**
Creates a GStreamer pipeline string for integrating a user-defined callback element. This allows developers to inject custom processing logic at specific points within the pipeline.

**Usage:**
Use the `USER_CALLBACK_PIPELINE` function to add a callback stage to your pipeline, enabling custom data handling and processing as needed.

**For more details, refer to the [`USER_CALLBACK_PIPELINE` function in `gstreamer_helper_pipelines.py`](hailo_apps_infra/gstreamer_helper_pipelines.py).**

### `CROPPER_PIPELINE`
**Description:**
Wraps an inner pipeline with hailocropper and hailoaggregator.
The cropper will crop detections made by earlier stages in the pipeline.
Each detection is cropped and sent to the inner pipeline for further processing.
The aggregator will combine the cropped detections with the original frame.
Example use case: After face detection pipeline stage, crop the faces and send them to a face recognition pipeline.

**Usage:**
Use the `CROPPER_PIPELINE` function to add a cropper stage to your pipeline, enabling cascading detections to the next network.

**For more details, refer to the [`CROPPER_PIPELINE` function in `gstreamer_helper_pipelines.py`](hailo_apps_infra/gstreamer_helper_pipelines.py).**

## Additional Features
Run any example with the `--help` flag to view all available options.

**Example:**
```bash
python hailo_apps_infra/pose_estimation_pipeline.py --help

usage: pose_estimation_pipeline.py [-h] [--input INPUT] [--use-frame] [--show-fps]
                          [--arch {hailo8,hailo8l}] [--hef-path HEF_PATH]
                          [--disable-sync] [--dump-dot]

Hailo App Help

options:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Input source. Can be a file, USB (webcam), RPi camera (CSI camera module) or ximage. For RPi camera use '-i rpi' Defaults to example video resources/example.mp4
  --use-frame, -u       Use frame from the callback function
  --show-fps, -f        Print FPS on sink
  --arch {hailo8,hailo8l}
                        Specify the Hailo architecture (hailo8 or hailo8l).
                        Default is None , app will run check.
  --hef-path HEF_PATH   Path to HEF file
  --disable-sync        Disables display sink sync, will run as fast as
                        possible. Relevant when using file source.
  --dump-dot            Dump the pipeline graph to a dot file pipeline.dot

```
Refer to the following sections for more information on using these options.

### Running with Different Input Sources
By default, these examples use an example video source. You can change the input source using the `--input` flag.


#### Raspberry Pi Camera Input
To use the Raspberry Pi camera input, run the following command:
```bash
python hailo_apps_infra/detection_pipeline.py --input rpi
```

#### USB Camera Input
To determine which USB camera to use, please run the following script:
```bash
get-usb-camera
```
This will help you identify an available camera.

**Test the camera functionality:**
```bash
ffplay -f v4l2 /dev/video<X>
```
**USB Camera input example:**
```bash
python hailo_apps_infra/detection_pipeline.py --input /dev/video<X>
```

#### XImage Window Input
This input is not compatible with Raspberry Pi (RPi).

In the CLI, run:
```bash
xwininfo
```
You should get an output like this:
```bash
xwininfo: Please select the window about which you
          would like information by clicking the
          mouse in that window.

xwininfo: Window id: 0xc3 (has no name)

  Absolute upper-left X:  0
  Absolute upper-left Y:  0
  Relative upper-left X:  0
  Relative upper-left Y:  0
  Width: 7040
  Height: 1440
  Depth: 24
  Visual: 0x21
  Visual Class: TrueColor
  Border width: 0
  Class: InputOutput
  Colormap: 0x20 (installed)
  Bit Gravity State: ForgetGravity
  Window Gravity State: NorthWestGravity
  Backing Store State: NotUseful
  Save Under State: no
  Map State: IsViewable
  Override Redirect State: yes
  Corners:  +0+0  -0+0  -0-0  +0-0
  -geometry 7040x1440+0+0
```
**USB Camera input example:**

```bash
python hailo_apps_infra/detection_pipeline.py --input <window id(In our example it is 0xc3)>
```

#### File input
```bash
python hailo_apps_infra/detection_pipeline.py  --input resources/example.mp4
```

### Using the Frame Buffer
To utilize the frame buffer, add the `--use-frame` flag. Be aware that extracting and displaying video frames can slow down the application due to non-optimized implementation. Writing to the buffer and replacing the old buffer in the pipeline is possible but inefficient.

### Printing the Frame Rate
To display the frame rate, add the `--show-fps` flag. This will print the FPS to both the terminal and the video output window.

### Dumping the Pipeline Graph
Useful for debugging and understanding the pipeline structure. To dump the pipeline graph to a DOT file, add the `--dump-dot` flag:
```bash
python hailo_apps_infra/detection_pipeline.py  --dump-dot
```
This creates a file named `pipeline.dot` in the `hailo_apps_infra` directory.

**Visualize the pipeline using Graphviz:**
1. **Install Graphviz:**
    ```bash
    sudo apt install graphviz
    ```
2. **Visualize the pipeline:**
    ```bash
    dot -Tx11 hailo_apps_infra/pipeline.dot &
    ```
3. **Save the pipeline as a PNG:**
    ```bash
    dot -Tpng hailo_apps_infra/pipeline.dot -o pipeline.png
    ```

# Troubleshooting and Known Issues
If you encounter any issues, please open a ticket in the [Hailo Community Forum](https://community.hailo.ai/). The forum is a valuable resource filled with useful information and potential solutions.

**Known Issues:**
- **Frame Buffer Performance:** The frame buffer extraction and display are not optimized, potentially slowing down the application. It is provided as a simple example.
- **DEVICE_IN_USE() Error:**
  The `DEVICE_IN_USE()` error indicates that the Hailo device (usually `/dev/hailo0`) is being accessed or locked by another process. This can occur during concurrent access attempts or if a previous process did not terminate cleanly.

  **Steps to Resolve:**

  1. **Identify the Device:**
     Ensure that `/dev/hailo0` is the correct device file for your setup.

  2. **Find Processes Using the Device:**
     List any processes currently using the Hailo device:
     ```bash
     sudo lsof /dev/hailo0
     ```

  3. **Terminate Processes:**
     Use the PID (Process ID) from the previous command's output to terminate the process. Replace `<PID>` with the actual PID:
     ```bash
     sudo kill -9 <PID>
     ```
