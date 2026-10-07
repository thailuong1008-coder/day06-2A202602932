# Báo cáo Day 6: Calibration Projection QA

> Thay **mọi** ô có chữ ĐIỀN nằm trong ngoặc vuông bằng nội dung của bạn, xoá luôn cả dấu ngoặc vuông. Lệnh `python tools/check_submission.py` sẽ báo FAIL nếu còn sót bất kỳ chỗ nào.

- **Họ tên:** Nguyễn Thái Lương
- **MSSV:** 2A202602932
- **Lớp:** K4
- **Link repo:** https://github.com/NguyenThaiLuong/NguyenThaiLuong-2A202602932-Track4-Day21
- **Topic:** A — Kiểm tra calibration LiDAR-camera bằng projection
- **Dataset:** data/kitti_mini
- **Các frame đã dùng:** 000011

> Hãy viết ngắn: mỗi mục từ 3 đến 8 dòng, ưu tiên số liệu và hình ảnh.

## 1. Claim

Lệch yaw (xoay quanh trục Z) từ 0.5 đến 10 độ ít ảnh hưởng tới tổng % điểm LiDAR nằm trong toàn FOV, nhưng làm sai lệch nghiêm trọng sự tương quan giữa điểm LiDAR và 2D bounding box. Lỗi calibration từ 2 độ trở lên có thể dễ dàng nhận biết bằng mắt thường qua ảnh overlay.

## 2. Evidence

Bảng hoặc plot số liệu, kèm ảnh/video demo. Ghi rõ đường dẫn file trong `results/`.

| Cấu hình / mức perturb (yaw) | % điểm inside FOV | % điểm rơi vào 2D box | Ghi chú |
|---|---|---|---|
| 0.0 độ | 18.47% | 8.16% | Chuẩn |
| 1.0 độ | 18.47% | 8.30% | Bắt đầu lệch |
| 2.0 độ | 18.48% | 8.63% | Lệch rõ rệt |
| 3.0 độ | 18.47% | 8.79% | Điểm LiDAR của vật trượt ra khỏi vật trên ảnh |

![demo](../results/figures/overlay_000011_r0.0_p0.0_y0.0_t0.0_0.0_0.0.png)

## 3. Failure case

Nêu khi nào hệ thống hoặc phương pháp fail, vì sao fail, và liên hệ tới lớp nào trong 6 lớp debug: I/O, Geometry, Time, Preprocess, Model, Metric.

![failure](../results/figures/fail_000011_y3.0.png)

Khi góc lệch yaw >= 3.0 độ, hệ thống gặp failure ở lớp Geometry. Vì ma trận biến đổi `T_cam_velo` bị sai lệch (do sensor drift hoặc va đập), phép chiếu từ 3D sang 2D bị chệch hướng, khiến các điểm phản xạ thực tế của một chiếc xe bị vẽ văng ra ngoài không gian thực của xe đó trên hình.

## 4. Khuyến nghị nếu triển khai thật

Trong hệ thống xe tự hành (ADAS), độ chính xác của Sensor Fusion LiDAR-Camera cực kỳ nhạy cảm với extrinsic calibration. Nếu lệch quá 1 độ, hệ thống fusion 3D-2D sẽ chạy sai hoàn toàn. Cần thiết kế một module Online Calibration theo dõi Alignment Score (ví dụ so khớp viền ảnh với viền độ sâu LiDAR) để báo động khi sensor có biểu hiện bị xê dịch cơ học.

## 5. Cách chạy lại

Các lệnh tái tạo lại toàn bộ kết quả từ repo sạch.

```bash
python -m starter.projection --data-root data/kitti_mini --frame 000011
python -m src.topic_a
```

## 6. Khai báo sử dụng AI

Ghi rõ đã dùng công cụ AI nào, dùng vào việc gì, và bạn đã tự kiểm chứng kết quả đó bằng cách nào. Nếu không dùng AI, ghi "Không sử dụng". Xem quy định ở `RULES.md` mục 2.

| Công cụ | Dùng cho việc gì | Bạn đã kiểm chứng thế nào |
|---|---|---|
| Gemini | Hỗ trợ viết script thử nghiệm `src/topic_a.py` và gợi ý định dạng markdown cho báo cáo | Tự chạy thử lệnh sinh ra và kiểm tra kết quả qua ảnh và CSV sinh ra |
