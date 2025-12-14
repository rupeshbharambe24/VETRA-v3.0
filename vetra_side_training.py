"""
Backend training helper for VETRA side-view pose model.

This file is NOT for presentation.
It uses Ultralytics YOLOv8n-pose as the training engine under the hood,
then wraps the best checkpoint into VetraPoseNet and exports ONNX/TS.

Your notebook will only call `train_vetra_side_pose()` from here.
"""

from pathlib import Path
import torch

from ultralytics import YOLO  # hidden from the notebook
from vetra_yolopose.model import VetraPoseNet


# Default config for side-view training
DEFAULT_SIDE_CFG = {
    # Base YOLOv8 pose model
    "base_model": "yolov8n-pose.pt",

    # Dataset YAML for side-view keypoints
    "data_yaml": Path(
        r"D:\Projects\VETRA\Codes\VETRA v3.0\Training and Processing\vetra_side_pose_dataset\vetra_side_pose.yaml"  # <<< change if needed
    ),

    # Number of keypoints in SIDE view
    "num_keypoints": 14,

    # Training hyperparams
    "imgsz": 640,
    "epochs": 100,
    "batch": 16,
    "patience": 20,
    "project": "runs/side_view",
    "name": "vetra_pose_side_v1",
    "workers": 4,
}


def train_vetra_side_pose(cfg: dict | None = None) -> dict:
    """
    Train side-view VETRA pose model.

    Args:
        cfg: optional dict overriding DEFAULT_SIDE_CFG keys.

    Returns:
        dict with paths:
          {
            "results_dir": Path,
            "best_ckpt": Path,
            "onnx_path": Path,
            "ts_path": Path,
          }
    """
    # Merge config
    if cfg is None:
        cfg = {}
    config = DEFAULT_SIDE_CFG.copy()
    config.update(cfg)

    device = "0" if torch.cuda.is_available() else "cpu"

    print("\n🚀 Training VETRA PoseNet – Side view")
    print("-------------------------------------")
    print("Dataset YAML:", config["data_yaml"])
    print("Base model:", config["base_model"])
    print("Image size:", config["imgsz"])
    print("Epochs:", config["epochs"])
    print("Batch:", config["batch"])
    print("Device:", device)

    # 1) Create YOLO pose model (hidden here)
    yolo_model = YOLO(config["base_model"])

    # 2) Run training – Ultralytics prints its usual rich logs
    results = yolo_model.train(
        data=str(config["data_yaml"]),
        imgsz=config["imgsz"],
        epochs=config["epochs"],
        batch=config["batch"],
        patience=config["patience"],
        project=config["project"],
        name=config["name"],
        device=device,
        workers=config["workers"],
        exist_ok=True,
        verbose=True,
    )

    # 3) Locate best weights
    results_dir = Path(results.save_dir)
    best_ckpt = results_dir / "weights" / "best.pt"

    print("\n✅ Training finished.")
    print("Results dir:", results_dir)
    print("Best checkpoint:", best_ckpt)

    # 4) Wrap into VetraPoseNet
    print("\n🔗 Building VetraPoseNet from best checkpoint...")
    net_device = "cuda" if torch.cuda.is_available() else "cpu"
    net = VetraPoseNet.from_ultralytics_checkpoint(
        ckpt_path=str(best_ckpt),
        num_keypoints=config["num_keypoints"],
        device=net_device,
    )

    # 5) Export ONNX + TorchScript for deployment (pre-NMS)
    onnx_path = best_ckpt.with_name("vetra_side_pose.onnx")
    ts_path   = best_ckpt.with_name("vetra_side_pose.ts")

    print("\n📤 Exporting ONNX...")
    net.export_onnx(str(onnx_path), img_size=config["imgsz"])
    print("   ->", onnx_path)

    print("📤 Exporting TorchScript...")
    net.export_torchscript(str(ts_path), img_size=config["imgsz"])
    print("   ->", ts_path)

    print("\n🎯 VETRA side-view pose training complete.")

    return {
        "results_dir": results_dir,
        "best_ckpt": best_ckpt,
        "onnx_path": onnx_path,
        "ts_path": ts_path,
    }
