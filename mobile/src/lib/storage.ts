/** لایه‌ی نگهداری توکن و پروژه‌ی فعال روی دستگاه (AsyncStorage). */
import AsyncStorage from "@react-native-async-storage/async-storage";

const TOKEN_KEY = "sakhtban_token";
const PROJECT_KEY = "sakhtban_active_project_id";

export const tokenStorage = {
  get: () => AsyncStorage.getItem(TOKEN_KEY),
  set: (token: string) => AsyncStorage.setItem(TOKEN_KEY, token),
  clear: () => AsyncStorage.removeItem(TOKEN_KEY),
};

export const activeProjectStorage = {
  get: () => AsyncStorage.getItem(PROJECT_KEY),
  set: (projectId: string) => AsyncStorage.setItem(PROJECT_KEY, projectId),
};
