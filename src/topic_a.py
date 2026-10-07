import pandas as pd
import numpy as np
from pathlib import Path
from starter.datasets import load_frame
from starter.projection import perturb_extrinsic, project_velo_to_image

def points_in_2d_box(uv, bbox):
    x1, y1, x2, y2 = bbox
    return (uv[:, 0] >= x1) & (uv[:, 0] <= x2) & (uv[:, 1] >= y1) & (uv[:, 1] <= y2)

def run_experiment(data_root="data/synthetic", frame="000000"):
    Path("results").mkdir(exist_ok=True)
    fr = load_frame(data_root, frame)
    calib = fr["calib"]
    points = fr["points"]
    image_shape = fr["image"].shape
    
    perturbations = [0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]
    results = []
    
    for yaw in perturbations:
        calib_p = perturb_extrinsic(calib, yaw_deg=yaw)
        uv, depth, mask = project_velo_to_image(points, calib_p, image_shape)
        
        pct_in_fov = mask.mean() * 100
        
        in_any_box = np.zeros(len(uv), dtype=bool)
        for obj in fr["labels"]:
            in_box = points_in_2d_box(uv, obj.bbox)
            in_any_box = in_any_box | in_box
            
        pct_in_box = (in_any_box.sum() / len(uv) * 100) if len(uv) > 0 else 0
        
        results.append({
            "yaw_deg": yaw,
            "pct_inside_fov": pct_in_fov,
            "pct_inside_2d_box": pct_in_box
        })
        
        if yaw == 3.0:
            import cv2
            from starter.projection import overlay_points, draw_box2d
            vis = overlay_points(fr["image"], uv, depth)
            for obj in fr["labels"]:
                vis = draw_box2d(vis, obj.bbox, label=obj.type)
            cv2.imwrite(f"results/figures/fail_000011_y{yaw}.png", vis)
        
    df = pd.DataFrame(results)
    df.to_csv("results/topic_a_experiment.csv", index=False)
    print(df)

if __name__ == "__main__":
    run_experiment(data_root="data/kitti_mini", frame="000011")
