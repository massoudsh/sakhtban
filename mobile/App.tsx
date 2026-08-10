/** اپ موبایل ثبت ایراد کیفی — سخت‌بان QA (issue #22). */
import { useEffect } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { StatusBar } from "expo-status-bar";
import LoginScreen from "@/screens/LoginScreen";
import ProjectListScreen from "@/screens/ProjectListScreen";
import NewDefectScreen from "@/screens/NewDefectScreen";
import { subscribeAutoFlush } from "@/lib/offlineQueue";

export type RootStackParamList = {
  Login: undefined;
  ProjectList: undefined;
  NewDefect: { projectId: string; projectName: string };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  useEffect(() => {
    // با برگشت اینترنت، صف آفلاین ثبت ایراد به‌طور خودکار خالی می‌شود.
    const unsubscribe = subscribeAutoFlush();
    return unsubscribe;
  }, []);

  return (
    <NavigationContainer>
      <StatusBar style="auto" />
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen name="Login" component={LoginScreen} options={{ title: "ورود" }} />
        <Stack.Screen name="ProjectList" component={ProjectListScreen} options={{ title: "پروژه‌ها" }} />
        <Stack.Screen
          name="NewDefect"
          component={NewDefectScreen}
          options={({ route }) => ({ title: `ثبت ایراد — ${route.params.projectName}` })}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
