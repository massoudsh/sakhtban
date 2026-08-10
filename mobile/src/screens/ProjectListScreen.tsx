import { useEffect, useState } from "react";
import { View, Text, FlatList, Pressable, StyleSheet, ActivityIndicator } from "react-native";
import type { NativeStackScreenProps } from "@react-navigation/native-stack";
import type { RootStackParamList } from "@/App";
import { api, type Project } from "@/lib/api";
import { activeProjectStorage } from "@/lib/storage";

type Props = NativeStackScreenProps<RootStackParamList, "ProjectList">;

export default function ProjectListScreen({ navigation }: Props) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getProjects()
      .then(setProjects)
      .catch((err) => setError(err instanceof Error ? err.message : "خطا در دریافت پروژه‌ها"))
      .finally(() => setLoading(false));
  }, []);

  async function selectProject(project: Project) {
    await activeProjectStorage.set(project.id);
    navigation.navigate("NewDefect", { projectId: project.id, projectName: project.name });
  }

  if (loading) return <ActivityIndicator style={{ flex: 1 }} />;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>پروژه‌ی خود را انتخاب کنید</Text>
      {error && <Text style={styles.error}>{error}</Text>}
      <FlatList
        data={projects}
        keyExtractor={(p) => p.id}
        renderItem={({ item }) => (
          <Pressable style={styles.card} onPress={() => selectProject(item)}>
            <Text style={styles.cardTitle}>{item.name}</Text>
            {item.location && <Text style={styles.cardSub}>{item.location}</Text>}
          </Pressable>
        )}
        ListEmptyComponent={!error ? <Text style={styles.empty}>پروژه‌ای یافت نشد.</Text> : null}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  title: { fontSize: 18, fontWeight: "700", marginBottom: 12, textAlign: "right" },
  card: { padding: 16, borderRadius: 10, backgroundColor: "#f2f2f2", marginBottom: 10 },
  cardTitle: { fontSize: 16, fontWeight: "600", textAlign: "right" },
  cardSub: { fontSize: 13, color: "#666", textAlign: "right", marginTop: 2 },
  empty: { textAlign: "center", color: "#888", marginTop: 40 },
  error: { color: "#d64545", textAlign: "center", marginBottom: 8 },
});
