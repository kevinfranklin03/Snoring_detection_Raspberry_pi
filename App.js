import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Ionicons from 'react-native-vector-icons/Ionicons';

import HomeScreen from './screens/HomeScreen';
import SummaryScreen from './screens/SummaryScreen';
import FAQScreen from './screens/FAQScreen';

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ color, size }) => {
            let iconName;

            if (route.name === 'Home') iconName = 'play-circle';
            else if (route.name === 'Summary') iconName = 'bar-chart';
            else if (route.name === 'FAQ') iconName = 'help-circle';

            return <Ionicons name={iconName} size={size} color={color} />;
          },
          tabBarActiveTintColor: '#4CAF50',
          tabBarInactiveTintColor: 'gray',
          headerShown: false,
          tabBarStyle: { backgroundColor: '#121212' },
        })}
      >
        <Tab.Screen name="Home" component={HomeScreen} />
        <Tab.Screen name="Summary" component={SummaryScreen} />
        <Tab.Screen name="FAQ" component={FAQScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
