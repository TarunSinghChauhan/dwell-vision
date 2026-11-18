"""Track people in a video and show how long each stays in a zone.

No API key needed (default backend runs a YOLO model locally):
  python app.py --source in.mp4 --target out.mp4

Custom zone (x,y corner points):
  python app.py --source in.mp4 --zone 100,300 700,300 700,650 100,650

Optional Roboflow backend (needs ROBOFLOW_API_KEY and `pip install inference`):
  python app.py --source in.mp4 --backend roboflow
"""
import argparse

import numpy as np
import supervision as sv
from trackers import ByteTrackTracker

from dwell import DwellTimeTracker


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True, help="input video path")
    p.add_argument("--target", default="out.mp4", help="output video path")
    p.add_argument("--backend", choices=["ultralytics", "roboflow"], default="ultralytics")
    p.add_argument("--model", default=None, help="default: yolov8n.pt / yolov8n-640")
    p.add_argument("--zone", nargs="+", help="x,y points; default is the central area of the frame")
    p.add_argument("--conf", type=float, default=0.4)
    return p.parse_args()


def load_detector(backend, model_name):
    """Returns a function frame, conf -> sv.Detections."""
    if backend == "ultralytics":
        from ultralytics import YOLO

        model = YOLO(model_name or "yolov8n.pt")  # weights download automatically

        def detect(frame, conf):
            return sv.Detections.from_ultralytics(model(frame, conf=conf, verbose=False)[0])

    else:
        from inference import get_model

        model = get_model(model_name or "yolov8n-640")

        def detect(frame, conf):
            return sv.Detections.from_inference(model.infer(frame, confidence=conf)[0])

    return detect


def default_zone(width, height):
    x1, x2 = int(width * 0.2), int(width * 0.8)
    y1, y2 = int(height * 0.3), int(height * 0.9)
    return np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])


def main():
    args = parse_args()
    info = sv.VideoInfo.from_video_path(args.source)
    if args.zone:
        polygon = np.array([[int(v) for v in pt.split(",")] for pt in args.zone])
    else:
        polygon = default_zone(*info.resolution_wh)

    detect = load_detector(args.backend, args.model)
    tracker = ByteTrackTracker(frame_rate=info.fps)
    zone = sv.PolygonZone(polygon=polygon)
    dwell = DwellTimeTracker(fps=info.fps)

    box = sv.BoxAnnotator()
    label = sv.LabelAnnotator()
    zone_ann = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color.RED)

    with sv.VideoSink(args.target, info) as sink:
        for frame in sv.get_video_frames_generator(args.source):
            dets = detect(frame, args.conf)
            dets = dets[dets.class_id == 0]  # COCO "person"
            dets = tracker.update(dets)
            dets = dets[dets.tracker_id >= 0]  # drop not-yet-confirmed tracks

            in_zone = zone.trigger(dets)
            seconds = dwell.update(dets.tracker_id, in_zone)
            labels = [f"#{t} {seconds[int(t)]:.1f}s" for t in dets.tracker_id]

            frame = box.annotate(frame.copy(), dets)
            frame = label.annotate(frame, dets, labels)
            frame = zone_ann.annotate(frame)
            sink.write_frame(frame)

    print(f"Saved {args.target}")
    print("Seconds in zone per person:", dwell.summary())


if __name__ == "__main__":
    main()
