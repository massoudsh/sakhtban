/**
 * انتخاب موقعیت روی پلان طبقه با ضربه‌زدن روی تصویر (issue #22).
 * موقعیت به‌صورت نسبی (۰ تا ۱ روی عرض/ارتفاع تصویر) برگردانده می‌شود — مستقل از
 * سایز واقعی تصویر، برای این‌که سمت بک‌اند و روی نمایش‌های بعدی هم قابل استفاده باشد.
 * اگر پلان طبقه‌ای برای پروژه آپلود نشده باشد (imageUri خالی)، یک زمینه‌ی خنثی
 * نمایش داده می‌شود و کاربر همچنان می‌تواند روی آن ضربه بزند (مثلاً به‌عنوان نقشه‌ی کلی واحد).
 */
import { useState } from "react";
import { View, Image, Pressable, StyleSheet, Text, type GestureResponderEvent } from "react-native";

interface Props {
  imageUri?: string | null;
  value: { x: number; y: number } | null;
  onChange: (pos: { x: number; y: number }) => void;
}

export function FloorPlanPicker({ imageUri, value, onChange }: Props) {
  const [size, setSize] = useState({ width: 1, height: 1 });

  function handlePress(e: GestureResponderEvent) {
    const { locationX, locationY } = e.nativeEvent;
    const x = Math.min(1, Math.max(0, locationX / size.width));
    const y = Math.min(1, Math.max(0, locationY / size.height));
    onChange({ x, y });
  }

  return (
    <View>
      <Text style={styles.label}>موقعیت روی پلان طبقه (لمس کنید تا پین بگذارید)</Text>
      <Pressable
        onPress={handlePress}
        onLayout={(e) => setSize({ width: e.nativeEvent.layout.width, height: e.nativeEvent.layout.height })}
        style={styles.plan}
      >
        {imageUri ? (
          <Image source={{ uri: imageUri }} style={StyleSheet.absoluteFill} resizeMode="contain" />
        ) : (
          <View style={[StyleSheet.absoluteFill, styles.placeholder]} />
        )}
        {value && (
          <View
            style={[
              styles.pin,
              { left: `${value.x * 100}%`, top: `${value.y * 100}%` },
            ]}
          />
        )}
      </Pressable>
      {value && (
        <Text style={styles.coords}>
          موقعیت ثبت‌شده: {(value.x * 100).toFixed(0)}٪ ، {(value.y * 100).toFixed(0)}٪
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  label: { fontSize: 13, color: "#666", marginBottom: 6, textAlign: "right" },
  plan: {
    width: "100%",
    aspectRatio: 4 / 3,
    backgroundColor: "#eee",
    borderRadius: 10,
    overflow: "hidden",
  },
  placeholder: { backgroundColor: "#e2e2e2" },
  pin: {
    position: "absolute",
    width: 18,
    height: 18,
    marginLeft: -9,
    marginTop: -18,
    borderRadius: 9,
    backgroundColor: "#e0a800",
    borderWidth: 2,
    borderColor: "#fff",
  },
  coords: { fontSize: 12, color: "#666", marginTop: 4, textAlign: "right" },
});
