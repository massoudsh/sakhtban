/** ثبت ایراد کیفی: عکس + موقعیت (GPS و پلان طبقه) + توضیح متنی/صوتی + پیمانکار + شدت (issue #22). */
import { useEffect, useState, useCallback } from "react";
import {
  View,
  Text,
  TextInput,
  Pressable,
  Image,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Alert,
} from "react-native";
import type { NativeStackScreenProps } from "@react-navigation/native-stack";
import { CameraView, useCameraPermissions } from "expo-camera";
import * as Location from "expo-location";
import { Audio } from "expo-av";
import type { RootStackParamList } from "@/App";
import type { DefectSeverity } from "@/lib/api";
import { submitOrQueue, getQueue, flushQueue } from "@/lib/offlineQueue";
import { FloorPlanPicker } from "@/components/FloorPlanPicker";
import { SeverityPicker } from "@/components/SeverityPicker";

type Props = NativeStackScreenProps<RootStackParamList, "NewDefect">;

export default function NewDefectScreen({ route }: Props) {
  const { projectId } = route.params;

  const [cameraPermission, requestCameraPermission] = useCameraPermissions();
  const [showCamera, setShowCamera] = useState(false);
  const [photoUri, setPhotoUri] = useState<string | null>(null);

  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [voiceUri, setVoiceUri] = useState<string | null>(null);
  const [isRecording, setIsRecording] = useState(false);

  const [gps, setGps] = useState<{ lat: number; lng: number } | null>(null);
  const [floorPlanPos, setFloorPlanPos] = useState<{ x: number; y: number } | null>(null);

  const [contractorName, setContractorName] = useState("");
  const [category, setCategory] = useState("");
  const [locationLabel, setLocationLabel] = useState("");
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [severity, setSeverity] = useState<DefectSeverity>("minor");

  const [submitting, setSubmitting] = useState(false);
  const [queueCount, setQueueCount] = useState(0);

  const refreshQueueCount = useCallback(() => {
    getQueue().then((q) => setQueueCount(q.length));
  }, []);

  useEffect(() => {
    refreshQueueCount();
    (async () => {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status === "granted") {
        const pos = await Location.getCurrentPositionAsync({});
        setGps({ lat: pos.coords.latitude, lng: pos.coords.longitude });
      }
    })();
  }, [refreshQueueCount]);

  async function takePhoto(camera: CameraView | null) {
    if (!camera) return;
    const photo = await camera.takePictureAsync({ quality: 0.6 });
    setPhotoUri(photo.uri);
    setShowCamera(false);
  }

  async function toggleVoiceRecording() {
    if (isRecording && recording) {
      setIsRecording(false);
      await recording.stopAndUnloadAsync();
      setVoiceUri(recording.getURI());
      setRecording(null);
      return;
    }
    const { status } = await Audio.requestPermissionsAsync();
    if (status !== "granted") {
      Alert.alert("دسترسی میکروفون رد شد", "برای ضبط توضیح صوتی به دسترسی میکروفون نیاز است.");
      return;
    }
    await Audio.setAudioModeAsync({ allowsRecordingIOS: true, playsInSilentModeIOS: true });
    const { recording: rec } = await Audio.Recording.createAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY);
    setRecording(rec);
    setIsRecording(true);
  }

  async function handleSubmit() {
    if (!title.trim() || !description.trim() || !locationLabel.trim()) {
      Alert.alert("اطلاعات ناقص", "عنوان، توضیح و موقعیت (متن) الزامی است.");
      return;
    }
    setSubmitting(true);
    try {
      const { sentNow } = await submitOrQueue({
        project_id: projectId,
        contractor_name: contractorName.trim() || null,
        title: title.trim(),
        description: description.trim(),
        category: category.trim() || null,
        location: locationLabel.trim(),
        photo_before_url: photoUri,
        voice_note_url: voiceUri,
        gps_lat: gps?.lat ?? null,
        gps_lng: gps?.lng ?? null,
        floor_plan_x: floorPlanPos?.x ?? null,
        floor_plan_y: floorPlanPos?.y ?? null,
        severity,
      });

      Alert.alert(
        sentNow ? "ثبت شد" : "در صف آفلاین ذخیره شد",
        sentNow
          ? "ایراد با موفقیت ثبت شد."
          : "اتصال برقرار نیست؛ به‌محض برگشت اینترنت به‌طور خودکار ارسال می‌شود."
      );

      setPhotoUri(null);
      setVoiceUri(null);
      setFloorPlanPos(null);
      setContractorName("");
      setCategory("");
      setLocationLabel("");
      setTitle("");
      setDescription("");
      setSeverity("minor");
      refreshQueueCount();
    } catch (err) {
      Alert.alert("خطا", err instanceof Error ? err.message : "ثبت ایراد ناموفق بود");
    } finally {
      setSubmitting(false);
    }
  }

  async function syncNow() {
    const result = await flushQueue();
    refreshQueueCount();
    Alert.alert("همگام‌سازی", `${result.sent} مورد ارسال شد، ${result.remaining} مورد در صف باقی ماند.`);
  }

  if (showCamera) {
    return (
      <CameraViewScreen onCapture={takePhoto} onCancel={() => setShowCamera(false)} permission={cameraPermission} requestPermission={requestCameraPermission} />
    );
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      {queueCount > 0 && (
        <Pressable style={styles.queueBanner} onPress={syncNow}>
          <Text style={styles.queueBannerText}>
            {queueCount} ایراد در صف آفلاین — برای تلاش دوباره لمس کنید
          </Text>
        </Pressable>
      )}

      <Text style={styles.sectionLabel}>عکس ایراد</Text>
      {photoUri ? (
        <Image source={{ uri: photoUri }} style={styles.photoPreview} />
      ) : (
        <Pressable style={styles.photoButton} onPress={() => setShowCamera(true)}>
          <Text style={styles.photoButtonText}>گرفتن عکس</Text>
        </Pressable>
      )}

      <FloorPlanPicker imageUri={null} value={floorPlanPos} onChange={setFloorPlanPos} />
      {gps && <Text style={styles.gpsText}>GPS: {gps.lat.toFixed(5)}, {gps.lng.toFixed(5)}</Text>}

      <TextInput style={styles.input} placeholder="عنوان ایراد" value={title} onChangeText={setTitle} />
      <TextInput
        style={[styles.input, styles.multiline]}
        placeholder="توضیح متنی"
        value={description}
        onChangeText={setDescription}
        multiline
      />
      <Pressable style={[styles.voiceButton, isRecording && styles.voiceButtonActive]} onPress={toggleVoiceRecording}>
        <Text style={styles.voiceButtonText}>
          {isRecording ? "پایان ضبط صدا" : voiceUri ? "ضبط دوباره‌ی توضیح صوتی" : "ضبط توضیح صوتی (اختیاری)"}
        </Text>
      </Pressable>

      <TextInput style={styles.input} placeholder="موقعیت (مثلاً: طبقه ۳، واحد ۱۲)" value={locationLabel} onChangeText={setLocationLabel} />
      <TextInput style={styles.input} placeholder="دسته (برق، نازک‌کاری، سازه...)" value={category} onChangeText={setCategory} />
      <TextInput style={styles.input} placeholder="پیمانکار مسئول" value={contractorName} onChangeText={setContractorName} />

      <Text style={styles.sectionLabel}>شدت</Text>
      <SeverityPicker value={severity} onChange={setSeverity} />

      <Pressable style={styles.submitButton} onPress={handleSubmit} disabled={submitting}>
        {submitting ? <ActivityIndicator color="#fff" /> : <Text style={styles.submitButtonText}>ثبت ایراد</Text>}
      </Pressable>
    </ScrollView>
  );
}

function CameraViewScreen({
  onCapture,
  onCancel,
  permission,
  requestPermission,
}: {
  onCapture: (camera: CameraView | null) => void;
  onCancel: () => void;
  permission: ReturnType<typeof useCameraPermissions>[0];
  requestPermission: () => void;
}) {
  let cameraRef: CameraView | null = null;

  if (!permission?.granted) {
    return (
      <View style={styles.permissionContainer}>
        <Text>برای گرفتن عکس به دسترسی دوربین نیاز است.</Text>
        <Pressable style={styles.submitButton} onPress={requestPermission}>
          <Text style={styles.submitButtonText}>اجازه‌ی دسترسی</Text>
        </Pressable>
        <Pressable onPress={onCancel}>
          <Text style={{ marginTop: 12 }}>انصراف</Text>
        </Pressable>
      </View>
    );
  }

  return (
    <View style={{ flex: 1 }}>
      <CameraView style={{ flex: 1 }} ref={(r) => (cameraRef = r)} />
      <View style={styles.cameraControls}>
        <Pressable style={styles.captureButton} onPress={() => onCapture(cameraRef)} />
        <Pressable onPress={onCancel} style={styles.cancelButton}>
          <Text style={{ color: "#fff" }}>انصراف</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16, gap: 12 },
  sectionLabel: { fontSize: 14, fontWeight: "700", textAlign: "right", marginTop: 6 },
  queueBanner: { backgroundColor: "#fff3cd", padding: 10, borderRadius: 8, marginBottom: 8 },
  queueBannerText: { textAlign: "right", color: "#8a6500", fontSize: 13 },
  photoButton: { backgroundColor: "#eee", borderRadius: 10, padding: 24, alignItems: "center" },
  photoButtonText: { fontWeight: "600" },
  photoPreview: { width: "100%", aspectRatio: 4 / 3, borderRadius: 10 },
  gpsText: { fontSize: 12, color: "#666", textAlign: "right" },
  input: { borderWidth: 1, borderColor: "#ccc", borderRadius: 8, padding: 12, textAlign: "right" },
  multiline: { minHeight: 80, textAlignVertical: "top" },
  voiceButton: { backgroundColor: "#eee", borderRadius: 8, padding: 12, alignItems: "center" },
  voiceButtonActive: { backgroundColor: "#f4c7c3" },
  voiceButtonText: { fontWeight: "600" },
  submitButton: { backgroundColor: "#1a1300", borderRadius: 10, padding: 16, alignItems: "center", marginTop: 8 },
  submitButtonText: { color: "#fff", fontWeight: "700" },
  permissionContainer: { flex: 1, justifyContent: "center", alignItems: "center", padding: 24, gap: 12 },
  cameraControls: {
    position: "absolute",
    bottom: 30,
    width: "100%",
    alignItems: "center",
    gap: 10,
  },
  captureButton: { width: 70, height: 70, borderRadius: 35, backgroundColor: "#fff", borderWidth: 4, borderColor: "#ccc" },
  cancelButton: { backgroundColor: "rgba(0,0,0,0.5)", paddingHorizontal: 16, paddingVertical: 8, borderRadius: 20 },
});
