import sys, os, random
sys.stdout.reconfigure(encoding='utf-8')

print('='*55)
print(' BEHAVIOUR TRACKING MODULE DIAGNOSTIC')
print('='*55)

# 1. Imports
print('\n[1] Imports...')
try:
    from behaviour_tracking.detection import Detector
    print('  [PASS] detection.py')
except Exception as e:
    print('  [FAIL] detection.py:', e)

try:
    from behaviour_tracking.tracker import Tracker, Track
    print('  [PASS] tracker.py')
except Exception as e:
    print('  [FAIL] tracker.py:', e)

try:
    from behaviour_tracking.behaviour_analyzer import BehaviourAnalyzer
    print('  [PASS] behaviour_analyzer.py')
except Exception as e:
    print('  [FAIL] behaviour_analyzer.py:', e)

try:
    from behaviour_tracking.anomaly_detector import AnomalyDetector
    print('  [PASS] anomaly_detector.py')
except Exception as e:
    print('  [FAIL] anomaly_detector.py:', e)

try:
    from behaviour_tracking.video_stream import VideoStream
    print('  [PASS] video_stream.py')
except Exception as e:
    print('  [FAIL] video_stream.py:', e)

# 2. YOLOv8
print('\n[2] YOLOv8...')
try:
    from ultralytics import YOLO
    model_exists = os.path.exists('yolov8n.pt')
    print('  [PASS] ultralytics installed')
    print('  [INFO] yolov8n.pt present:', model_exists)
except ImportError:
    print('  [FAIL] ultralytics NOT installed - run: pip install ultralytics')

# 3. DeepSORT
print('\n[3] DeepSORT...')
try:
    from deep_sort_realtime.deepsort_tracker import DeepSort
    print('  [PASS] deep-sort-realtime installed')
except ImportError:
    print('  [WARN] Not installed - fallback centroid tracker will be used')

# 4. OpenCV + webcam
print('\n[4] OpenCV + Webcam...')
try:
    import cv2
    print('  [PASS] OpenCV version:', cv2.__version__)
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print('  [PASS] Webcam accessible (index 0)')
        cap.release()
    else:
        print('  [WARN] No webcam found - upload video mode only')
        cap.release()
except Exception as e:
    print('  [FAIL] OpenCV error:', e)

# 5. Behaviour classification test
print('\n[5] Behaviour classification logic...')
try:
    from behaviour_tracking.behaviour_analyzer import BehaviourAnalyzer
    from behaviour_tracking.tracker import Track
    analyzer = BehaviourAnalyzer()

    # Resting animal
    t1 = Track(1, [100,100,200,200], 'Cattle', 0.9)
    for _ in range(25):
        t1.history.append((150, 150))
    r1 = analyzer.analyse({1: t1})
    print('  [PASS] Resting test  ->', r1[1])

    # Walking animal
    t2 = Track(2, [300,300,400,400], 'Cattle', 0.9)
    x = 350
    for i in range(25):
        x += 8
        t2.history.append((x, 350))
    r2 = analyzer.analyse({2: t2})
    print('  [PASS] Walking test  ->', r2[2])

    # Stress animal (high variance movement)
    t3 = Track(3, [200,200,300,300], 'Cattle', 0.9)
    for i in range(25):
        t3.history.append((200 + random.randint(-40,40), 200 + random.randint(-40,40)))
    r3 = analyzer.analyse({3: t3})
    print('  [PASS] Stress test   ->', r3[3])

except Exception as e:
    print('  [FAIL] Behaviour logic:', e)

# 6. Alert / Anomaly engine
print('\n[6] Anomaly detector...')
try:
    from behaviour_tracking.anomaly_detector import AnomalyDetector
    ad = AnomalyDetector()
    counts = ad.alert_counts()
    print('  [PASS] Initial alert counts:', counts)
    ad.add_system_alert('INFO', 'Test alert fired OK')
    print('  [PASS] Alert added, total:', len(ad.recent_alerts()))
except Exception as e:
    print('  [FAIL] Anomaly detector:', e)

print('\n' + '='*55)
print(' DIAGNOSTIC COMPLETE')
print('='*55)
