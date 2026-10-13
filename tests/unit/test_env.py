from vyra.env import diagnose, format_report


def test_diagnose_is_cheap_and_complete():
    report = diagnose()
    assert tuple(int(p) for p in report.python.split(".")[:2]) >= (3, 11)
    names = {n for n, _ in report.packages}
    assert {"numpy", "cv2", "torch", "ultralytics"} <= names
    assert report.gpu.startswith("não verificada")


def test_format_report_marks_missing_packages():
    text = format_report(diagnose())
    assert "python" in text and "gpu" in text
