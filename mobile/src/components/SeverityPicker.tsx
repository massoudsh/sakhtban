import { View, Pressable, Text, StyleSheet } from "react-native";
import type { DefectSeverity } from "@/lib/api";

const OPTIONS: { value: DefectSeverity; label: string; color: string }[] = [
  { value: "minor", label: "جزئی", color: "#3aa76d" },
  { value: "major", label: "مهم", color: "#e0a800" },
  { value: "critical", label: "بحرانی", color: "#d64545" },
];

export function SeverityPicker({ value, onChange }: { value: DefectSeverity; onChange: (v: DefectSeverity) => void }) {
  return (
    <View style={styles.row}>
      {OPTIONS.map((opt) => {
        const selected = opt.value === value;
        return (
          <Pressable
            key={opt.value}
            onPress={() => onChange(opt.value)}
            style={[styles.chip, { borderColor: opt.color }, selected && { backgroundColor: opt.color }]}
          >
            <Text style={[styles.chipText, selected && { color: "#fff" }]}>{opt.label}</Text>
          </Pressable>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: "row-reverse", gap: 8 },
  chip: { flex: 1, paddingVertical: 10, borderRadius: 8, borderWidth: 1.5, alignItems: "center" },
  chipText: { fontWeight: "600" },
});
