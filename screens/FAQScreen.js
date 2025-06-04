import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function FAQScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>❓ FAQ</Text>
      <Text style={styles.content}>This app detects snoring using Raspberry Pi and a trained AI model.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#121212', padding: 20 },
  title: { fontSize: 24, color: '#fff', marginBottom: 10 },
  content: { fontSize: 16, color: '#ccc' },
});
